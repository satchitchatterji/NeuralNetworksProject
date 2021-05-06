import os
import math

from extras import Vector
class Rocket:
	def __init__(self, scene):
		self.scene = scene
		
		self.rocket_img_path = os.getcwd()+'/rocket.png'
		self.rocket_img = self.scene.app.loadImage(self.rocket_img_path)
		
		self.img_height = 100
		self.img_width = 0.7*self.img_height

		self.pos = Vector(0, 0) 
		self.pos.x = self.scene.width/2 - self.img_width/2
		self.pos.y = self.scene.height - self.scene.ground_height - self.img_height

		self.center_pos = Vector(0,0)
		self.update_center_pos()

		self.fire_img_path = os.getcwd()+'/fire.png'
		self.fire_img = self.scene.app.loadImage(self.fire_img_path)
		self.fire_img_width = 0.25 * self.img_width
		self.fire_img_height = 10/9 * self.fire_img_width
		
		self.rotation = 0
		self.rotation_mag = 0.02

		self.vel = Vector(0, 0)
		self.engine_on = False
		self.thrust = Vector(0, 0)
		self.thrust_mag = 0.015

		scene.add_rocket(self)

	def update_center_pos(self):
		self.center_pos.x = self.pos.x + self.img_width/2
		self.center_pos.y = self.pos.y + self.img_height/2

	def update_fire_coords(self):
		# self.fire_x = self.pos.x + 0.38*self.img_width
		# self.fire_y = self.pos.y + 0.94*self.img_height

		self.fire_x = 0.38*self.img_width-self.img_width/2
		self.fire_y = 0.94*self.img_height-self.img_height/2

	def reset_position(self):
		self.pos.x = self.scene.width/2 - self.img_width/2
		self.pos.y = self.scene.height - self.scene.ground_height - self.img_height
		self.update_center_pos()

	def reset_rotation(self):
		self.rotation = 0

	def reset_movement(self):
		self.thrust.zeros()
		self.vel.zeros()
		self.engine_on = False
		
	def parse_key_input(self):
		# turn engine on and off
		if self.scene.app.key == 'w':
			self.engine_on = True
		elif self.scene.app.key == ' ':
			self.engine_on = False

		# turn rotation off and on
		elif self.scene.app.key == 's':
			pass # stops rotation
		elif self.scene.app.key == 'a':
			self.rotation -= self.rotation_mag
		elif self.scene.app.key == 'd':
			self.rotation += self.rotation_mag

		elif self.scene.app.key == 'r':
			self.reset_position()
			self.reset_movement()
			self.reset_rotation()

	def update_thrust(self):
		if self.engine_on:
			self.thrust.x = -self.thrust_mag*math.cos(self.rotation+math.pi/2)
			self.thrust.y = -self.thrust_mag*math.sin(self.rotation+math.pi/2)
		else:
			self.thrust.zeros()

	def update_velocity(self):
		self.vel += self.scene.gravity
		self.vel += self.thrust

	def update_position(self):
		self.pos += self.vel

		if self.pos.y + self.img_height > self.scene.height - self.scene.ground_height:
			self.pos.y = self.scene.height - self.scene.ground_height - self.img_height
			self.reset_movement()

	def update(self):
		self.parse_key_input()
		self.update_thrust()
		self.update_velocity()
		self.update_position()

	def draw(self):
		self.scene.app.pushMatrix()
		self.update_center_pos()
		self.scene.app.translate(self.center_pos.x, self.center_pos.y)
		self.scene.app.rotate(self.rotation)

		if self.engine_on:
			self.update_fire_coords()
			self.fire_img = self.scene.app.loadImage(self.fire_img_path)
			self.scene.app.image(self.fire_img, self.fire_x, self.fire_y, self.fire_img_width, self.fire_img_height)

		self.rocket_img = self.scene.app.loadImage(self.rocket_img_path) 
		self.scene.app.image(self.rocket_img, -self.img_width/2, -self.img_height/2, self.img_width, self.img_height)
		self.scene.app.popMatrix()

