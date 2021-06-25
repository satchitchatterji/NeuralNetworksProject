




import numpy as np

class Layer:

	def __init__(self, n_inputs, n_neurons):
		self.weights = np.random.randn(n_inputs, n_neurons)
		self.biases = np.random.randn(1, n_neurons)
		# self.biases = np.zeros((1, n_neurons))
		self.activation_f = self.sigmoid

	def tanh(self, x):
		return np.tanh(x)

	def relu(self, x):
		return np.maximum(0, x)

	def sigmoid(self, x):
		return (1/(1 + np.exp(-x)))

	def set_parameters(self, weights, biases):
		self.weights = weights
		self.biases = biases

	def get_parameters(self):
		return self.weights, self.biases

	def forward(self, inputs):
		self.outputs = self.activation_f(np.dot(inputs, self.weights) + self.biases)

class ControllerNetwork:
	def __init__(self, n_inputs, n_outputs, single_layer=True):
		self.size = (n_inputs, len(n_outputs))
		self.controls = n_outputs
		self.layers = []
		if single_layer:
			self.add_layer(n_inputs, n_inputs)
			# self.add_layer(n_inputs, n_inputs)
			self.add_layer(n_inputs, len(n_outputs))
		# you can add more layers here
		# make sure the nth layer ouput is the
		# same length as (n+1)th layer input
		# and the final layer has output length
		# equal to len(n_outputs).

	def add_layer(self, input_size, output_size):
		self.layers.append(Layer(input_size, output_size))

	def set_layer_parameters(self, layer=0, weights=None, biases=None):
		self.layers[layer].set_parameters(weights, biases)

	def get_layer_parameters(self, layer=0):
		return self.layers[layer].get_parameters()

	def forward(self, inputs):
		last_outputs = inputs
		for i in range(len(self.layers)):
			self.layers[i].forward(last_outputs)
			last_outputs = self.layers[i].outputs

	def get_max(self):
		highest = np.argmax(self.layers[-1].outputs)
		return highest

	def get_decision(self, inputs):
		self.forward(inputs)
		return self.controls[self.get_max()]