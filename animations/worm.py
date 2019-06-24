## Wormy animation
import dcfurs
import badge
import random

class worm:
  interval = 5
  x = 1
  y = 1

  def __init__(self):
    self.fbuf = [bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18)]
    self.counter = 0

  def updatePosition(self):
    self.dimPixels()
    (tx, ty, tz) = badge.imu.filtered_xyz()
    new_x = 0
    new_y = 0                        # NOTE:  X and Y mean different things to ty and friends, than x and friends.  Yeah....
    if tx < -70 and self.y > 1:      # We basically have the badge upside down
      new_y -= 1
      if random.randint(0, 1) == 1:  # Fidget X
        new_x += 1
    elif ty < -8 and self.x > 1:    # If we tilt it left or right, (or if it's already at the top because we're upside down)
      if random.randint(0, 1) == 1:  # We only want to obey this kind of tilt half the time, otherwise let's fidget Y
        new_x += 1
      else:
        new_y = random.randint(-1, 1) 
    elif ty > 8 and self.x < 17:    # Tilting other way, same as above
      if random.randint(0, 1) == 1:
        new_x -= 1
      else:
        new_y = random.randint(-1, 1)
    else:                            # Otherwise let's basically just move randomly
      move_x = random.randint(0, 1)
      if move_x:
        new_x = random.randint(-1, 1)
      else:
        new_y = random.randint(-1, 1)
    if (dcfurs.has_pixel(self.x + new_x, self.y + new_y)):
      self.x += new_x
      self.y += new_y
    else: # Always move.  This could lead to recursive crash if this method is programmed poorly :)
      self.updatePosition()
    self.setPixel(self.x, self.y, 255)

  def dimPixels(self):
    for y in range(0,len(self.fbuf)):
      row = self.fbuf[y]
      for x in range(0, len(row)):
        if self.fbuf[y][x] > 16:
          self.fbuf[y][x] -= 8
          if self.fbuf[y][x] > 128:
            self.fbuf[y][x] -= 8
        else:
          self.fbuf[y][x] = 0
 
  def setPixel(self, x, y, value):
    self.fbuf[y][x] = value 
  
  def draw(self):
    self.updatePosition()
    dcfurs.set_frame(self.fbuf)
