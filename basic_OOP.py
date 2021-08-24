class ClassA():
	var1 = 0
	var2 = 0
	def __init__(self):
		ClassA.var1 = 1
		ClassA.var2 = 2

	def methodA(self):
		ClassA.var1 = ClassA.var1 + ClassA.var2
		return ClassA.var1

class ClassB(ClassA):
	def __init__(self):
		print(ClassA.var1, "1")
		print(ClassA.var2, "2")

object1 = ClassA()
sum = object1.methodA()

object2 = ClassB()
print(sum)