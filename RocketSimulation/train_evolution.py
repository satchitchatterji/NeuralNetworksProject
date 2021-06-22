from processing_py import *
from random import uniform

from scene import Scene
from rocket import Rocket
from controller import RocketController
from FNN import ControllerNetwork
from extras import Vector
from genetic import ControllerPopulation
import pickle
import numpy as np
from datetime import datetime
from trial import run_multi_trials

cur_time = datetime.now()
test_time = cur_time.strftime('%Y%m%dT%H%M')
subdir = 'tests/'
print(f"Current time: {cur_time.strftime('%X')}")


generations = 20
n_rockets = 50
n_trials = 10 # number of random trials per generation

notes = f"Only velocity score"

notes = f'Gens: {generations}, Rockets: {n_rockets}, ' + notes

continual_draw = False


scene = Scene(1000, 1000, init_target_val = 800)
rockets = [Rocket(scene, start_pos=Vector(100,100)) for _ in range(n_rockets)]

for rocket in rockets:
	rocket.rotation = np.pi

input_len = len(rockets[0].get_data_list())
controls = ['w',' ', 's', 'a', 'd']

controllers = [RocketController(rocket, physical_control = False) for rocket in rockets]
cns = [ControllerNetwork(input_len, controls) for _ in range(n_rockets)]

mean_scores = []
sd_scores = []
min_scores = []

for i_generation in range(generations):

	print(f'Generation {i_generation}')
	controller_population = ControllerPopulation(controllers, cns)
	
	scores = run_multi_trials(n_trials, scene, rockets, controllers, cns, init='random')

	for r in range(len(rockets)):
		rockets[r].set_score(scores[r])

	mean_scores.append(sum(scores)/len(scores))
	min_scores.append(min(scores))
	sd_scores.append(np.std(scores))
	print(min(scores))
	
	if i_generation != generations - 1:
		cns = controller_population.reproduce()

	for rocket in rockets:
		rocket.reset_all()

s_scores = sorted(scores)
s_cns = []

for s in s_scores:
	s_cns.append(cns[scores.index(s)])

print(mean_scores)
print(min_scores)

pickle.dump(s_cns, open(f'{subdir}/sorted_cn_list_{test_time}.pickle', 'wb'))

with open(f'{subdir}/mean_scores_{test_time}.txt', 'w') as f:
	f.write(str(mean_scores))

with open(f'{subdir}/min_scores_{test_time}.txt', 'w') as f:
	f.write(str(min_scores))

with open(f'{subdir}/sd_scores_{test_time}.txt', 'w') as f:
	f.write(str(sd_scores))

with open(f'{subdir}/scene_attr_{test_time}.txt', 'w') as f:
	f.write(str(vars(scene)))

with open(f'{subdir}/logs.txt', 'a') as f:
	f.write('\n'+test_time+","+notes+f', Run time: \t{(datetime.now()-cur_time).total_seconds()}')


print('Data saved!')
print(f'File reference:{test_time}')
print('Time to run:')
print(f'\t{(datetime.now()-cur_time).total_seconds()}')
exit()

