
class test():
	def __init__(self):
		self.x = None

	def two(self):
		self.x = 20
		return self.x

	def one(self):
		three = 30
		return three



fox = test()
fox.two()
print(fox.x)

