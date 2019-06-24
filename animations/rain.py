## Matrix-esque Rain Animation
import dcfurs
import random

class rain:
    def __init__(self):
        self.fbuf = [bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18)]
        self.lastrand = len(self.fbuf[0])
        self.interval = 150
        self.counter = 0

    def rain_fall(self):
        ## For each pixel in the buffer:
        y = len(self.fbuf)-1
        while y >= 0:
            row = self.fbuf[y]
            for x in range(0,len(row)):
                px = row[x]
                if ((px >= 255) and (y < (len(self.fbuf)-1))):
                    self.fbuf[y+1][x] = px
                row[x] = px >> 2
            y -= 1
        ## Redraw the display
        for y in range(0,len(self.fbuf)):
            row = self.fbuf[y]
            for x in range(0, len(row)):
                dcfurs.set_pixel(x, y, row[x])

    def rain_newdrop(self):
        ## Pick a random column and insert a new raindrop
        self.lastrand += random.randint(1, len(self.fbuf[0])-1)
        self.lastrand %= len(self.fbuf[0])
        self.fbuf[0][self.lastrand] = 255

    def draw(self):
        self.rain_fall()
        if (self.counter % 3) == 0:
            self.rain_newdrop()
        self.counter += 1
