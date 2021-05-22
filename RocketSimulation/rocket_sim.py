from processing_py import *
from random import uniform

from scene import Scene
from rocket import Rocket
from controller import RocketController
from extras import Vector

scene = Scene(800, 800)

rocket = Rocket(scene)

controller = RocketController(rocket, physical_control = True)

while(True):
	controller.control()
	rocket.update()
	# print(rocket.get_data())
	scene.draw()
