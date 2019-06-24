## Pong animation
## The physics are not 100% true to the origional pong, and this is
## slightly more keen to make vertical reflections. However, that does
## tend to work better on the uber-wide aspect ratio of our display.
import dcfurs
import badge
import random

class pong:
    def __init__(self):
        self.interval = 150
        self.updown = 1
        self.leftright = 1
        self.bouncecount = 0
        while True:
            self.x = random.randint(0, dcfurs.ncols-1)
            self.y = random.randint(0, dcfurs.nrows-1)
            if dcfurs.has_pixel(self.x, self.y):
                break
    
    def bounce(self):
        nx = self.x + self.leftright
        ny = self.y + self.updown
        if dcfurs.has_pixel(nx, ny):
            return

        self.bouncecount += 1
        ## Try a vertical reflection
        if dcfurs.has_pixel(nx, self.y - self.updown):
            self.updown = -self.updown
        ## Try a horizontal reflection
        elif dcfurs.has_pixel(self.x - self.leftright, ny):
            self.leftright = -self.leftright
        ## Otherwise, come back from whence we came
        else:
            self.updown = -self.updown
            self.leftright = -self.leftright

    def draw(self):
        self.bounce()
        dcfurs.clear()
        dcfurs.set_pixel(self.x, self.y, 1)
        self.x += self.leftright
        self.y += self.updown
        dcfurs.set_pixel(self.x, self.y, 255)