

from domain.ScannedFile import ScannedFile


import copy
import os
import re


class Scanner:
	
	def __init__(self, dir_path, recurse=True):
		
		assert recurse is True, "Non-recursive scanning not implemented"
		
		self.__dir_path = dir_path
		self.__recurse = recurse
		
		self.__files = None
		
		self.__regex_file_extension_compiled = re.compile(R".*\.(?P<extension>[a-zA-Z0-9]+)$")
		
	def scan(self):
		
		scanned_files = []
		
		for root_path, dirs, files in os.walk(self.__dir_path):
			
			for f in files:
				
				file_path = os.path.join(root_path, f)
				file_extension = self._get_file_extension(file_path)
				
				scanned_files.append(ScannedFile(path=file_path, extension=file_extension))
		
		self.__files = scanned_files
	
	def get_files(self):
		
		return copy.deepcopy(self.__files)
	
	def _get_file_extension(self, file_path):
		
		extension = None
		
		match = self.__regex_file_extension_compiled.match(file_path)
		if match:
			
			extension = match.group("extension")
			extension = extension.lower()
		
		return extension
