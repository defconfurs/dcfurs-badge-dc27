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
    self.initGrid()

  def checkButtons(self):
    (tx, ty, tz) = badge.imu.filtered_xyz()
    if self.last_glider_left == 0 and ty < -40: # Tilt Left
      self.addGlider(1, 1)
      self.last_glider_left = 18
    elif self.last_glider_right == 0 and ty > 40: # Tilt Right
      self.addReverseGlider(self.rows-1, self.columns-1)
      self.last_glider_right = 18

  def draw(self):
    self.checkButtons()
    dcfurs.clear()
    for i in range(self.rows):
      for j in range(self.columns):
        if self.grid[i][j] == 1:
          dcfurs.set_pixel(i,j,255)
    self.update()

  def initGrid(self):
    self.grid = [[0 for col in range(self.columns)] for row in range(self.rows)]
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
