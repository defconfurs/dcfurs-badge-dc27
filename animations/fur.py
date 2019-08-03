"""Furry Face Simulator 
Use:  http://liquidthex.com/dcfursBadgePixelator/
Features:
  * Will randomly blink every 10 - 20 seconds if no large-scale movements happen (winks)
  * Will track eyes with small nudges in up / down, left / right tilts
  * Will wink left/right if tilted too far
  * Will close eyes if held upside down
  * Will close eyes when shaken
"""

import dcfurs
import badge
import random

class fur:
  interval = 45 
  ticks_per_sec = int(1000 / interval)
  last_blink = 0
  next_blink = 0
  stop_blink = 0

  def __init__(self):
    self.counter = 0
#  darkblue = 00000001 = 01
#  blue =     00011111 = 1F
#             11111111 = 3F
#             00000101 = 05
#  pink =     11100011 = E3
#             00100001 = 21
#             11100000 = E0
    self.foregrounds = [None] * 6
    self.backgrounds = [None] * 6
    self.foreground_dims = [None] * 6
    self.rows=18
    self.columns=7
    self.foregrounds[0] = 0xFF
    self.foreground_dims[0] = 0x03
    self.backgrounds[0] = 0x0
    self.foregrounds[1] = 0xFF
    self.foreground_dims[1] = 0xE0
    self.backgrounds[1] = 0x0
    self.foregrounds[2] = 0x1F
    self.foreground_dims[2] = 0xE3
    self.backgrounds[2] = 0x0
    self.foregrounds[3] = 0xE3
    self.foreground_dims[3] = 0x1F
    self.backgrounds[3] = 0x0
    self.foregrounds[4] = 0xE3
    self.foreground_dims[4] = 0x21
    self.backgrounds[4] = 0x1F
    self.foregrounds[5] = 0x1F
    self.foreground_dims[5] = 0x05
    self.backgrounds[5] = 0xE3
    self.colorIndex = 0
    self.reset_fbuf()
    self.colorizeFaces()
    self.next_blink = random.randint(self.ticks_per_sec * 10, self.ticks_per_sec * 20)

  def boop(self):
    self.colorIndex += 1
    if self.colorIndex >= len(self.foregrounds):
      self.colorIndex = 0
    self.colorizeFaces()
#    if self.colorIndex >= len(self.foregrounds):
#      self.colorIndex = len(self.foregrounds) - 1
#      r = randrange(0, 128)
#      g = randrange(0, 128)
#      b = randrange(0, 128)
#      darkr = 32 + r if 32 + r < 255 else 255
#      darkg = 32 + g if 32 + g < 255 else 255
#      darkb = 32 + b if 32 + b < 255 else 255
#      midr = 64 + r if 64 + r < 255 else 255
#      midg = 64 + g if 64 + g < 255 else 255
#      midb = 64 + b if 64 + b < 255 else 255
#      brightr = 128 + r if 128 + r < 255 else 255
#      brightg = 128 + g if 128 + g < 255 else 255
#      brightb = 128 + b if 128 + b < 255 else 255
#      self.superdark[len(self.superdark) - 1] = self.mkColor(r, g, b)
#      self.dark[len(self.superdark) - 1] = self.mkColor(darkr, darkg, darkb)
#      self.mid[len(self.superdark) - 1] = self.mkColor(midr, midg, midb)
#      self.bright[len(self.superdark) - 1] = self.mkColor(brightr, brightg, brightb)
    
  def colorizeFaces(self):
    foreground = self.foregrounds[self.colorIndex]
    foreground_dim = self.foreground_dims[self.colorIndex]
    self.winkRightFace = [[1,13,foreground],[1,14,foreground],[1,15,foreground],[2,12,foreground],[2,13,foreground_dim],[2,14,foreground_dim],[2,15,foreground],[2,16,foreground],[3,2,foreground],[3,3,foreground],[3,4,foreground],[3,11,foreground],[3,14,foreground_dim],[3,15,foreground],[3,16,foreground],[4,1,foreground],[4,5,foreground],[4,11,foreground],[4,12,foreground],[4,14,foreground_dim],[4,15,foreground],[4,16,foreground],[5,12,foreground],[5,13,foreground],[5,14,foreground],[5,15,foreground]]
    self.winkLeftFace = [[1,2,foreground],[1,3,foreground],[1,4,foreground],[2,1,foreground],[2,2,foreground],[2,3,foreground_dim],[2,4,foreground_dim],[2,5,foreground],[3,1,foreground],[3,2,foreground],[3,3,foreground_dim],[3,5,foreground],[3,6,foreground],[3,13,foreground],[3,14,foreground],[3,15,foreground],[4,1,foreground],[4,2,foreground],[4,3,foreground_dim],[4,6,foreground],[4,12,foreground],[4,16,foreground],[5,2,foreground],[5,3,foreground],[5,4,foreground],[5,5,foreground]]
    self.winkUpperRightFace = [[1,13,foreground],[1,15,foreground],[2,12,foreground],[2,13,foreground_dim],[2,16,foreground],[3,2,foreground],[3,3,foreground],[3,4,foreground],[3,11,foreground],[3,12,foreground],[3,13,foreground_dim],[3,14,foreground_dim],[3,15,foreground_dim],[3,16,foreground],[4,1,foreground],[4,5,foreground],[4,11,foreground],[4,12,foreground],[4,13,foreground],[4,14,foreground],[4,15,foreground],[4,16,foreground],[5,12,foreground],[5,13,foreground],[5,14,foreground],[5,15,foreground]]
    self.winkUpperLeftFace = [[1,2,foreground],[1,3,foreground],[1,4,foreground],[2,1,foreground],[2,4,foreground_dim],[2,5,foreground],[3,1,foreground],[3,3,foreground],[3,4,foreground_dim],[3,5,foreground],[3,6,foreground],[3,13,foreground],[3,14,foreground],[3,15,foreground],[4,1,foreground],[4,2,foreground],[4,3,foreground],[4,4,foreground],[4,5,foreground],[4,6,foreground],[4,12,foreground],[4,16,foreground],[5,2,foreground],[5,3,foreground],[5,4,foreground],[5,5,foreground]]
    self.winkLowerLeftFace = [[1,2,foreground],[1,3,foreground],[1,4,foreground],[2,1,foreground],[2,2,foreground],[2,3,foreground],[2,4,foreground],[2,5,foreground],[3,1,foreground],[3,2,foreground_dim],[3,3,foreground_dim],[3,4,foreground_dim],[3,5,foreground],[3,6,foreground],[3,13,foreground],[3,14,foreground],[3,15,foreground],[4,1,foreground],[4,4,foreground_dim],[4,5,foreground],[4,6,foreground],[4,12,foreground],[4,16,foreground],[5,3,foreground],[5,4,foreground],[5,5,foreground]]
    self.winkLowerRightFace = [[1,13,foreground],[1,14,foreground],[1,15,foreground],[2,12,foreground],[2,13,foreground],[2,14,foreground],[2,15,foreground],[2,16,foreground],[3,2,foreground],[3,3,foreground],[3,4,foreground],[3,11,foreground],[3,12,foreground],[3,13,foreground_dim],[3,14,foreground_dim],[3,15,foreground_dim],[3,16,foreground],[4,1,foreground],[4,5,foreground],[4,11,foreground],[4,12,foreground],[4,13,foreground_dim],[4,16,foreground],[5,12,foreground],[5,13,foreground],[5,15,foreground]]
    self.standardFace = [[1,2,foreground],[1,3,foreground],[1,4,foreground],[1,13,foreground],[1,14,foreground],[1,15,foreground],[2,1,foreground],[2,2,foreground_dim],[2,3,foreground_dim],[2,4,foreground_dim],[2,5,foreground],[2,12,foreground],[2,13,foreground_dim],[2,14,foreground_dim],[2,15,foreground_dim],[2,16,foreground],[3,1,foreground],[3,2,foreground_dim],[3,5,foreground],[3,6,foreground],[3,11,foreground],[3,12,foreground],[3,15,foreground_dim],[3,16,foreground],[4,1,foreground],[4,2,foreground_dim],[4,4,foreground],[4,5,foreground],[4,6,foreground],[4,11,foreground],[4,12,foreground],[4,13,foreground],[4,15,foreground_dim],[4,16,foreground],[5,2,foreground],[5,3,foreground],[5,4,foreground],[5,5,foreground],[5,12,foreground],[5,13,foreground],[5,14,foreground],[5,15,foreground]]
    self.upperRightFace = [[1,2,foreground],[1,3,foreground],[1,4,foreground],[1,13,foreground],[1,14,foreground],[1,15,foreground],[2,1,foreground],[2,2,foreground],[2,3,foreground_dim],[2,5,foreground],[2,12,foreground],[2,13,foreground_dim],[2,15,foreground],[2,16,foreground],[3,1,foreground],[3,2,foreground],[3,3,foreground_dim],[3,6,foreground],[3,11,foreground],[3,12,foreground],[3,13,foreground_dim],[3,16,foreground],[4,1,foreground],[4,2,foreground],[4,3,foreground_dim],[4,4,foreground_dim],[4,5,foreground_dim],[4,6,foreground],[4,11,foreground],[4,12,foreground],[4,13,foreground_dim],[4,14,foreground_dim],[4,15,foreground_dim],[4,16,foreground],[5,2,foreground],[5,3,foreground],[5,4,foreground],[5,5,foreground],[5,12,foreground],[5,13,foreground],[5,14,foreground],[5,15,foreground]]
    self.upperLeftFace = [[1,2,foreground],[1,3,foreground],[1,4,foreground],[1,13,foreground],[1,14,foreground],[1,15,foreground],[2,1,foreground],[2,2,foreground],[2,4,foreground_dim],[2,5,foreground],[2,12,foreground],[2,13,foreground],[2,15,foreground_dim],[2,16,foreground],[3,1,foreground],[3,4,foreground_dim],[3,5,foreground],[3,6,foreground],[3,11,foreground],[3,12,foreground],[3,15,foreground_dim],[3,16,foreground],[4,1,foreground],[4,2,foreground_dim],[4,3,foreground_dim],[4,4,foreground_dim],[4,5,foreground],[4,6,foreground],[4,11,foreground],[4,12,foreground],[4,13,foreground_dim],[4,14,foreground_dim],[4,15,foreground_dim],[4,16,foreground],[5,2,foreground],[5,3,foreground],[5,4,foreground],[5,5,foreground],[5,12,foreground],[5,13,foreground],[5,14,foreground],[5,15,foreground]]
    self.rightFace = [[1,2,foreground],[1,3,foreground],[1,4,foreground],[1,13,foreground],[1,14,foreground],[1,15,foreground],[2,1,foreground],[2,2,foreground],[2,3,foreground_dim],[2,4,foreground_dim],[2,5,foreground],[2,12,foreground],[2,13,foreground_dim],[2,14,foreground_dim],[2,15,foreground],[2,16,foreground],[3,1,foreground],[3,2,foreground],[3,3,foreground_dim],[3,5,foreground],[3,6,foreground],[3,11,foreground],[3,12,foreground],[3,13,foreground_dim],[3,15,foreground],[3,16,foreground],[4,1,foreground],[4,2,foreground],[4,3,foreground_dim],[4,6,foreground],[4,11,foreground],[4,12,foreground],[4,13,foreground_dim],[4,16,foreground],[5,2,foreground],[5,3,foreground],[5,4,foreground],[5,5,foreground],[5,12,foreground],[5,13,foreground],[5,14,foreground],[5,15,foreground]]
    self.leftFace = [[1,2,foreground],[1,3,foreground],[1,4,foreground],[1,13,foreground],[1,14,foreground],[1,15,foreground],[2,1,foreground],[2,2,foreground],[2,3,foreground_dim],[2,4,foreground_dim],[2,5,foreground],[2,12,foreground],[2,13,foreground_dim],[2,14,foreground_dim],[2,15,foreground],[2,16,foreground],[3,1,foreground],[3,4,foreground_dim],[3,5,foreground],[3,6,foreground],[3,11,foreground],[3,14,foreground_dim],[3,15,foreground],[3,16,foreground],[4,1,foreground],[4,2,foreground],[4,4,foreground_dim],[4,5,foreground],[4,6,foreground],[4,11,foreground],[4,12,foreground],[4,14,foreground_dim],[4,15,foreground],[4,16,foreground],[5,2,foreground],[5,3,foreground],[5,4,foreground],[5,5,foreground],[5,12,foreground],[5,13,foreground],[5,14,foreground],[5,15,foreground]]
    self.lowerRightFace = [[1,2,foreground],[1,3,foreground],[1,4,foreground],[1,13,foreground],[1,14,foreground],[1,15,foreground],[2,1,foreground],[2,2,foreground],[2,3,foreground],[2,4,foreground],[2,5,foreground],[2,12,foreground],[2,13,foreground],[2,14,foreground],[2,15,foreground],[2,16,foreground],[3,1,foreground],[3,2,foreground],[3,3,foreground_dim],[3,4,foreground_dim],[3,5,foreground_dim],[3,6,foreground],[3,11,foreground],[3,12,foreground],[3,13,foreground_dim],[3,14,foreground_dim],[3,15,foreground_dim],[3,16,foreground],[4,1,foreground],[4,2,foreground],[4,3,foreground_dim],[4,6,foreground],[4,11,foreground],[4,12,foreground],[4,13,foreground_dim],[4,16,foreground],[5,2,foreground],[5,3,foreground],[5,5,foreground],[5,12,foreground],[5,13,foreground],[5,15,foreground]]
    self.lowerLeftFace = [[1,2,foreground],[1,3,foreground],[1,4,foreground],[1,13,foreground],[1,14,foreground],[1,15,foreground],[2,1,foreground],[2,2,foreground],[2,3,foreground],[2,4,foreground],[2,5,foreground],[2,12,foreground],[2,13,foreground],[2,14,foreground],[2,15,foreground],[2,16,foreground],[3,1,foreground],[3,2,foreground_dim],[3,3,foreground_dim],[3,4,foreground_dim],[3,5,foreground],[3,6,foreground],[3,11,foreground],[3,12,foreground_dim],[3,13,foreground_dim],[3,14,foreground_dim],[3,15,foreground],[3,16,foreground],[4,1,foreground],[4,4,foreground_dim],[4,5,foreground],[4,6,foreground],[4,11,foreground],[4,14,foreground_dim],[4,15,foreground],[4,16,foreground],[5,2,foreground],[5,4,foreground_dim],[5,5,foreground],[5,12,foreground],[5,14,foreground_dim],[5,15,foreground]]
    self.upperFace = [[1,2,foreground],[1,3,foreground],[1,14,foreground],[1,15,foreground],[2,1,foreground],[2,2,foreground_dim],[2,5,foreground],[2,12,foreground],[2,15,foreground_dim],[2,16,foreground],[3,1,foreground],[3,2,foreground_dim],[3,3,foreground_dim],[3,4,foreground_dim],[3,5,foreground],[3,6,foreground],[3,11,foreground],[3,12,foreground],[3,13,foreground_dim],[3,14,foreground_dim],[3,15,foreground_dim],[3,16,foreground],[4,1,foreground],[4,2,foreground],[4,3,foreground],[4,4,foreground],[4,5,foreground],[4,6,foreground],[4,11,foreground],[4,12,foreground],[4,13,foreground],[4,14,foreground],[4,15,foreground],[4,16,foreground],[5,2,foreground],[5,3,foreground],[5,4,foreground],[5,5,foreground],[5,12,foreground],[5,13,foreground],[5,14,foreground],[5,15,foreground]]
    self.lowerFace = [[1,2,foreground],[1,3,foreground],[1,4,foreground],[1,13,foreground],[1,14,foreground],[1,15,foreground],[2,1,foreground],[2,2,foreground],[2,3,foreground],[2,4,foreground],[2,5,foreground],[2,12,foreground],[2,13,foreground],[2,14,foreground],[2,15,foreground],[2,16,foreground],[3,1,foreground],[3,2,foreground_dim],[3,3,foreground_dim],[3,4,foreground_dim],[3,5,foreground_dim],[3,6,foreground],[3,11,foreground],[3,12,foreground_dim],[3,13,foreground_dim],[3,14,foreground_dim],[3,15,foreground_dim],[3,16,foreground],[4,1,foreground],[4,2,foreground_dim],[4,5,foreground_dim],[4,6,foreground],[4,11,foreground],[4,12,foreground_dim],[4,15,foreground_dim],[4,16,foreground],[5,2,foreground],[5,4,foreground],[5,5,foreground],[5,12,foreground],[5,13,foreground],[5,15,foreground]]
    self.blinkFace = [[3,2,foreground],[3,3,foreground],[3,4,foreground],[3,13,foreground],[3,14,foreground],[3,15,foreground],[4,1,foreground],[4,5,foreground],[4,12,foreground],[4,16,foreground]]
 
  def reset_fbuf(self):
    self.fbuf = [bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18)]

  def face(self):
    faceBuf = self.standardFace
    (tx, ty, tz) = badge.imu.filtered_xyz()
    self.reset_fbuf()
    move_y = 0
    move_x = 0
    if tz < -24:
      move_y = -1
    elif tz > 24:
      move_y = 1
    if ty < -24:
      move_x = 1
    elif ty > 24:
      move_x = -1
    if (badge.imu.read(0x3) & 0x80) != 0: # Shake event
      faceBuf = self.blinkFace
      self.stop_blink = random.randint(int(self.ticks_per_sec * .2), int(self.ticks_per_sec * .45))
    elif ty < -48:
      faceBuf = self.winkRightFace
      self.last_blink = 0
    elif ty > 48:
      faceBuf = self.winkLeftFace
      self.last_blink = 0
    elif tx < -48:
      faceBuf = self.blinkFace
      self.stop_blink = random.randint(int(self.ticks_per_sec * .2), int(self.ticks_per_sec * .45))
      self.last_blink = 0
    elif self.stop_blink > 0:
      self.stop_blink -= 1
      faceBuf = self.blinkFace
    elif self.last_blink > self.next_blink:
      faceBuf = self.blinkFace
      self.last_blink = 0
      self.stop_blink = random.randint(int(self.ticks_per_sec * .2), int(self.ticks_per_sec * .45))
      self.next_blink = random.randint(int(self.ticks_per_sec * 10), int(self.ticks_per_sec * 20))
    elif move_x == -1 and move_y == -1:
      faceBuf = self.lowerRightFace
    elif move_x == -1 and move_y == 0:
      faceBuf = self.rightFace
    elif move_x == -1 and move_y == 1:
      faceBuf = self.upperRightFace
    elif move_x == 0 and move_y == -1:
      faceBuf = self.lowerFace
    elif move_x == 0 and move_y == 0:
      faceBuf = self.standardFace
    elif move_x == 0 and move_y == 1:
      faceBuf = self.upperFace
    elif move_x == 1 and move_y == -1:
      faceBuf = self.lowerLeftFace
    elif move_x == 1 and move_y == 0:
      faceBuf = self.leftFace
    elif move_x == 1 and move_y == 1:
      faceBuf = self.upperLeftFace
    
    self.last_blink += 1

    for y in range(self.columns):
      for x in range(self.rows):
        mxy = [y, x, self.backgrounds[self.colorIndex]]
        self.onPixel(mxy)

    for xy in range(0,len(faceBuf)):
      self.onPixel(faceBuf[xy])

  def onPixel(self,xy):
    if len(xy) == 3:
      self.fbuf[xy[0]][xy[1]] = xy[2]
    else:
      self.fbuf[xy[0]][xy[1]] = 255

  def draw(self):
    self.face()
    dcfurs.set_frame(self.fbuf)
