# Testing and understanding

b = 2

def test():
	test.a = b+2


test()
print(test.a)


class Test:
	def __init__(self):
		self.blank = 0

	def test2(self):
		self.a = b+2
		print(self.a)

x = Test()

x.test2()
