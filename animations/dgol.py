## DranoTheCat's Glider Battle
## (using Conway's Game of Life Rules)
##
## Tilt badge left to start a new glider from the right
## tilt badge right to start a new glider from the left

import random
import dcfurs
import badge

class dgol:
  last_glider_left=3
  last_glider_right=3
  def __init__(self):
    self.interval=75
    self.rows=18
    self.columns=7
    self.heatcolors = [None] * 31
    self.heatcolors[0] = 0
    self.heatcolors[1] = self.mkColor(16, 0, 0)
    self.heatcolors[2] = self.mkColor(32, 0, 0)
    self.heatcolors[3] = self.mkColor(48, 0, 0)
    self.heatcolors[4] = self.mkColor(64, 0, 0)
    self.heatcolors[5] = self.mkColor(80, 0, 0)
    self.heatcolors[6] = self.mkColor(96, 0, 0)
    self.heatcolors[7] = self.mkColor(112, 0, 0)
    self.heatcolors[8] = self.mkColor(128, 0, 0)
    self.heatcolors[9] = self.mkColor(144, 0, 0)
    self.heatcolors[10] = self.mkColor(160, 0, 0)
    self.heatcolors[11] = self.mkColor(176, 0, 0)
    self.heatcolors[12] = self.mkColor(192, 0, 0)
    self.heatcolors[13] = self.mkColor(208, 0, 0)
    self.heatcolors[14] = self.mkColor(224, 0, 0)
    self.heatcolors[15] = self.mkColor(255, 0, 0)
    self.heatcolors[16] = self.mkColor(255, 0, 16)
    self.heatcolors[17] = self.mkColor(255, 0, 32)
    self.heatcolors[18] = self.mkColor(255, 0, 48)
    self.heatcolors[19] = self.mkColor(255, 0, 64)
    self.heatcolors[20] = self.mkColor(255, 0, 80)
    self.heatcolors[21] = self.mkColor(255, 0, 96)
    self.heatcolors[22] = self.mkColor(255, 0, 112)
    self.heatcolors[23] = self.mkColor(255, 0, 128)
    self.heatcolors[24] = self.mkColor(255, 0, 144)
    self.heatcolors[25] = self.mkColor(255, 0, 160)
    self.heatcolors[26] = self.mkColor(255, 0, 176)
    self.heatcolors[27] = self.mkColor(255, 0, 192)
    self.heatcolors[28] = self.mkColor(255, 0, 208)
    self.heatcolors[29] = self.mkColor(255, 0, 224)
    self.heatcolors[30] = self.mkColor(255, 0, 255)
    self.nblue = self.mkColor(0, 255, 255)
    self.colors = [None] * 20
    self.colors[0] = 0
    self.colors[1] = self.mkColor(0, 128, 128)
    self.colors[2] = self.mkColor(0, 144, 144)
    self.colors[3] = self.mkColor(0, 160, 160)
    self.colors[4] = self.mkColor(0, 176, 176)
    self.colors[5] = self.mkColor(0, 192, 192)
    self.colors[6] = self.mkColor(0, 208, 208)
    self.colors[7] = self.mkColor(0, 224, 224)
    self.colors[8] = self.mkColor(0, 240, 240)
    self.colors[9] = self.mkColor(0, 255, 255)
    self.colors[10] = self.mkColor(0, 128, 128)
    self.colors[11] = self.mkColor(0, 144, 144)
    self.colors[12] = self.mkColor(0, 160, 160)
    self.colors[13] = self.mkColor(0, 176, 176)
    self.colors[14] = self.mkColor(0, 192, 192)
    self.colors[15] = self.mkColor(0, 208, 208)
    self.colors[16] = self.mkColor(0, 224, 224)
    self.colors[17] = self.mkColor(0, 240, 240)
    self.colors[18] = self.mkColor(0, 255, 255)
    self.colors[19] = self.mkColor(255, 255, 255)
    self.initGrid()

  def checkButtons(self):
    (tx, ty, tz) = badge.imu.filtered_xyz()
    if self.last_glider_left == 0 and ty < -40: # Tilt Left
      self.addGlider(1, 1)
      self.last_glider_left = 18
    elif self.last_glider_right == 0 and ty > 40: # Tilt Right
      self.addReverseGlider(self.rows-1, self.columns-1)
      self.last_glider_right = 18

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

  def draw(self):
    self.checkButtons()
#    dcfurs.clear()
    for i in range(self.rows):
      for j in range(self.columns):
        if self.grid[i][j] == 1:
          self.heatmap[i][j] += 1
          if self.heatmap[i][j] > 19:
            self.heatmap[i][j] = 19
          dcfurs.set_pix_rgb(i, j, self.nblue)
        else:
          if self.heatmap[i][j] > 0:
            dcfurs.set_pix_rgb(i, j, self.heatcolors[self.heatmap[i][j]])
    self.update()

  def initGrid(self):
    self.grid = [[0 for col in range(self.columns)] for row in range(self.rows)]
    self.heatmap = [[1 for col in range(self.columns)] for row in range(self.rows)]
    self.addGlider(1, 1)
    return self.grid

  def fixColumns(self, j):
    if j < 0:
      j = self.columns + j
    elif j >= self.columns:
      j = 0 + j % self.columns
    return j

  def fixRows(self, i):
    if i < 0:
      i = self.rows + i
    elif i >= self.rows:
      i = 0 + i % self.rows
    return i

  def setGrid(self, i, j, value):
    i = self.fixRows(i)
    j = self.fixColumns(j)
    self.grid[i][j] = value

  def getGrid(self, i, j):
    i = self.fixRows(i)
    j = self.fixColumns(j)
    return self.grid[i][j]

  def addReverseGlider(self, i, j):
    self.setGrid(i, j, 0)
    self.setGrid(i, j-1, 0)
    self.setGrid(i, j-2, 1)
    self.setGrid(i-1, j, 1)
    self.setGrid(i-1, j-1, 0)
    self.setGrid(i-1, j-2, 1)
    self.setGrid(i-2, j, 0)
    self.setGrid(i-2, j-1, 1)
    self.setGrid(i-2, j-2, 1)

  def addGlider(self, i, j):
    self.setGrid(i, j, 0)
    self.setGrid(i, j+1, 0)
    self.setGrid(i, j+2, 1)
    self.setGrid(i+1, j, 1)
    self.setGrid(i+1, j+1, 0)
    self.setGrid(i+1, j+2, 1)
    self.setGrid(i+2, j, 0)
    self.setGrid(i+2, j+1, 1)
    self.setGrid(i+2, j+2, 1)

  def update(self):
    self.last_glider_left -= 1 if self.last_glider_left > 0 else 0
    self.last_glider_right -= 1 if self.last_glider_right > 0 else 0
    newGrid = [row[:] for row in self.grid]
    for i in range(0,self.rows):
      for j in range(0,self.columns):
        # using toroidal boundary conditions - x and y wrap around
        # so that the simulaton takes place on a toroidal surface.
        # j,i == x
        # | a | b | c |
        # | d | x | e |
        # | f | g | h |
        a = self.getGrid(i-1, j-1)
        b = self.getGrid(i-1, j)
        c = self.getGrid(i-1, j+1)
        d = self.getGrid(i, j-1)
        e = self.getGrid(i, j+1)
        f = self.getGrid(i+1, j-1)
        g = self.getGrid(i+1, j)
        h = self.getGrid(i+1, j+1)
        total = a+b+c+d+e+f+g+h

        # apply Conway's rules
        if self.grid[i][j] == 1:
          if (total < 2) or (total > 3):
            newGrid[i][j] = 0
        else:
          if total == 3:
            newGrid[i][j] = 1
    self.grid[:] = newGrid[:]
