class Zpt(object):
	def __init__(self, x, y, z):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)
	
	def as_t(self):
		return (self.x, self.y, self.z)
