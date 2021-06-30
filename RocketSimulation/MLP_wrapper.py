





class MLP_wrapper:
	def __init__(self, mlp):
		self.mlp = mlp

	def get_move(self, move):
		# why dictionary? :p
		dict_output = {0: 'w', 1: ' ', 2: 's', 3: 'a', 4: 'd', 5: 'p'}
		return dict_output[move[0]]

	def get_decision(self, inputs):
		return self.get_move(self.mlp.predict([inputs]))
