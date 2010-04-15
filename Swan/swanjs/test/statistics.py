grades = ['F','F','F','E','D','C','B','A','A','A+','A+']
coursenames = ["Programming", "Logic", "Hardware", "DiscreteMathematics", "MathematicalMethods", "ComputerSystems", "Graphics"]

class Course():
	
	def __init__(self):
		self.students = []
		self.marks = [0,0,0,0,0,0,0,0,0,0,0]
	
	def setName(self, name):
		self.name = name
		
	def addStudent(self, login, mark):
		self.students.append([login, grades[mark]])
		self.marks[mark] += 1
		
	def getMean(self):
		tot = 0
		for rank in range(11):
			tot += (rank * self.marks[rank])
		self.mean = tot / len(self.students)
		return self.mean
		
	def getSD(self):
		tot = 0
		for rank in range(11):
			for count in range(self.marks[rank]):
				dif = (rank - self.mean)
				tot += dif ** 2
		return tot/len(self.students)

inputs = native("location.hash.slice(1)")
outputs = []

courses = inputs.split(';')

for course in courses[:-1]:
	parts = course.strip().split(' ')
	coursename = parts[0]
	c = Course()
	c.setName(coursename)
	outputs.append(c)
	for i in range(1, len(parts), 2):
		log = parts[i]
		mark = parts[i+1]
		c.addStudent(log, mark)


for output in outputs:
	print output.name
	print output.students
	print "Mean: " + output.getMean()
	print "SD: " + native("Math.sqrt(statistics_output.getSD())")