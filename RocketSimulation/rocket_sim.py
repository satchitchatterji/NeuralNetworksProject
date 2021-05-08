
from processing_py import *
from random import uniform
from extras import Vector
from rocket import Rocket
from datetime import datetime

class Scene:
	def __init__(self, width, height):
		self.app = App(width, height)
		self.width = width
		self.height = height
		self.ground_height = 20
		self.rocket = None
		self.file_key = open("data_key.csv", 'a');

		self.gravity = Vector(0, 0.01)

		self.target_size = 100
		self.target_lims = (0, self.width-self.target_size)
		self.target_pos = uniform(*self.target_lims)
		self.target_center = Vector(self.target_pos, self.ground_height)

	def add_rocket(self, rocket):
		self.rocket = rocket

	def draw_background(self):
		self.app.background(0,0,0)

	def draw_ground(self, col=(33,179,47)):
		self.app.fill(*col)
		self.app.rect(0, self.height-self.ground_height, self.width, self.ground_height)

	def draw_target(self, col = (255, 0, 0)):
		self.app.fill(*col)
		self.app.rect(self.target_pos, self.height-self.ground_height, self.target_size, self.ground_height)

	def draw(self):
		self.draw_background()
		self.draw_ground()
		self.draw_target()
		if self.rocket is not None:
			self.rocket.update()
			self.rocket.draw()
		self.app.redraw()
		
		# find a safer way to do this maybe?
		if self.app.isDead._flag:
			exit()


scene = Scene(800, 800)
scene.gravity = Vector(0, 0.01)

rocket = Rocket(scene)
rocket.thrust_mag = 0.02
rocket.rotation_mag = 0.02

#file = open("data.csv",'w')
# print("Rocket data from " + (str)(datetime.now()), file=file)
# print("Nr, posX, posY, centerX, centerY, velX, velY, thrustX, thrustY, rot, engine, targetX, targetY", file=file)

while(True):
	rocket.update()
	scene.draw()
	#rocket.print_data(file)
 
