

from domain.FileTypeInfo import FileTypeInfo
from domain.ScannedFile import ScannedFile


class ReportItem:
	
	def __init__(
		self,
		scanned_file: ScannedFile,
		file_type_info: FileTypeInfo,
		belongs_to_type: bool
	):
		
		self.__scanned_file = scanned_file
		self.__file_type_info = file_type_info
		self.__belongs = belongs_to_type
	
	def __str__(self):
		
		s = ""
		
		s += "Extension = %s; Path = %s" % (self.__scanned_file.get_extension(), self.__scanned_file.get_path())
		
		return s
	
	def get_path(self):
		
		return self.__scanned_file.get_path()
	
	def belongs(self):
		
		return self.__belongs
