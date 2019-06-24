import dcfurs
import badge
import random
import settings
import emote
from micropython import const

## Enumerated types for each cell of the maze.
MAZE_NULL = ord('.')    # cell has not been visited during generation
MAZE_UP = ord('^')      # arrived here by moving up
MAZE_DOWN = ord('v')    # arrived here by moving down
MAZE_LEFT = ord('<')    # arrived here by moving left
MAZE_RIGHT = ord('>')   # arrived here by moving right
MAZE_FINISH = ord('X')  # destination cell
MAZE_WALL = ord('*')    # cell is a wall

def dirxy(direction, magnitude=1):
    if direction == MAZE_UP:
        return (0,-magnitude)
    if direction == MAZE_DOWN:
        return (0,magnitude)
    if direction == MAZE_LEFT:
        return (-magnitude,0)
    if direction == MAZE_RIGHT:
        return (magnitude,0)
    return (0,0)

class maze:
    def __init__(self, width=51, height=51):
        self.blink = True
        self.interval = 200
        self.width = (width | 1)
        self.height = (height | 1)
        self.autosolve = settings.mazesolver
        self.counter = 0
        self.wincount = 5000 / self.interval
        
        # Build actual maze
        self.z = []
        for y in range(self.height):
            self.z.append(bytearray([MAZE_NULL] * self.width))
        
        # Fill borders
        for x in range(self.width):
            self.z[0][x] = MAZE_WALL
            self.z[self.height-1][x] = MAZE_WALL
        for y in range(self.height):
            self.z[y][0] = MAZE_WALL
            self.z[y][self.width-1] = MAZE_WALL
        
        # Pick a random end point on even coordinates.
        self.x = random.randint(0, self.width-2) | 1
        self.y = random.randint(0, self.height-2) | 1
        self.z[self.y][self.x] = MAZE_FINISH
        #print("Start: %d,%d" % (self.x,self.y))

        # generate the map working backward from the ending point
        start = (self.x,self.y)
        depth = 0
        maxDepth = 0

        while True:
            ## Choose a random direction and calculate its depth.
            dirset = [MAZE_UP, MAZE_DOWN, MAZE_LEFT, MAZE_RIGHT]
            valid = False
            while len(dirset) != 0:
                direction = random.choice(dirset)
                dirset.remove(direction)
                dx,dy = dirxy(direction, magnitude=-2)
                nx,ny = self.x+dx,self.y+dy
                
                if nx < self.width and nx >= 0 and ny < self.height and ny >= 0:
                    if self.z[ny][nx] == MAZE_NULL:
                        valid = True
                        self.z[ny][nx] = direction
                        self.z[(dy>>1) + self.y][(dx>>1) + self.x] = direction
                        self.x += dx
                        self.y += dy
                        depth += 2
                        break
            
            ## Rewind if there was no unexplored direction we could go.
            if not valid:
                if depth > maxDepth:
                    start = (self.x,self.y)
                    maxDepth = depth
                dx,dy = dirxy(self.z[self.y][self.x], magnitude=2)
                if (dx == 0) and (dy == 0):
                    break
                depth -= 2
                self.x += dx
                self.y += dy

        ## Convert remaining cells into walls
        self.x = start[0]
        self.y = start[1]
        for row in self.z:
            for i in range(len(row)):
                if row[i] == MAZE_NULL:
                    row[i] = MAZE_WALL

    def render(self, xpos, ypos):
        for y in range(0, dcfurs.nrows):
            zy = y+ypos
            if (zy < 0) or (zy >= self.height):
                dcfurs.set_row(y, 0)
                continue
            row = self.z[zy]
            for x in range(dcfurs.ncols):
                zx = x+xpos
                if (zx < 0) or (zx >= self.width):
                    dcfurs.set_pixel(x, y, 0)
                elif row[zx] == MAZE_WALL:
                    dcfurs.set_pixel(x, y, 1)
                elif row[zx] == MAZE_FINISH:
                    dcfurs.set_pixel(x, y, 0xff if self.blink else 0)
                elif (zx == self.x) and (zy == self.y):
                    dcfurs.set_pixel(x, y, 0xff)
                else:
                    dcfurs.set_pixel(x, y, 0)

    def draw(self):
        ## Check for a win condition
        if (self.z[self.y][self.x] == MAZE_FINISH):
            if not self.wincount:
                emote.render("^.^")
                return
            else:
                self.wincount -= 1
        ## Automatically solve the maze
        elif self.autosolve:
            if (self.counter & 3) == 3:
                ## Move once every 4 ticks.
                dx,dy = dirxy(self.z[self.y][self.x], magnitude=1)
                self.x += dx
                self.y += dy
        ## Let the user solve it with the accelerometer.
        elif ((self.counter & 1) == 0):
            ## Read and translate the accelerometer orientation
            ax = -badge.imu.y()
            ay = badge.imu.x()

            ## Move the cursor if a sufficiently assertive tilt is detected.        
            if (ax*ax + ay*ay) > 75:
                dx, dy = (0,0)
                if (ax > 4):
                    dx = 1
                elif (ax < -4):
                    dx = -1
                if (ay > 4):
                    dy = 1
                elif (ay < -4):
                    dy = -1
                
                ## Prefer movement along the X-axis
                if (abs(ax) > abs(ay)):
                    if (self.z[self.y][self.x + dx] != MAZE_WALL):
                        self.x += dx
                    elif (self.z[self.y + dy][self.x] != MAZE_WALL):
                        self.y += dy
                ## Prefer movement on the Y-axis
                else:
                    if (self.z[self.y + dy][self.x] != MAZE_WALL):
                        self.y += dy
                    elif (self.z[self.y][self.x + dx] != MAZE_WALL):
                        self.x += dx
        
        ## Redraw
        self.counter += 1
        self.blink = not self.blink
        self.render(self.x - 3, self.y - 3)

    def printmap(self):
        for row in self.z:
            print(row)
