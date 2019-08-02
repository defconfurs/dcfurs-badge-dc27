## DranoTheCat's Pink and Blue fireworks
##
## Tilt badge left to make lights move to the left
## Tilt badge right to make lights move to the right
## Boop to change speed -- meh, this effect sucked so disabled
##

from random import randrange
import math
import dcfurs
import badge
import utime

### TESTS FOR PC
#from os import system

# Each rainbowLight object keeps track of its own settings
class rainbowLight:
  def __init__(self, x, y, r, l):
    self.x = x
    self.y = y
    self.r = r
    self.l = l
    if randrange(0, 2) >= 1:
      self.cr = randrange(200, 255)
      self.cg = randrange(0, 64)
      self.cb = randrange(200, 255)
    else:
      self.cr = randrange(0, 64)
      self.cg = randrange(200, 255)
      self.cb = randrange(200, 255)
    self.state = 'appear'


class fireworks:
  maxRadius = 2     # Maximum radius for lights
  maxCycles = 12    # Maximum cycles lights will stay alive
  newDropPct = 90  # Percent chance each cycle for a new droplet to be created
  lights = []
  def __init__(self):
    self.interval=75
    self.ivals = [75, 150, 250, 500, 50]
    self.cval = 0
    self.rows=18
    self.columns=7
    self.initGrid()
    self.createLight()

#  def boop(self):
#    self.cval += 1
#    if self.cval >= len(self.ivals):
#      self.cval = 0
#    self.interval = self.ivals[self.cval]

  def checkButtons(self):
    (tx, ty, tz) = badge.imu.filtered_xyz()
    if ty < -40: # Tilt Right
      for light in self.lights:
        if light.x < self.rows:
          light.x += 1
        else:
          light.x = self.rows - 1
    elif ty > 40: # Tilt Left
      for light in self.lights:
        if light.x > 1:
          light.x -= 1
        else:
          light.x = 0

  # This method displays a quasi-grid for testing on a CLI
  def bogusDisplay(self):
    print("------------------------------------------------------------")
    for i in range(self.rows):
      for j in range(self.columns):
        a = hex(self.getGrid(i, j))
        print(a, " ", end="")
      print("")
    print("============================================================")

  def createLight(self):
    x = randrange(0, self.rows) 
    y = randrange(0, self.columns)
    r = randrange(1, self.maxRadius)
    l = randrange(3, self.maxCycles)
    self.lights.append(rainbowLight(x, y, r, l)) 

  def render(self, light):
    # Appearance effect:
    #   Draw circle at radius at min brightness
    #   Then decrement radius, increase brightness, and draw the new circle, until done
    # ThrobA effect:
    #    Draw final circle at r+1 at min brightness
    #    Find remainder brightness steps for rest of radius; ignore bottom brightness
    #    Draw circle at radius r/3 + 1 at next brightness level, then r/3 + n until min brightness
    #    Draw circle at radius r/3 at max brightness
    # throbB effect:  same as appearance
    # Vanish effect:
    #    1 - apperance
    #    2 - apperance but r -= 1
    #    3 - apperance but r -= 2
    #    ...
    #print("ID {} | State: {}".format(light.id, light.state))
    if light.state == 'appear':
      radius = light.r
      while (radius > 0):
        self.drawLight(light, radius, (light.r - radius + 1) / light.r)
        radius -= 3
      light.state = 'throbA'
    elif light.state == 'throbA':
      radius = light.r
      minBright = 1 / light.r
      self.drawLight(light, radius, minBright)
      radius -= 3
      while (radius > 0):
        bright = (light.r - radius + 1) / light.r
        if bright > 1:
          bright = 1
        if radius < light.r / 4:
          bright = 1
        self.drawLight(light, radius, bright)
        radius -= 3
      light.state = 'throbB'
    elif light.state == 'throbB':
      radius = light.r + 1
      while (radius > 0):
        self.drawLight(light, radius, (light.r - radius + 2) / light.r)
        radius -= 3
      c = self.mkColor(255, 255, 255)
      self.setGrid(light.x, light.y, c)
      light.state = 'throbA'
    elif light.state == 'vanish':
      #print("ID: {} | vanish! {}".format(light.id, light.r))
      radius = light.r
      while (radius > 0):
        self.drawLight(light, radius, (light.r - radius + 1) / (light.r + 0 - light.l))
        radius -= 3
      light.r -= 1
      light.l = 1
      light.state = 'throbB'

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

  def drawLight(self, light, radius, brightness):
    #print("drawLight brightness: {}".format(brightness))
  #  start = utime.ticks_ms()
    if brightness < 0.75 and brightness >= 0.35:
      brightness = 0.35
    elif brightness < 0.25 and brightness >= 0.1:
      brightness = 0.1
    cr = int(light.cr * brightness + 0.5)
    cg = int(light.cg * brightness + 0.5)
    cb = int(light.cb * brightness + 0.5)
    rr = radius * radius
    for x in range(light.x - radius, light.x + 1):
      ax = light.x - x
      axax = ax * ax
      for y in range(light.y - radius, light.y + 1):
        # Are we within the radius?
        ay = light.y - y
        ayay = ay * ay
        extra = 0
        if radius > 1:
          extra = 1
        if axax + ayay <= rr + extra:
          c = self.mkColor(cr, cg, cb)
          self.setGrid(x, y, c)
          self.setGrid(light.x + ax, y, c)
          self.setGrid(light.x + ax, light.y + ay, c)
          self.setGrid(x, light.y + ay, c)
  #  end = utime.ticks_ms()
  #  t = end - start
  #  print("drawLight of radius {} Done in {}".format(radius, t))

  def draw(self):
#    start = utime.ticks_ms()
#    print("start")
    self.checkButtons()
    self.update()
#    dcfurs.clear()
    for i in range(self.rows):
      for j in range(self.columns):
        dcfurs.set_pix_rgb(i, j, self.getGrid(i, j))
#    self.bogusDisplay()
    if randrange(0, 100) < self.newDropPct:
      self.createLight()
#    end = utime.ticks_ms()
#    t = end - start
#    print("done in {}".format(t))

  def initGrid(self):
    self.grid = [[0 for col in range(self.columns)] for row in range(self.rows)]
    return self.grid

  def fixColumns(self, j):
    if j < 0:
      j = 0
    elif j >= self.columns:
      j = self.columns - 1
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
    # If we already have a value, let's try to mix the colors...
#    if self.getGrid(i, j) > 0:
#      ec = self.getGrid(i, j)
#      cr = format(ec, '08b')[0:3]
#      cg = format(ec, '08b')[3:6]
#      cb = format(ec, '08b')[6:8]
#      dr = int(cr, 2)
#      dg = int(cg, 2)
#      db = int(cb, 2)
#      value = value
#      xr = format(value, '08b')[0:3]
#      xg = format(value, '08b')[3:6]
#      xb = format(value, '08b')[6:8]
#      yr = int(xr, 2)
#      yg = int(xg, 2)
#      yb = int(xb, 2)
#      nr = math.ceil((dr + yr) / 2)
#      ng = math.ceil((dg + yg) / 2)
#      nb = math.ceil((db + yb) / 2)
#      nv = self.mkColor(nr, ng, nb)
#      self.grid[i][j] = nv
#    else:
    self.grid[i][j] = value

  def getGrid(self, i, j):
    i = self.fixRows(i)
    j = self.fixColumns(j)
    return self.grid[i][j]

  def update(self):
    self.initGrid()
    if len(self.lights) < 1:
      self.createLight()
    for light in self.lights:
      light.l -= 1
      if light.l < 1:
        light.state = 'vanish'
      if light.r < 1:
        self.lights.remove(light)
      else:
        self.render(light)
