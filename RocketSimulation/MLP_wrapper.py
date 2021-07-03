import numpy as np

class MLP_wrapper:
	def __init__(self, mlp):
		self.mlp = mlp

	def get_move(self, move):
		outputs = ['w', ' ', 's', 'a', 'd', 'p']
		try:
			# sklearn MLPClassifier works with this
			# as far as MLP.py is written
			return outputs[move[0]]
		except IndexError:
			# tflearn DNN works with this
			# as far as MLP_tnsrfl.py is written
			return outputs[move]

	def get_decision(self, inputs):
		try:
			# sklearn MLPClassifier works with this
			# as far as MLP.py is written
			return self.get_move(self.mlp.predict([inputs]))
		except ValueError:
			# tflearn DNN works with this
			# as far as MLP_tnsrfl.py is written
			inputs = np.array([i for i in inputs]).reshape(-1,len(inputs),1)
			return self.get_move(np.argmax(self.mlp.predict(inputs)))
