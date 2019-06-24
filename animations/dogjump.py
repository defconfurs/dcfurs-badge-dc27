'''
    Author: ioncann0ns

    DEF CON Furs Badge Script: Dog Jump Game
'''

import pyb
import dcfurs
import badge
import micropython
import settings
import ubinascii

game_brightness = 5
dead_brightness = 100

class dogjump:
	def __init__(self):
		print("Time to play Dog Jump!")
		self.obstacles = list()
		self.dog = [(2, 4), (4, 4), (2, 3), (3, 3), (4, 3), (4, 2), (5, 2), (2, 2), (4, 1)]
		self.obstacle = [(17, 4), (17, 3)]
		self.jumping = False
		self.waiting = True
		self.score = 0
		self.interval = 80
		self.falling = False

	def draw(self):
		# refresh
		dcfurs.clear()
		# draw score
		draw_score(self.score)
		# draw floor
		create_floor()
		# draw dog
		draw_entity(self.dog)

		# reset to the regular interval
		self.interval = 80

		# jump handling
		# mid-jump
		if self.jumping:
			# ceiling hit: stop jumping, start falling
			if self.dog[8][1] <= -3:
				self.jumping = False
				self.falling = True
			# going up
			else:
				dog_move(self.dog, 1)
		# dog gravity
		elif self.falling:
			# floor hit: stop falling
			if self.dog[0][1] >= 4:
				self.falling = False
			# going down
			else:
				dog_move(self.dog, -1)

		# obstacle handling
		# create obstacle
		if not self.waiting:
			self.score = obstacle_move(self.obstacle, self.score)
		# draw obstacle
		draw_entity(self.obstacle)

		# check for collision
		for point in self.obstacle:
			for check in self.dog:
				if point[0] == check[0]:
					if point[1] == check[1]:
						dcfurs.set_pixel(point[0], point[1], dead_brightness)
						self.obstacles = list()
						self.dog = [(2, 4), (4, 4), (2, 3), (3, 3), (4, 3), (4, 2), (5, 2), (2, 2), (4, 1)]
						self.obstacle = [(17, 4), (17, 3)]
						self.jumping = False
						self.waiting = True
						self.interval = 1000
						self.falling = False

	def boop(self):
		# dog jump
		if not self.falling:
			# first jump
			if self.waiting:
				self.score = 0
				self.waiting = False
				self.interval = 80
			# start jumping
			else:
				self.interval = 10
				self.jumping = True

def draw_entity(entity):
	for point in entity:
		if point[1] > 0:
			dcfurs.set_pixel(point[0], point[1], game_brightness)


def dog_move(dog, diff):
	for point in range(len(dog)):
		dog[point] = (dog[point][0], dog[point][1]-diff)


def obstacle_move(obstacle, score):
	if settings.debug:
		print("Obstacle: {},{}".format(obstacle[0][0], obstacle[0][1]))
	if obstacle[0][0] <= 0:
		for point in range(len(obstacle)):
			obstacle[point] = (17, obstacle[point][1])
		score += 1
		print("Score: {}".format(score))
	else:
		for point in range(len(obstacle)):
			obstacle[point] = (obstacle[point][0]-1, obstacle[point][1])
	return score


def draw_score(score):
	score_str = "{0:b}".format(score)
	start = (dcfurs.ncols - len(score_str)) - 1
	for i in range(len(score_str)):
		if score_str[i] == '1':
			dcfurs.set_pixel(start+i, 0, game_brightness)


def create_floor():
	for point in range(18):
		dcfurs.set_pixel(point, 5, game_brightness)

