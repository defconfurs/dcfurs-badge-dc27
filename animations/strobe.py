## DranoTheCat's Evil Strobe
##
## Boop to change colors?
##
##

from random import randrange,randint
import emote
import dcfurs
import badge
import utime

class strobe:
  def __init__(self):
    dcfurs.clear()
    self.interval=15
    self.rows=18
    self.columns=7
    self.center_x = 9
    self.center_y = 3
    self.colorIndex = 0
    self.throbStep = 0
    self.throbIncrease = True
    self.angle = 360
    self.iterations = 0
    self.boopLock = False
    self.moveDirection = True
    self.boopIndex = 0
    self.boopAngles = [360, 120, 300, 180]
    self.angleCycleIterations = 4
    self.boopEasterEggIndex = 0
    self.boopEasterEggMax = 25
    self.throb_x = self.center_x - 1
    self.throb_y = self.center_y - 1
    self.evilPixels = [[0,2],[0,15],[0,16],[1,2],[1,3],[1,14],[1,15],[2,3],[2,4],[2,13],[2,14],[3,3],[3,4],[3,5],[3,12],[3,13],[3,14],[4,2],[4,3],[4,4],[4,5],[4,6],[4,11],[4,12],[4,13],[4,14],[4,15],[5,3],[5,6],[5,11],[5,14]]

  def draw(self):
    self.iterations += 1
    if self.throbIncrease:
      self.throbStep += 8
      if self.throbStep > 255:
        self.throbStep = 255
        self.throbIncrease = False
    else:
      self.throbStep -= 8
      if self.throbStep < 16:
        self.throbStep = 16 
        self.throbIncrease = True
    for y in range(self.columns):
      for x in range(self.rows):
        if self.evilPixel(x, y):
          dcfurs.set_pix_hue(x, y, self.angle, 0)
        else:
          dcfurs.set_pix_hue(x, y, self.angle, self.throbStep)

  def evilPixel(self, x, y):
    for pixel in self.evilPixels:
      if pixel[1] == x and pixel[0] == y:
        return True
    return False
    
  def boop(self):
    self.boopIndex += 1
    if self.boopIndex >= len(self.boopAngles):
      self.angle = randint(0, 360)
    else:
      self.angle = self.boopAngles[self.boopIndex]
