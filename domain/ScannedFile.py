

class ScannedFile:
	
	def __init__(self, path, extension):
		
		self.__path = path
		self.__extension = extension
	
	def __str__(self):
		
		s = ""
		
		s += "ScannedFile(%s) -> %s" % (self.__path, self.__extension)
		
		return s
	
	def get_path(self):
		
		return self.__path
	
	def get_extension(self):
		
		return self.__extension
