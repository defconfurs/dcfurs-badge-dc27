## DranoTheCat's DJ Mode
##
##

from random import randrange,randint
import emote
import dcfurs
import badge
import utime

class dj:
  def __init__(self):
    dcfurs.clear()
    self.interval=10
    self.rows=18
    self.columns=7
    self.throb_x = 9
    self.throb_y = 2
    self.strobeAngle = 0
    self.pinkAngle = 300
    self.blueAngle = 180
    self.lastBeat = 0
    self.clearNext = False
    self.ticksPerBeat = 800
    self.boops = [0] * 4
    self.lastBoop = 0
    self.boopIndex = 0
    self.djMode = 0
    self.djMaxMode = 4
    self.djDuration = 25000
    self.lastTiltTimeout = 20
    self.lastCircleColor = 0
    self.djTicks = utime.ticks_add(utime.ticks_ms(), self.djDuration)
    self.nextBoopTimeout = 1500
    self.initGrid()

  def checkButtons(self):
    # Disabled for now
    return
    (tx, ty, tz) = badge.imu.filtered_xyz()
    if ty > 90: # Tilt Left
      print("DJ Mode: Previous Mode")
      self.lastTiltTimeout = 200
      self.initGrid()
      self.djTicks = utime.ticks_add(utime.ticks_ms(), self.djDuration)
      self.djMode -= 1
      if self.djMode < 0:
        self.djMode = self.djMaxMode
    elif ty < -90: # Tilt Right
      print("DJ Mode: Next Mode")
      self.lastTiltTimeout = 200
      self.initGrid()
      self.djTicks = utime.ticks_add(utime.ticks_ms(), self.djDuration)
      self.djMode += 1
      if self.djMode > self.djMaxMode:
        self.djMode = 1

  def draw(self):
    drawTime = utime.ticks_ms()
#    if utime.ticks_diff(drawTime, self.lastBeat) > self.ticksPerBeat:
#      print("DEBUG BEAT: {} lastBeat: {}".format(utime.ticks_diff(drawTime, self.lastBeat), self.lastBeat))
    if self.lastTiltTimeout > 0:
      self.lastTiltTimeout -= 1
    else:
      self.checkButtons()
    if drawTime > self.djTicks:
#      self.initGrid()
      self.djTicks = utime.ticks_add(utime.ticks_ms(), self.djDuration)
      self.djMode += 1
      if self.djMode > self.djMaxMode:
        self.djMode = 0
    # Process boops first
    if self.boopIndex > 0:
      # Do we have four boops?
      # If so, NOW should be the next downbeat
      if self.boops[3] > 0:
        # We have our 4 samples; let's average deltas and set the new internvalsPerBeat
        d1 = utime.ticks_diff(self.boops[1], self.boops[0])
        d2 = utime.ticks_diff(self.boops[2], self.boops[1])
        d3 = utime.ticks_diff(self.boops[3], self.boops[2])
        print("DJ MODE: Changing ticksPerBeat. Old: {} New: {} d1: {} d2: {} d3: {}".format(self.ticksPerBeat, int((d1 + d2 + d3) / 3), d1, d2, d3))
        self.ticksPerBeat = int((d1 + d2 + d3) / 3) # We tap slow?
        self.lastBeat = 0
        self.boops = [0] * 4
        self.boopIndex = 0
        self.lastBoop = 0
      else: # OK; we don't have 4 boops. But has our window expired?
        if self.boopIndex > 0:
            if utime.ticks_diff(drawTime, self.boops[self.boopIndex - 1]) > self.nextBoopTimeout:
              # Yup; expired. Do we have 1, 2, or 3 boops?
              if self.boopIndex == 3:
                # Increase the speed by 5 ticks
                print("DJ MODE: Increasing speed by 5 ticks.  Old: {} New: {}".format(self.ticksPerBeat, self.ticksPerBeat - 5)) 
                self.ticksPerBeat -= 5
                self.boops = [0] * 4
                self.boopIndex = 0
                self.lastBoop = 0
              elif self.boopIndex == 2:
                # Decrease the speed by 5 ticks
                print("DJ MODE: Decreasing speed by 5 ticks.  Old: {} New: {}".format(self.ticksPerBeat, self.ticksPerBeat + 5)) 
                self.ticksPerBeat += 5
                self.boops = [0] * 4
                self.boopIndex = 0
                self.lastBoop = 0
              elif self.boopIndex == 1:
                # Just set the downbeat
                print("DJ Mode: Downbeat!")
                self.lastBeat = self.boops[0]
                self.boops = [0] * 4
                self.boopIndex = 0
                self.lastBoop = 0
                
    angle = 0
    brightness = 0
    if self.djMode == 1: # Dots!
      if utime.ticks_diff(drawTime, self.lastBeat) > self.ticksPerBeat * 2:
        self.beatIteration = 0
        if self.lastBeat > 0:
          self.lastBeat = utime.ticks_add(self.lastBeat, 2*self.ticksPerBeat)
        else:
          self.lastBeat = drawTime
        ri = randint(0, 2)
        if ri == 0:
          self.angleGrid = [[-1 for col in range(self.columns)] for row in range(self.rows)]
        elif ri == 1:
          self.angleGrid = [[self.pinkAngle for col in range(self.columns)] for row in range(self.rows)]
        elif ri == 2:
          self.angleGrid = [[self.blueAngle for col in range(self.columns)] for row in range(self.rows)]
        self.brightnessGrid = [[255 for col in range(self.columns)] for row in range(self.rows)]
      else:
        for y in range(self.columns):
          for x in range(self.rows):
            if self.brightnessGrid[x][y] == -1:
              self.brightnessGrid[x][y] = 255
            self.brightnessGrid[x][y] -= 64
            if self.brightnessGrid[x][y] < 0:
              self.brightnessGrid[x][y] = 0
        rx = randint(0, self.rows - 1)
        ry = randint(0, self.columns - 1)
        for i in range(5):
          angle = self.pinkAngle
          if randint(0, 1) == 0:
            angle = self.blueAngle
          self.angleGrid[rx][ry] = angle
          self.brightnessGrid[rx][ry] = randint(0, 255)
    elif self.djMode == 0: # Strobe a color, halftime
      self.angleGrid = [[self.strobeAngle for col in range(self.columns)] for row in range(self.rows)]
      self.strobeAngle += 1
      if self.strobeAngle > 360:
        self.strobeAngle = 0
      if utime.ticks_diff(drawTime, self.lastBeat) > 2*self.ticksPerBeat:
        # On the beat, we want our strobe to be the brightest
        self.beatIteration = 0
        if self.lastBeat > 0:
          self.lastBeat = utime.ticks_add(self.lastBeat, 2*self.ticksPerBeat)
        else:
          self.lastBeat = drawTime
        self.brightnessGrid = [[255 for col in range(self.columns)] for row in range(self.rows)]
      else:
        pctThruBeat = utime.ticks_diff(drawTime, self.lastBeat) / (2*self.ticksPerBeat)
        brightness = 0
        if pctThruBeat > .5:
          brightness = int(pctThruBeat * 255)
        else:
          brightness = int(255 - (2*pctThruBeat * 255))
        self.brightnessGrid = [[brightness for col in range(self.columns)] for row in range(self.rows)]
    elif self.djMode == 4: # Circles Fade In
      if utime.ticks_diff(drawTime, self.lastBeat) > self.ticksPerBeat:
        # On the beat, Draw circles
        rr5 = 10*10
        rr4 = 6*6
        rr3 = 4*4
        rr2 = 2*2
        if self.lastCircleColor == 1:
          self.lastCircleColor = 0
        else:
          self.lastCircleColor = 1
        angle = self.pinkAngle
        if self.lastCircleColor == 1:
          angle = self.blueAngle
        for y in range(self.columns):
          ydist = y - self.throb_y + randint(-2, 2)
          if ydist < 0:
            ydist = 0 - ydist
          yy = ydist*ydist
          for x in range(self.rows):
            xdist = x - self.throb_x + randint(-2, 2)
            if xdist < 0:
              xdist = 0 - xdist
            xx = xdist*xdist
            pctThruBeat = utime.ticks_diff(drawTime, self.lastBeat) / self.ticksPerBeat
            maxBright = int(255 * pctThruBeat)
            penMaxBright = int(.5 * maxBright)
            midBright = int(.25 * maxBright)
            subMidBright = int(.05 * maxBright)
            self.angleGrid[x][y] = angle
            if xx + yy <= rr2:
              self.brightnessGrid[x][y] = maxBright
            elif xx + yy <= rr3:
              self.brightnessGrid[x][y] = penMaxBright
            elif xx + yy <= rr4:
              self.brightnessGrid[x][y] = midBright
            else:
              self.brightnessGrid[x][y] = subMidBright
        self.beatIteration = 0
        if self.lastBeat > 0:
          self.lastBeat = utime.ticks_add(self.lastBeat, self.ticksPerBeat)
        else:
          self.lastBeat = drawTime
      else:
        for y in range(self.columns):
          for x in range(self.rows):
            self.brightnessGrid[x][y] -= 4
    elif self.djMode == 3: # Pink and blue star field
      if utime.ticks_diff(drawTime, self.lastBeat) > self.ticksPerBeat:
        # On the beat, draw stars
        self.beatIteration = 0
        if self.lastBeat > 0:
          self.lastBeat = utime.ticks_add(self.lastBeat, self.ticksPerBeat)
        else:
          self.lastBeat = drawTime
        for y in range(self.columns):
          for x in range(self.rows):
            self.brightnessGrid[x][y] -= 4
        angle = self.pinkAngle
        if randint(0, 1) == 0:
          angle = self.blueAngle
        for y in range(self.columns):
          for x in range(self.rows):
            if randint(0, 3) == 0:
              self.brightnessGrid[x][y] = 255
              self.angleGrid[x][y] = angle
      else:
        for y in range(self.columns):
          for x in range(self.rows):
            if self.brightnessGrid[x][y] > 0:
              self.brightnessGrid[x][y] -= 8 
    elif self.djMode == 2: # Draw pink and blue lines
      if utime.ticks_diff(drawTime, self.lastBeat) > (self.ticksPerBeat / 8):
        # On the beat, draw a new line
        self.beatIteration = 0
        if self.lastBeat > 0:
          self.lastBeat = utime.ticks_add(self.lastBeat, int(self.ticksPerBeat / 8))
        else:
          self.lastBeat = drawTime
#        if randint(0, 5) == 0:
#          self.initGrid()
        if randint(0, 1) == 0: # Let's do a row
          y = randint(0, self.columns - 1)
          if self.angleGrid[5][y] == self.pinkAngle:
            for x in range(self.rows):
              self.angleGrid[x][y] = self.blueAngle
              self.brightnessGrid[x][y] = 255
          elif self.angleGrid[5][y] == self.blueAngle:
            for x in range(self.rows):
              self.angleGrid[x][y] = self.pinkAngle
              self.brightnessGrid[x][y] = 255
          else:
            if randint(0, 1) == 0:
              for x in range(self.rows):
                self.angleGrid[x][y] = self.pinkAngle
                self.brightnessGrid[x][y] = 255
            else:
              for x in range(self.rows):
                self.angleGrid[x][y] = self.blueAngle
                self.brightnessGrid[x][y] = 255
        else:
          x = randint(0, self.rows - 1)
          if self.angleGrid[x][3] == self.pinkAngle:
            for y in range(self.columns):
              self.angleGrid[x][y] = self.blueAngle
              self.brightnessGrid[x][y] = 255
          elif self.angleGrid[x][3] == self.blueAngle:
            for y in range(self.columns):
              self.angleGrid[x][y] = self.pinkAngle
              self.brightnessGrid[x][y] = 255
          else:
            if randint(0, 1) == 0:
              for y in range(self.columns):
                self.angleGrid[x][y] = self.pinkAngle
                self.brightnessGrid[x][y] = 255
            else:
              for y in range(self.columns):
                self.angleGrid[x][y] = self.blueAngle
                self.brightnessGrid[x][y] = 255
      else:
        for y in range(self.columns):
          for x in range(self.rows):
            if self.brightnessGrid[x][y] > 16:
              self.brightnessGrid[x][y] -= 16 

    for y in range(self.columns):
      for x in range(self.rows):
        if self.angleGrid[x][y] == -1:
          dcfurs.set_pixel(x, y, 0xff)
        else:
          dcfurs.set_pix_hue(x, y, self.angleGrid[x][y], self.brightnessGrid[x][y])

  def initGrid(self):
    self.angleGrid = [[0 for col in range(self.columns)] for row in range(self.rows)]
    self.brightnessGrid = [[0 for col in range(self.columns)] for row in range(self.rows)]

  def boop(self):
    if self.boopIndex < len(self.boops):
      self.boops[self.boopIndex] = utime.ticks_ms()
      self.boopIndex += 1
