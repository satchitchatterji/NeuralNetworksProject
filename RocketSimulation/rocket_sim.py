from processing_py import *
from random import uniform
import csv

from scene import Scene
from rocket import Rocket
from controller import RocketController
from FNN import ControllerNetwork
from extras import Vector

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

list_of_keys = []

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
		key = rockets[0].scene.app.key
		if key in controls:
			list_of_keys.append(rockets[0].scene.app.key)
		else:
			list_of_keys.append("p")
 
		controller.control(decision)
		ns[decision]+=1
		rocket.update()

	deaths = sum([r.is_dead for r in rockets])
	if deaths == len(rockets):
		print("\nAll rockets dead!")

		with open('scores.txt', 'w') as f:
			for i in range(len(rockets)):

				# if rockets[i].center_pos.x!=135:
				# 	print(rockets[i].score(), rockets[i].center_pos)
				scores.append(rockets[i].score())
				f.write(f'{i}: {rockets[i].score()}\n')
		saved_data = True
		print(ns)
		print(min(scores), max(scores))
		print('Saved score data!')
		print("Don't forget to close the game panel!")
		print(cur_frame)
		print("Save data? T/F")
		answer = input()
		if(answer == 'T'):
			save_data_to_file()
			print("Data saved")
	
	if continual_draw:
		scene.draw()
  
	def save_data_to_file():
		f = open('data_for_training.csv', 'a')
		writer = csv.writer(f)
		input_data = rocket.get_data_list()
		output_data = list_of_keys
		writer.writerow(input_data + output_data)
		# writer.writerow(output_data)

		f.close()
	