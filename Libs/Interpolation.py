import math

class Interpolation:
	def __init__(self, x, intPolType):
		if intPolType == "sin":
			self.sin(x)
		elif intPolType == "smoothStep":
			self.smoothStep(x)
		elif intPolType == "squared":
			self.squared(x)
		elif intPolType == "sqrt":
			self.sqrt(x)
		elif intPolType == "cubed":
			self.cubed(x)
		elif intPolType == "cubedrt":
			self.cubert(x)
		elif intPolType == "dumb":
			self.dumb(x)
		else:
			self.linear(x)
			
	def linear(self, x):
		self.y = x
		return self.y

	def smoothStep(self, x):
		self.y = (3 * x)**2 - (2 * x)**3
		return self.y
	
	def squared(self, x):
		self.y = x**2
		return self.y

	def sqrt(self, x):
		self.y = x**.5
		return self.y

	def cubed(self, x):
		self.y = x**3
		return self.y

	def cubert(self, x):
		self.y = x**float(1/3)
		return self.y

	def sin(self, x):
		self.y = math.sin(x)
		return self.y
	
	def dumb(self, x):
		self.y = ((32*x**12) + (23*x**5) - (3*x**3)) / 2
		return self.y
