## DranoTheCat's Cylon
##
## Boop to change colors
##
##

from random import randrange
import emote
import dcfurs
import badge
import utime

class dcylon:
  def __init__(self):
    dcfurs.clear()
    self.interval=20
    self.rows=18
    self.columns=7
    self.center_x = 9
    self.center_y = 3
    self.eye_radius = 3
    self.colorIndex = 0
    self.superdark = [None] * 6
    self.dark = [None] * 6
    self.mid = [None] * 6
    self.bright = [None] * 6
    self.superdark[0] = self.mkColor(32, 0, 0)
    self.dark[0] = self.mkColor(64, 0, 0)
    self.mid[0] = self.mkColor(128, 0, 0)
    self.bright[0] = self.mkColor(255, 0, 0)
    self.superdark[1] = self.mkColor(32, 0, 32)
    self.dark[1] = self.mkColor(64, 0, 64)
    self.mid[1] = self.mkColor(128, 0, 128)
    self.bright[1] = self.mkColor(255, 0, 255)
    self.superdark[2] = self.mkColor(0, 32, 32)
    self.dark[2] = self.mkColor(0, 64, 64)
    self.mid[2] = self.mkColor(0, 128, 128)
    self.bright[2] = self.mkColor(0, 255, 255)
    self.superdark[3] = self.mkColor(0, 32, 0)
    self.dark[3] = self.mkColor(0, 64, 0)
    self.mid[3] = self.mkColor(0, 128, 0)
    self.bright[3] = self.mkColor(0, 255, 0)
    self.superdark[4] = self.mkColor(0, 32, 32)
    self.dark[4] = self.mkColor(0, 64, 64)
    self.mid[4] = self.mkColor(0, 128, 128)
    self.bright[4] = self.mkColor(0, 255, 255)
    self.superdark[5] = self.mkColor(32, 0, 32)
    self.dark[5] = self.mkColor(64, 0, 64)
    self.mid[5] = self.mkColor(128, 0, 128)
    self.bright[5] = self.mkColor(255, 0, 255)
    self.initGrid()
    self.x = self.center_x
    self.y = self.center_y
    self.iteration = 0
    self.maxIteration = 1
    self.direction = True
    self.drawEye(self.x, self.y)

  def zfill(self, s, width):
    if len(s) < width:
        return ("0" * (width - len(s))) + s
    else:
        return s

  def mkColor(self, r, g, b):
    br = self.zfill(bin(r)[2:], 8)
    bg = self.zfill(bin(g)[2:], 8)
    bb = self.zfill(bin(b)[2:], 8)
    return int(br + bg + bb, 2)

  def drawEye(self, cx, cy):  
    radius = self.eye_radius
    rr = radius * radius
    self.initGrid()
    for x in range(cx - radius, cx + 1):
      ax = cx - x
      axax = ax * ax
      for y in range(cy - radius, cy + 1):
        ay = cy - y
        ayay = ay * ay
        if axax + ayay <= rr + 1:
          c = self.superdark[self.colorIndex]
          self.setGrid(x, y, c)
          self.setGrid(cx + ax, y, c)
          self.setGrid(cx + ax, cy + ay, c)
          self.setGrid(x, cy + ay, c)
        else:
          self.setGrid(x, y, 0)
          self.setGrid(cx + ax, y, 0)
          self.setGrid(cx + ax, cy + ay, 0)
          self.setGrid(x, cy + ay, 0)
    self.setGrid(cx + 1, cy, self.mid[self.colorIndex])
    self.setGrid(cx - 1, cy, self.mid[self.colorIndex])
    self.setGrid(cx + 1, cy + 1, self.mid[self.colorIndex])
    self.setGrid(cx - 1, cy - 1, self.mid[self.colorIndex])
    self.setGrid(cx, cy, self.bright[self.colorIndex])

  def boop(self):
    self.colorIndex += 1
    if self.colorIndex >= len(self.superdark):
      self.colorIndex = len(self.superdark) - 1
      r = randrange(0, 128)
      g = randrange(0, 128)
      b = randrange(0, 128)
      darkr = 32 + r if 32 + r < 255 else 255
      darkg = 32 + g if 32 + g < 255 else 255
      darkb = 32 + b if 32 + b < 255 else 255
      midr = 64 + r if 64 + r < 255 else 255
      midg = 64 + g if 64 + g < 255 else 255
      midb = 64 + b if 64 + b < 255 else 255
      brightr = 128 + r if 128 + r < 255 else 255
      brightg = 128 + g if 128 + g < 255 else 255
      brightb = 128 + b if 128 + b < 255 else 255
      self.superdark[len(self.superdark) - 1] = self.mkColor(r, g, b)
      self.dark[len(self.superdark) - 1] = self.mkColor(darkr, darkg, darkb)
      self.mid[len(self.superdark) - 1] = self.mkColor(midr, midg, midb)
      self.bright[len(self.superdark) - 1] = self.mkColor(brightr, brightg, brightb)
  
  def draw(self):
    self.iteration += 1
    if self.iteration <= self.maxIteration:
      return
    self.iteration = 0
    if self.x <= self.rows / 3:
      self.maxIteration = 4
    elif self.x >= 2 * (self.rows / 3):
      self.maxIteration = 4
    elif self.x <= self.rows / 5:
      self.maxIteration = 8
    elif self.x >= 4 * (self.rows / 5):
      self.maxIteration = 8
    else:
      self.maxIteration = 1
    if self.direction:
      self.x += 1
      if self.x >= self.rows:
        self.x = self.rows - 1
        self.direction = False
        self.maxIteration = 8
    else:
      self.x -= 1
      if self.x < 0:
        self.x = 0
        self.direction = True
        self.maxIteration = 8
    self.drawEye(self.x, self.y)
    for i in range(self.rows):
      for j in range(self.columns):
        if self.grid[i][j] > 0:
          dcfurs.set_pix_rgb(i, j, self.grid[i][j])
        else:
          dcfurs.set_pix_rgb(i, j, 0)

  def initGrid(self):
    self.grid = [[0 for col in range(self.columns)] for row in range(self.rows)]

  def setGrid(self, i, j, value, star = None):
    if i < 0 or j < 0 or i >= self.rows or j >= self.columns:
      return
    self.grid[i][j] = value
