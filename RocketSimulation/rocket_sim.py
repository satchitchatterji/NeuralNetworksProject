from processing_py import *

from extras import Vector
from rocket import Rocket

class Scene:
	def __init__(self, width, height):
		self.app = App(width, height)
		self.width = width
		self.height = height
		self.ground_height = 20
		self.rocket = None

		self.gravity = Vector(0, 0.01)

	def add_rocket(self, rocket):
		self.rocket = rocket

	def draw_background(self):
		self.app.background(0,0,0)

	def draw_ground(self, col=(33,179,47)):
		self.app.fill(*col)
		self.app.rect(0, self.height-self.ground_height, self.width, self.ground_height)

	def draw(self):
		self.draw_background()
		self.draw_ground()
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
rocket.thrust_mag = 0.015
rocket.rotation_mag = 0.02

while(True):
	rocket.update()
	scene.draw()
