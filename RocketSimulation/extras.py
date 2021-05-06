# maybe replace with numpy vector
class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def zeros(self):
		self.x = 0
		self.y = 0

	def __neg__(self):
		return Vector(-self.x, -self.y)

	def __add__(self, other):
		return Vector(self.x+other.x, self.y+other.y)

	def __sub__(self, other):
		return Vector(self.x-other.x, self.y-other.y)

	def __repr__(self):
		return(f"x: {self.x}, y: {self.y}")
