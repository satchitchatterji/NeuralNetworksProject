import glob
import csv
import pickle
from datetime import datetime
from sklearn import preprocessing

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

from scene import Scene
from rocket import Rocket
from controller import RocketController
from extras import Vector

"""
The main class for the sklearn MLP classifier, trained with 152 successful games
"""


def get_successful_games():
	list_success = []
	path = "saved_runs\\*.csv"
	for fname in glob.glob(path):
		with open(fname, newline='') as f:
			reader = csv.reader(f)
			row1 = next(reader)  # gets the first line
			if "True" in str(row1):
				list_success.append(fname)
	return list_success

def format_input(row):
	formatted_row = []
	for element in row:
		try:
			formatted_row.append(float(element))
		except ValueError:
			if element == "False":
				formatted_row.append(float(1))
			else:
				formatted_row.append(float(0))
	return formatted_row

def format_output(element):
	dict_output = {'w': 0, ' ': 1, 's': 2, 'a': 3, 'd': 4, 'p': 5}
	return float(dict_output[element])


def separate_input_output():
	list_games = get_successful_games()
	X = []
	y = []
	for game in list_games:
		with open(game, 'r') as read_obj:
			csv_reader = csv.reader(read_obj)
			#skip first two rows
			next(csv_reader)
			next(csv_reader)

			for row in csv_reader:
				X.append(format_input(row[:-1])) # input
				y.append(format_output(row[-1])) # output
	return X, y


def train():
	list_games = get_successful_games()
	print("Number of successful games: ", len(list_games))
	training_data_input = separate_input_output()[0]
	training_data_output = separate_input_output()[1]

	clf = MLPClassifier(hidden_layer_sizes=(11), random_state=1, max_iter=500, learning_rate_init=0.0001, alpha=0.01, warm_start=True,
                     early_stopping=True, activation='tanh').fit(training_data_input, training_data_output)
 
	print("accuracy:", clf.score(training_data_input, training_data_output))
	return clf

def get_move(move):
	dict_output = {0: 'w', 1: ' ', 2: 's', 3: 'a', 4: 'd', 5: 'p'}
	return dict_output[move[0]]


def scale_data(data):
	scaler = preprocessing.StandardScaler()
	return scaler.fit_transform(data)


def main(clf):
	scene = Scene(1000, 1000, init_target_val = 400)
	rocket = Rocket(scene, start_pos='random')
	controller = RocketController(rocket, physical_control = False)

	cur_frame = 0

	while(True):

		cur_frame+=1
		if cur_frame>60*20:
			print('Timeout!')
			rocket.is_dead = True

		if rocket.is_dead:
			break

		game_state = rocket.get_data_list()
		# game_state = scale_data([game_state])
		decision = get_move(clf.predict([game_state]))
		controller.control(decision)
		rocket.update()
		scene.draw()


if __name__ == "__main__":
    
	cur_time = datetime.now()
	test_time = cur_time.strftime('%Y%m%dT%H%M')
 
	tr = True
  
	file_ref = '20210630T1917'

	if tr:
		clf = train()
		pickle.dump(clf, open(f'sklearn_models/{test_time}.pickle', 'wb'))
	else:
		clf = pickle.load(open(f'sklearn_models/{file_ref}.pickle', 'rb'))
	
	main(clf)