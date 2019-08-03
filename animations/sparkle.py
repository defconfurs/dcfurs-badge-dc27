## DranoTheCat's Pretty Sparkle
##
##

from random import randrange,randint
import emote
import dcfurs
import badge
import utime

class sparkle:
  def __init__(self):
    dcfurs.clear()
    self.interval=60
    self.rows=18
    self.columns=7
    self.colorIndex = 0
    self.sparkleStep = 0
    self.sparkleIncrease = True
    self.pinkAngle = 300
    self.blueAngle = 180
    self.iterations = 0
    self.sparkleStep = 0
    self.whiteDuration = 5
    self.boopType = 0
    self.boopSwipe = False
    self.boopSwipeInterval = 0
    self.initGrid()

  def boopRow(self, x):
    if self.boopType == 0:
      self.grid[x][self.boopSwipeInterval] = 3
    elif self.boopType == 1:
      self.grid[x][self.boopSwipeInterval] = 0
    elif self.boopType == 2:
      self.grid[x][self.boopSwipeInterval] = 1
    elif self.boopType == 3:
      self.grid[x][self.boopSwipeInterval] = 2

  def boopColumn(self, y):
    if self.boopType == 0:
      self.grid[self.boopSwipeInterval][y] = 3
    elif self.boopType == 1:
      self.grid[self.boopSwipeInterval][y] = 0
    elif self.boopType == 2:
      self.grid[self.boopSwipeInterval][y] = 1
    elif self.boopType == 3:
      self.grid[self.boopSwipeInterval][y] = 2

  def draw(self):
    if self.boopSwipe:
      if self.boopDirection == 0:
        for x in range(self.rows):
          self.boopRow(x)
        self.boopSwipeInterval += 1
        if self.boopSwipeInterval >= self.columns:
          self.boopSwipeInterval = 0 
          self.boopSwipe = False
          self.interval=60
      elif self.boopDirection == 1:
        for x in range(self.rows):
          self.boopRow(x)
        self.boopSwipeInterval -= 1
        if self.boopSwipeInterval < 0:
          self.boopSwipeInterval = 0 
          self.boopSwipe = False
          self.interval=60
      elif self.boopDirection == 2:
        for y in range(self.columns):
          self.boopColumn(y)
        self.boopSwipeInterval += 1
        if self.boopSwipeInterval >= self.rows:
          self.boopSwipeInterval = 0 
          self.boopSwipe = False
          self.interval=60
      elif self.boopDirection == 3:
        for y in range(self.columns):
          self.boopColumn(y)
        self.boopSwipeInterval -= 1
        if self.boopSwipeInterval < 0:
          self.boopSwipeInterval = 0
          self.boopSwipe = False
          self.interval=60

    if self.sparkleIncrease:
      self.sparkleStep += 8
      if self.sparkleStep > 127:
        self.sparkleStep = 127
        self.sparkleIncrease = False

    else:
      self.sparkleStep -= 8
      if self.sparkleStep < 0:
        self.sparkleStep = 0 
        self.sparkleIncrease = True
    for y in range(self.columns):
      for x in range(self.rows):
        if self.grid[x][y] == 1:
          if randint(0, 2) == 0:
            if self.boopSwipe:
              dcfurs.set_pix_hue(x, y, self.pinkAngle, 255)
            else:
              dcfurs.set_pix_hue(x, y, self.pinkAngle, randint(64, 255))
        elif self.grid[x][y] == 2:
          if randint(0, 2) == 0:
            if self.boopSwipe:
              dcfurs.set_pix_hue(x, y, self.blueAngle, 255)
            else:
              dcfurs.set_pix_hue(x, y, self.blueAngle, randint(64, 255))
        elif self.grid[x][y] >= 3:
          dcfurs.set_pixel(x, y, 0xFF)
          self.grid[x][y] += 1
          if self.grid[x][y] > self.whiteDuration:
            if randint(0, 1) == 0:
              self.grid[x][y] = 1
            else:
              self.grid[x][y] = 2
        else:
          dcfurs.set_pix_hue(x, y, 0, 0)

    if not self.boopSwipe:
      rx = randint(0, self.rows - 1)
      ry = randint(0, self.columns - 1)
      self.grid[rx][ry] = 3


  def initGrid(self):
    self.grid = [[0 for col in range(self.columns)] for row in range(self.rows)]

  def evilPixel(self, x, y):
    for pixel in self.evilPixels:
      if pixel[1] == x and pixel[0] == y:
        return True
    return False
    
  def boop(self):
    if not self.boopSwipe:
      self.interval = 10
      self.boopType = randint(0, 3)
      self.boopSwipe = True
      self.boopDirection = randint(0, 3)
      if self.boopDirection == 0:
        self.boopSwipeInterval = 0 
      elif self.boopDirection == 1:
        self.boopSwipeInterval = self.columns - 1
      elif self.boopDirection == 2:
        self.boopSwipeInterval = 0
      elif self.boopDirection == 3:
        self.boopSwipeInterval = self.rows - 1
