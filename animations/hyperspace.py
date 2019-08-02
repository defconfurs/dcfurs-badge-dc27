## DranoTheCat's Hyperspace
##
## Tilt badge left to 
## Tilt badge right to 
## Boop to change speed
##

from random import randrange
#import math
import dcfurs
import badge
import utime

# Each starLight object keeps track of its own settings
class starLight:
  def __init__(self, x, y, center_x, center_y):
    self.colors = [None] * 6
    self.x = x
    self.y = y
    self.slopeTrackerX = 0
    self.slopeTrackerY = 0
    self.colors[0] = 0
    self.slope_x = x - center_x
    self.slope_y = y - center_y
    if randrange(0, 2) >= 1:
      self.colors[1] = self.mkColor(32, 0, 32)
      self.colors[2] = self.mkColor(64, 0, 64)
      self.colors[3] = self.mkColor(128, 0, 128)
      self.colors[4] = self.mkColor(255, 0, 255)
    else:
      self.colors[1] = self.mkColor(0, 32, 32)
      self.colors[2] = self.mkColor(0, 64, 64)
      self.colors[3] = self.mkColor(0, 128, 128)
      self.colors[4] = self.mkColor(0, 255, 255)
    self.colors[5] = self.mkColor(255, 255, 255)

  def move(self):
    self.changeSlopeX()

  def zfill(self, s, width):
    if len(s) < width:
        return ("0" * (width - len(s))) + s
    else:
        return s

  def mkColor(self, r, g, b):
    br = self.zfill(bin(r)[2:], 8)
    bg = self.zfill(bin(g)[2:], 8)
    bb = self.zfill(bin(b)[2:], 8)
#    print("Color Code: {}, {}, {}".format(br, bg, bb))
    return int(br + bg + bb, 2)

  def changeSlopeX(self):
    aslope = self.slope_x
    if aslope < 0:
      aslope = 0 - aslope
    if self.slopeTrackerX > aslope:
      if self.slope_y >= 0:
        self.y += 1
      else:
        self.y -= 1
      self.slopeTrackerX = 0
    else:
      if self.slope_x >= 0:
        self.x += 1
      else:
        self.x -= 1
    self.slopeTrackerX += 1
     
  def changeSlopeY(self):
    aslope = self.slope_y
    if aslope < 0:
      aslope = 0 - aslope
    if self.slopeTrackerY > aslope:
      if self.slope_y >= 0:
        self.y += 1
      else:
        self.y -= 1
      self.slopeTrackerY = 0
    self.slopeTrackerY += 1


class hyperspace:
  stars = []
  maxStarsPerCreate = 3
  starIteration = 0
  maxStarIteration = 1 
  def __init__(self):
    dcfurs.clear()
    self.interval=50
    self.ivals = [50, 100, 200, 500, 25]
    self.cval = 0
    self.rows=18
    self.columns=7
    self.center_x = 9
    self.center_y = 3
    self.initGrid()
    self.createStars()

  def boop(self):
    self.cval += 1
    if self.cval >= len(self.ivals):
      self.cval = 0
    self.interval = self.ivals[self.cval]

  def dimPixels(self):
    for y in range(0, self.columns):
      for x in range(0, self.rows):
        if self.grid[x][y] > 0:
          self.setGrid(x, y, self.grid[x][y] - 1)

  def checkButtons(self):
    (tx, ty, tz) = badge.imu.filtered_xyz()
    if ty < -40: # Tilt Right
      if self.center_x < self.rows:
        self.center_x += 1
      else:
        self.center_x = self.rows - 1
    elif ty > 40: # Tilt Left
      if self.center_x > 1:
        self.center_x -= 1
      else:
        self.center_x = 0
    else:
      self.center_x = 9
      self.center_y = 3

  def createStars(self):
    for i in (0, randrange(0, self.maxStarsPerCreate)):
      minX = self.center_x - 6
      maxX = self.center_x + 6
      if minX < 0:
        minX = 0
      if minX > self.rows:
        maxX = self.rows - 1
      minY = self.center_y - 2
      maxY = self.center_y + 2
      if minY < 0:
        minY = 0
      if maxY > self.columns:
        maxY = self.columns - 1
      x = randrange(minX, maxX)
      y = randrange(minY, maxY)
      self.stars.append(starLight(x, y, self.center_x, self.center_y)) 

  def draw(self):
    self.dimPixels()
    self.checkButtons()
    self.starIteration += 1
    if self.starIteration > self.maxStarIteration:
      self.createStars() 
      self.starIteration = 0
    for star in self.stars:
      star.move()
      self.setGrid(star.x, star.y, 5, star)
    for i in range(self.rows):
      for j in range(self.columns):
        if self.grid[i][j] > 0:
          colors = self.starGrid[i][j]
          dcfurs.set_pix_rgb(i, j, colors[self.grid[i][j]])
        else:
          dcfurs.set_pix_rgb(i, j, 0)

  def initGrid(self):
    self.grid = [[0 for col in range(self.columns)] for row in range(self.rows)]
    self.starGrid = [[[None]*6 for col in range(self.columns)] for row in range(self.rows)]

  def fixColumns(self, j, star):
    if j < 0:
      self.stars.remove(star)
      return 'x'
    elif j >= self.columns:
      self.stars.remove(star)
      return 'x'
    return j

  def fixRows(self, i, star):
    if i < 0:
      self.stars.remove(star)
      return 'x'
    elif i >= self.rows:
      self.stars.remove(star)
      return 'x'
    return i

  def getStarGrid(self, i, j):
    return self.starGrid[i][j]

  def setGrid(self, i, j, value, star = None):
    i = self.fixRows(i, star)
    j = self.fixColumns(j, star)
    if i == 'x' or j == 'x':
      return
    self.grid[i][j] = value
    if star is not None:
      self.starGrid[i][j] = star.colors.copy()
