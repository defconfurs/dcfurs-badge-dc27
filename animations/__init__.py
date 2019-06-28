## Load the python animations
from animations.rainbow import rainbow
from animations.scroll import scroll
from animations.fur import fur
from animations.worm import worm
from animations.rain import rain
from animations.cylon import cylon
from animations.life import life
from animations.pong import pong
from animations.maze import maze
from animations.dgol import dgol
from animations.dogjump import dogjump

## Dynamically import all the python files we can find.
import os
import sys
import ujson
import dcfurs

## Template class for JSON-encoded animations
class __jsonanim__:
    def __init__(self):
        fh = open(self.path, "r")
        self.framenum = 0
        self.js = ujson.load(fh)
        self.intensity = bytearray([0, 2, 3, 4, 6, 9, 12, 17, 24, 34, 47, 66, 92, 130, 182, 255])
        fh.close()
        self.draw()

    def drawframe(self, frame):
        self.interval = int(frame['interval'])
        x = 0
        y = 0
        for ch in frame['frame']:
            if ch == ':':
                x = 0
                y = y+1
            else:
                dcfurs.set_pixel(x,y,self.intensity[int(ch, 16)])
                x = x+1

    def draw(self):
        self.drawframe(self.js[self.framenum])
        self.framenum = (self.framenum + 1) % len(self.js)

## Dynamically generate animation classes from JSON files.
files = os.listdir("/flash/animations")
for filename in files:
    if filename[:2] != "__" and filename[-5:] == ".json":
        classname = filename[:-5]
        globals()[classname] = type(classname, (__jsonanim__,), {'path': "/flash/animations/" + filename})


## Return a list of all animation classes
def all():
    results = []
    module = sys.modules['animations']
    for name in dir(module):
        x = getattr(module, name)
        if isinstance(x, type) and name[:2] != "__":
            results.append(x)
    return results
