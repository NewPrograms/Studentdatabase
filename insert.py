
class Insert:
	def __init__(self, engine):
		self.engine  = engine
	def read_file(self, path):
		with open(path) as p:
			data = p.read()
			self.execute_file(data)
			p.close()
	def execute_file(self, data):
		self.engine.execute(data)