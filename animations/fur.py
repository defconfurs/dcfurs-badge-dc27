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
  dimmer = 16
  winkRightFace = [[1,13],[1,14],[1,15],[2,12],[2,13,dimmer],[2,14,dimmer],[2,15],[2,16],[3,2],[3,3],[3,4],[3,11],[3,14,dimmer],[3,15],[3,16],[4,1],[4,5],[4,11],[4,12],[4,14,dimmer],[4,15],[4,16],[5,12],[5,13],[5,14],[5,15]]
  winkLeftFace = [[1,2],[1,3],[1,4],[2,1],[2,2],[2,3,dimmer],[2,4,dimmer],[2,5],[3,1],[3,2],[3,3,dimmer],[3,5],[3,6],[3,13],[3,14],[3,15],[4,1],[4,2],[4,3,dimmer],[4,6],[4,12],[4,16],[5,2],[5,3],[5,4],[5,5]]
  winkUpperRightFace = [[1,13],[1,15],[2,12],[2,13,dimmer],[2,16],[3,2],[3,3],[3,4],[3,11],[3,12],[3,13,dimmer],[3,14,dimmer],[3,15,dimmer],[3,16],[4,1],[4,5],[4,11],[4,12],[4,13],[4,14],[4,15],[4,16],[5,12],[5,13],[5,14],[5,15]]
  winkUpperLeftFace = [[1,2],[1,3],[1,4],[2,1],[2,4,dimmer],[2,5],[3,1],[3,3],[3,4,dimmer],[3,5],[3,6],[3,13],[3,14],[3,15],[4,1],[4,2],[4,3],[4,4],[4,5],[4,6],[4,12],[4,16],[5,2],[5,3],[5,4],[5,5]]
  winkLowerLeftFace = [[1,2],[1,3],[1,4],[2,1],[2,2],[2,3],[2,4],[2,5],[3,1],[3,2,dimmer],[3,3,dimmer],[3,4,dimmer],[3,5],[3,6],[3,13],[3,14],[3,15],[4,1],[4,4,dimmer],[4,5],[4,6],[4,12],[4,16],[5,3],[5,4],[5,5]]
  winkLowerRightFace = [[1,13],[1,14],[1,15],[2,12],[2,13],[2,14],[2,15],[2,16],[3,2],[3,3],[3,4],[3,11],[3,12],[3,13,dimmer],[3,14,dimmer],[3,15,dimmer],[3,16],[4,1],[4,5],[4,11],[4,12],[4,13,dimmer],[4,16],[5,12],[5,13],[5,15]]
  standardFace = [[1,2],[1,3],[1,4],[1,13],[1,14],[1,15],[2,1],[2,2,dimmer],[2,3,dimmer],[2,4,dimmer],[2,5],[2,12],[2,13,dimmer],[2,14,dimmer],[2,15,dimmer],[2,16],[3,1],[3,2,dimmer],[3,5],[3,6],[3,11],[3,12],[3,15,dimmer],[3,16],[4,1],[4,2,dimmer],[4,4],[4,5],[4,6],[4,11],[4,12],[4,13],[4,15,dimmer],[4,16],[5,2],[5,3],[5,4],[5,5],[5,12],[5,13],[5,14],[5,15]]
  upperRightFace = [[1,2],[1,3],[1,4],[1,13],[1,14],[1,15],[2,1],[2,2],[2,3,dimmer],[2,5],[2,12],[2,13,dimmer],[2,15],[2,16],[3,1],[3,2],[3,3,dimmer],[3,6],[3,11],[3,12],[3,13,dimmer],[3,16],[4,1],[4,2],[4,3,dimmer],[4,4,dimmer],[4,5,dimmer],[4,6],[4,11],[4,12],[4,13,dimmer],[4,14,dimmer],[4,15,dimmer],[4,16],[5,2],[5,3],[5,4],[5,5],[5,12],[5,13],[5,14],[5,15]]
  upperLeftFace = [[1,2],[1,3],[1,4],[1,13],[1,14],[1,15],[2,1],[2,2],[2,4,dimmer],[2,5],[2,12],[2,13],[2,15,dimmer],[2,16],[3,1],[3,4,dimmer],[3,5],[3,6],[3,11],[3,12],[3,15,dimmer],[3,16],[4,1],[4,2,dimmer],[4,3,dimmer],[4,4,dimmer],[4,5],[4,6],[4,11],[4,12],[4,13,dimmer],[4,14,dimmer],[4,15,dimmer],[4,16],[5,2],[5,3],[5,4],[5,5],[5,12],[5,13],[5,14],[5,15]]
  rightFace = [[1,2],[1,3],[1,4],[1,13],[1,14],[1,15],[2,1],[2,2],[2,3,dimmer],[2,4,dimmer],[2,5],[2,12],[2,13,dimmer],[2,14,dimmer],[2,15],[2,16],[3,1],[3,2],[3,3,dimmer],[3,5],[3,6],[3,11],[3,12],[3,13,dimmer],[3,15],[3,16],[4,1],[4,2],[4,3,dimmer],[4,6],[4,11],[4,12],[4,13,dimmer],[4,16],[5,2],[5,3],[5,4],[5,5],[5,12],[5,13],[5,14],[5,15]]
  leftFace = [[1,2],[1,3],[1,4],[1,13],[1,14],[1,15],[2,1],[2,2],[2,3,dimmer],[2,4,dimmer],[2,5],[2,12],[2,13,dimmer],[2,14,dimmer],[2,15],[2,16],[3,1],[3,4,dimmer],[3,5],[3,6],[3,11],[3,14,dimmer],[3,15],[3,16],[4,1],[4,2],[4,4,dimmer],[4,5],[4,6],[4,11],[4,12],[4,14,dimmer],[4,15],[4,16],[5,2],[5,3],[5,4],[5,5],[5,12],[5,13],[5,14],[5,15]]
  lowerRightFace = [[1,2],[1,3],[1,4],[1,13],[1,14],[1,15],[2,1],[2,2],[2,3],[2,4],[2,5],[2,12],[2,13],[2,14],[2,15],[2,16],[3,1],[3,2],[3,3,dimmer],[3,4,dimmer],[3,5,dimmer],[3,6],[3,11],[3,12],[3,13,dimmer],[3,14,dimmer],[3,15,dimmer],[3,16],[4,1],[4,2],[4,3,dimmer],[4,6],[4,11],[4,12],[4,13,dimmer],[4,16],[5,2],[5,3],[5,5],[5,12],[5,13],[5,15]]
  lowerLeftFace = [[1,2],[1,3],[1,4],[1,13],[1,14],[1,15],[2,1],[2,2],[2,3],[2,4],[2,5],[2,12],[2,13],[2,14],[2,15],[2,16],[3,1],[3,2,dimmer],[3,3,dimmer],[3,4,dimmer],[3,5],[3,6],[3,11],[3,12,dimmer],[3,13,dimmer],[3,14,dimmer],[3,15],[3,16],[4,1],[4,4,dimmer],[4,5],[4,6],[4,11],[4,14,dimmer],[4,15],[4,16],[5,2],[5,4,dimmer],[5,5],[5,12],[5,14,dimmer],[5,15]]
  upperFace = [[1,2],[1,3],[1,14],[1,15],[2,1],[2,2,dimmer],[2,5],[2,12],[2,15,dimmer],[2,16],[3,1],[3,2,dimmer],[3,3,dimmer],[3,4,dimmer],[3,5],[3,6],[3,11],[3,12],[3,13,dimmer],[3,14,dimmer],[3,15,dimmer],[3,16],[4,1],[4,2],[4,3],[4,4],[4,5],[4,6],[4,11],[4,12],[4,13],[4,14],[4,15],[4,16],[5,2],[5,3],[5,4],[5,5],[5,12],[5,13],[5,14],[5,15]]
  lowerFace = [[1,2],[1,3],[1,4],[1,13],[1,14],[1,15],[2,1],[2,2],[2,3],[2,4],[2,5],[2,12],[2,13],[2,14],[2,15],[2,16],[3,1],[3,2,dimmer],[3,3,dimmer],[3,4,dimmer],[3,5,dimmer],[3,6],[3,11],[3,12,dimmer],[3,13,dimmer],[3,14,dimmer],[3,15,dimmer],[3,16],[4,1],[4,2,dimmer],[4,5,dimmer],[4,6],[4,11],[4,12,dimmer],[4,15,dimmer],[4,16],[5,2],[5,4],[5,5],[5,12],[5,13],[5,15]]
  blinkFace = [[3,2],[3,3],[3,4],[3,13],[3,14],[3,15],[4,1],[4,5],[4,12],[4,16]]
  last_blink = 0
  next_blink = 0
  stop_blink = 0

  def __init__(self):
    self.reset_fbuf()
    self.counter = 0
    self.next_blink = random.randint(self.ticks_per_sec * 10, self.ticks_per_sec * 20)

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
