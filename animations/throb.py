## DranoTheCat's Evil Throb
##
## Boop to change colors?
##
##

from random import randrange,randint
import emote
import dcfurs
import badge
import utime

class throb:
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
    self.angle = 72
    self.iterations = 0
    self.boopLock = False
    self.moveDirection = True
    self.boopIndex = -1
    self.boopAngles = [360, 120, 300, 180]
    self.angleCycleIterations = 4
    self.boopEasterEggIndex = 0
    self.boopEasterEggMax = 25
    self.throb_x = self.center_x - 1
    self.throb_y = self.center_y - 1

  def move(self):
    if self.moveDirection:
      self.throb_x += 1
    else:
      self.throb_x -= 1

    ymove = randint(0, 8)
    if ymove == 3:
      self.throb_y -= 1
    elif ymove == 7:
      self.throb_y += 1

    if self.throb_x < 0:
      self.throb_x = 0
      self.moveDirection = True
    elif self.throb_x >= self.rows:
      self.throb_x = self.rows - 1
      self.moveDirection = False
    if self.throb_y < 0:
      self.throb_y = 0
    elif self.throb_y >= self.columns:
      self.throb_y = self.columns- 1


  def draw(self):
    rr5 = 7*7
    rr4 = 5*5
    rr3 = 3*3
    rr2 = 2*2
    self.iterations += 1
    if self.throbIncrease:
      self.throbStep += 1
      if self.throbStep > 60:
        self.throbStep = 60
        self.throbIncrease = False
    else:
      self.throbStep -= 1
      if self.throbStep < 0:
        self.throbStep = 0
        self.throbIncrease = True
    if self.boopEasterEggIndex >= self.boopEasterEggMax:
      self.boopEasterEggIndex = self.boopEasterEggMax
      self.move()
    if self.iterations % self.angleCycleIterations == 0:
      self.iterations = 0
      self.angle += 1
      if self.angle > 360:
        self.angle = 0
    if self.boopLock:
      self.angle = self.boopAngles[self.boopIndex]
    for y in range(self.columns):
      ydist = y - self.throb_y
      if ydist < 0:
        ydist = 0 - ydist
      yy = ydist*ydist
      for x in range(self.rows):
        xdist = x - self.throb_x
        if xdist < 0:
          xdist = 0 - xdist
        xx = xdist*xdist
        maxBright = 4 * self.throbStep
        if maxBright > 255:
          maxBright = 255
        penMaxBright = 3 * self.throbStep
        if penMaxBright > 255:
          penMaxBright = 255
        midBright = 2 * self.throbStep
        subMidBright = self.throbStep

        if xx + yy <= rr2:
          dcfurs.set_pix_hue(x, y, self.angle, 16 + maxBright)
        elif xx + yy <= rr3:
          dcfurs.set_pix_hue(x, y, self.angle, 16 + penMaxBright)
        elif xx + yy <= rr4:
          dcfurs.set_pix_hue(x, y, self.angle, 16 + midBright)
        elif xx + yy <= rr5:
          dcfurs.set_pix_hue(x, y, self.angle, 16 + subMidBright)
        else:
          dcfurs.set_pix_hue(x, y, self.angle, 16)
          
  def boop(self):
    self.boopLock = True
    self.boopIndex += 1
    self.boopEasterEggIndex += 1
    if self.boopIndex >= len(self.boopAngles):
      self.boopIndex = -1
      self.boopLock = False
