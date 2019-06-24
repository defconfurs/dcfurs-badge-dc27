## Conway's Game of Life
import dcfurs
import random

class life:
    def __init__(self):
        self.fbuf = [bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18)]
        self.interval = 750
        self.watchdog = 0
        dcfurs.clear()

        ## populate the initial state of the game
        for y in range(0,len(self.fbuf)):
            row = self.fbuf[y]
            for x in range(0, len(row)):
                if random.randint(0, 2) == 0:
                    row[x] = 255
                    dcfurs.set_pixel(x, y, row[x])
    
    ## Check if a given cell is alive
    def alive(self, x, y):
        ## Wrap around to simulate an infinite field
        if x < 0:
            x += dcfurs.ncols
        if y < 0:
            y += dcfurs.nrows
        ## Return 1 if the cell is alive, and zero otherwise
        row = self.fbuf[y % dcfurs.nrows]
        if row[x % dcfurs.ncols] == 255:
            return 1
        else:
            return 0

    ## Count the neighbors of a cell
    def neighbors(self, col, row):
        count = -self.alive(col, row)
        for x in range(col-1, col+2):
            for y in range(row-1, row+2):
                if self.alive(x, y):
                    count += 1
        return count

    ## Run a tick of the animation
    def draw(self):
        ## Compute the next tick and draw it to the screen
        next = [bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18)]
        delta = 0
        for y in range(0,len(self.fbuf)):
            row = next[y]
            for x in range(0, len(row)):
                count = self.neighbors(x, y)
                if self.alive(x, y):
                    if count == 2 or count == 3:
                        row[x] = 255
                    else:
                        delta += 1
                        row[x] = 8
                else:
                    if count == 3 or count == 6:
                        delta += 1
                        row[x] = 255
                dcfurs.set_pixel(x, y, row[x])

        ## Save the game state
        self.fbuf = next

        ## The game can sometimes reach a stable configuration (or die), so
        ## restart the game if the activity drops too low for more than 5
        ## ticks.
        if delta > 4:
            self.watchdog = 0
        elif self.watchdog > 5:
            self.__init__()
        else:
            self.watchdog = self.watchdog + 1
