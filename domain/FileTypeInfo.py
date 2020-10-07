

class FileTypeInfo:

	def __init__(
		self,
		label,
		key,
		mime_types,
		extensions,
		header_markers
	):
		self.__label = label
		
		self.__key = key
		
		if isinstance(mime_types, str):
			mime_types = [mime_types]
		self.__mime_types = mime_types
		
		if isinstance(extensions, str):
			extensions = [extensions]
		self.__extensions = extensions
		
		self.__header_markers = header_markers
		self.__header_markers_max_length = None
		
		self._changed()
	
	def __str__(self):
		
		s = ""
		
		s += "Key: %s\n" % (self.__key,)
		s += "Mime types: %s\n" % (self.__mime_types,)
		s += "Known extensions: %s\n" % (self.__extensions,)
		s += "Header markers: %s\n" % (self.__header_markers,)
		
		return s
	
	def _changed(self):
	
		longest_marker = 0
		
		for marker in self.__header_markers:
			if len(marker) > longest_marker:
				longest_marker = len(marker)
		
		self.__header_markers_max_length = longest_marker
	
	def get_key(self):
		
		return self.__key
	
	def get_label(self):
		
		return self.__label
	
	def get_extensions(self):
	
		return self.__extensions[:]
	
	def get_header_markers(self):
		
		return self.__header_markers
