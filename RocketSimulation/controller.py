class RocketController:
	"""
	A controller class for a rocket object, passed in
	as a parameter to constructor. The class can handle
	parsing the key inputs (either from a physical keyboard
	or a single character string representing the keys)
	and is designed to control a single rocket object.
	
	Currently, to control the rocket, there are these options
	that are called using functions stored in the controls
	dictionary:
		KEY   ->   BEHAVIOUR
		'w'   ->   Turn engine on
		' '   ->   Turn engine off <space>
		's'   ->   Stop rotation
		'a'   ->   Rotate anticlockwise (turn left)
		'd'   ->   Rotate anticlockwise (turn right)
		'r'   ->   Reset all values of rocket (pos, vel, acc)

	To control a rocket with a physical keyboard, set
	the physical_control parameter in the constructor to True.

	At each timepoint, call the update function to control.

	"""
	def __init__(self, rocket, physical_control = True):
		self.rocket = rocket
		self.scene = self.rocket.scene
		self.physical_control = physical_control

		self.controls = {}
		self.controls['w'] = self.engine_on
		self.controls[' '] = self.engine_off
		self.controls['s'] = self.stop_rotation
		self.controls['a'] = self.rotate_left
		self.controls['d'] = self.rotate_right
		self.controls['r'] = self.reset
		
		# If an unknown key is pressed,
		# carry on doing the same thing as if
		# no key was pressed at all. This
		# can be helpful if a autonomous controller
		# is given the option to do nothing at
		# any given time point. By default,
		# it's set to turn engine off (key:=' ')
		# since it does nothing at the start of
		# a rocket simulation.
		self.last_function = self.engine_off
	
	##### Control functions #####

	def engine_on(self):
		self.rocket.engine_on = True
	
	def engine_off(self):
		self.rocket.engine_on = False
	
	def stop_rotation(self):
		pass
	
	def rotate_left(self):
		self.rocket.rotation -= self.rocket.consts["rotation_speed"]
	
	def rotate_right(self):
		self.rocket.rotation += self.rocket.consts["rotation_speed"]
	
	def reset(self):
		self.rocket.reset_all()

	def control(self, key = None):
		"""
		Main control function. This method should be called
		at each timepoint or when you want to control the rocket.
		If physical_control is set to True at the constructor,
		then you only need to call <Controller object>.update()

		If it is set to False, then you can pass in a key (single character)
		returned by a virtual controller, e.g. a NN model. In this case,
		call <Controller object>.update(str:<key option>) 
		(example: controller.update('w') to turn the engine on)
		"""
		if self.physical_control:
			self.parse_keyboard_input()
		else:
			if key is not None:
				self.parse_virtual_input(key)
			else:
				print("Invalid key input")

	##### Various input functions #####

	def parse_virtual_input(self, key):
		self.__press_key__(key)

	def parse_keyboard_input(self):
		self.__press_key__(self.scene.app.key)
	
	##### Executes behavior change in rocket #####

	def __press_key__(self, key):
		if key in self.controls.keys():
			self.last_function = self.controls[str(key)]
		else:
			pass

		self.last_function()
	