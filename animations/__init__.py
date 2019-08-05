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
from animations.dj import dj
from animations.northernlights import northernlights
from animations.fireworks import fireworks
from animations.hyperspace import hyperspace
from animations.dcylon import dcylon
from animations.throb import throb 
from animations.strobe import strobe 
from animations.sparkle import sparkle

## Dynamically import all the python files we can find.
import os
import sys
import ujson
import badge
import dcfurs

## Template class for JSON-encoded animations
class __jsonanim__:
    # XTerm color palette
    xterm = [
        0x00,   # black
        0x80,   # maroon
        0x10,   # green
        0x90,   # olive
        0x02,   # navy
        0x82,   # purple
        0x12,   # teal
        0xdb,   # silver
        0x92,   # grey
        0xe0,   # red
        0x1c,   # lime
        0xfc,   # yellow
        0x03,   # blue
        0xe3,   # fuschia
        0x1f,   # aqua
        0xff,   # white
    ]

    # Monochrome gamma intensity mapping
    intensity = [
        0, 2, 3, 4, 6, 9, 12, 17, 24, 34, 47, 66, 92, 130, 182, 255
    ]

    def __init__(self):
        try:
            fh = open(self.path, "r")
            self.framenum = 0
            self.js = ujson.load(fh)
            fh.close()
        except MemoryError as e:
            print("Caught a MemoryError while trying to load {}".format(self.path))
            self.js = [{"interval":"750","frame":"0ff0000f000f000000:f00f0f0f0000f00000:f0000000f0000f0000:f0000000f000f00000:f00f0f000f0f000000:0ff00000000000ffff:000000000000000000"},{"interval":"750","frame":"0ff0000f000f000000:f00f0f0f0000f00000:f0000000f0000f0000:f0000000f000f00000:f00f0f000f0f000000:0ff000000000000000:000000000000000000"}]

        self.color = badge.hue2rgb(int(rand() * 360))
        self.draw()

    def drawframe(self, frame):
        self.interval = int(frame['interval'])
        x = 0
        y = 0

        # Handle monochrome and legacy animations
        if 'frame' in frame:
            # Generate the animation color mapping.
            colormap = [0]*16
            c_red   = (self.color & 0xff0000) >> 16
            c_green = (self.color & 0x00ff00) >> 8
            c_blue  = (self.color & 0x0000ff) >> 0
            for i in range(0,16):
                p_red   = c_red * self.intensity[i] >> 8
                p_green = c_green * self.intensity[i] >> 8
                p_blue  = c_blue * self.intensity[i] >> 8
                colormap[i] = (p_red << 16) + (p_green << 8) + p_blue
            
            # Set the pixel values.
            data = frame['frame']
            for ch in data:
                if ch == ':':
                    x = 0
                    y = y+1
                else:
                    dcfurs.set_pix_rgb(x, y, colormap[int(ch, 16)])
                    x = x+1
        # Handle 8-bit RGB data
        elif 'rgb' in frame:
            pix = 0
            even = True
            data = frame['rgb']
            for ch in data:
                if ch == ':':
                    x = 0
                    y = y+1
                elif even:
                    even = False
                    pix = int(ch, 16) << 4
                else:
                    even = True
                    pix += int(ch, 16)
                    dcfurs.set_pixel(x,y,pix)
                    x = x+1
        # Handle 4-bit palette data
        elif 'palette' in frame:
            data = frame['palette']
            for ch in data:
                if ch == ':':
                    x = 0
                    y = y+1
                else:
                    dcfurs.set_pixel(x,y,self.xterm[int(ch, 16)])
                    x = x+1
        # Otherwise, we couldn't make sense of it.
        else:
            dcfurs.clear()

    def draw(self):
        self.drawframe(self.js[self.framenum])
        self.framenum = (self.framenum + 1) % len(self.js)

## Dynamically load/generate animation classes.
files = os.listdir("/flash/animations")
for filename in files:
    if filename[:2] == "__":
        continue
    
    # Files ending in .json can be parsed into static animations.
    if filename[-5:] == ".json":
        print("Loading JSON animation from " + filename)
        classname = filename[:-5]
        globals()[classname] = type(classname, (__jsonanim__,), {'path': "/flash/animations/" + filename})
    
    # Files ending in .py should contain scripted animations.
    if filename[-3:] == ".py":
        classname = filename[:-3]
        try:
            print("Loading scripted animation from " + filename)
            mod = __import__("animations." + classname, globals(), locals(), (classname))
            globals()[classname] = getattr(mod, classname)
        finally:
            pass

## Return a list of all animation classes
def all():
    results = []
    module = sys.modules['animations']
    for name in dir(module):
        x = getattr(module, name)
        if isinstance(x, type) and name[:2] != "__":
            results.append(x)
    return results
