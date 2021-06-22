from processing_py import *
from random import uniform
import csv

from scene import Scene
from rocket import Rocket
from controller import RocketController
from FNN import ControllerNetwork
from extras import Vector

from datetime import datetime

##### CHANGE YOUR NAME HERE #####

player_name = 'andreea'


cur_time = datetime.now()
test_time = cur_time.strftime('%Y%m%dT%H%M')
subdir = 'saved_runs/'
print(f"Current time: {cur_time.strftime('%X')}")

continual_draw = True
n_rockets = 1

scene = Scene(1000, 1000)
rockets = [Rocket(scene, start_pos=Vector(100,100)) for _ in range(n_rockets)]

input_len = len(rockets[0].get_data_list())
controls = ['w',' ', 's', 'a', 'd']

controllers = [RocketController(rocket, physical_control = True) for rocket in rockets]
cns = [ControllerNetwork(input_len, controls) for _ in range(n_rockets)]

frames = 10000
cur_frame = 0
saved_data = False

ns = {}

for c in controls:
	ns[c] = 0
scores = []
while(True):

	if saved_data:
		scene.draw()
		continue

	cur_frame+=1
	if cur_frame>frames:
		print('Timeout!')
		for rocket in rockets:
			rocket.is_dead = True

	for i in range(len(rockets)):
		rocket = rockets[i]
		controller  = controllers[i]
		cn = cns[i]

		if rocket.is_dead:
			continue

		decision = cn.get_decision(rocket.get_data_list())
		controller.control(decision)
		ns[decision]+=1
		rocket.update()

	deaths = sum([r.is_dead for r in rockets])
	if deaths == len(rockets):
		print("\nAll rockets dead!")

		with open('scores.txt', 'w') as f:
			for i in range(len(rockets)):
				scores.append(rockets[i].score())
				f.write(f'{i}: {rockets[i].score()}\n')

		# assuming one rocket for now
		for controller in controllers:
			controller.save_to_file(f'{subdir}/{player_name}_save_{test_time}.csv')

		saved_data = True
		print(ns)
		print(min(scores), max(scores))
		print('Saved score data!')
		print("Don't forget to close the game panel!")
		
	
	if continual_draw:
		scene.draw()