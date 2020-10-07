

from domain.Scanner import Scanner
from domain.ScannedFile import ScannedFile
from domain.FileTypesLoader import FileTypesLoader
from domain.FileTypeInfo import FileTypeInfo
from domain.ReportItem import ReportItem


class Detector:
	
	CONST_DEFAULT_HEADER_SCAN_LENGTH = 1000000
	
	def __init__(self, source, source_recurse=True, header_scan_length=None):
		
		self.__source = source
		self.__source_recurse = source_recurse
		
		if header_scan_length is None:
			header_scan_length = self.CONST_DEFAULT_HEADER_SCAN_LENGTH
		self.__header_scan_length = header_scan_length
		
		self.__file_types = FileTypesLoader()
		self.__scanned_files = None
		self.__report_items = None
	
	def run(self):
		
		self.__file_types.load()
		
		scanner = Scanner(dir_path=self.__source, recurse=self.__source_recurse)
		scanner.scan()
		self.__scanned_files = scanner.get_files()
		
		self._generate_report()
		for file_type in self.__file_types.get_types():
			
			print((("*" * 40) + "\n") * 3)
			print("Report for file type:")
			print(str(file_type))
			
			report_items = self.__report_items[file_type.get_key()]
			if len(report_items) > 0:
				for report_item in report_items:
					report_item: ReportItem
					print("Found a file:", report_item.get_path())
			else:
				print("No files found for this file type")
	
	def _generate_report(self):
		
		report_items = {}
		
		# Load each file only once, to save disk reads
		for scanned_file in self.__scanned_files:
			
			scanned_file: ScannedFile
			
			file_header = self._load_file_header(file_path=scanned_file.get_path())
			
			for file_type in self.__file_types.get_types():
				
				type_key = file_type.get_key()
				
				report_items_temp = self._check_file(
					file_type=file_type, scanned_file=scanned_file, file_header=file_header
				)
				
				if file_type.get_key() not in report_items:
					report_items[type_key] = []
				
				for report_item in report_items_temp:
					report_items[type_key].append(report_item)
		
		self.__report_items = report_items
	
	def _load_file_header(self, file_path):
		
		with open(file_path, "rb") as f:
			header_bytes = f.read(self.__header_scan_length)
		
		return header_bytes
	
	@staticmethod
	def _check_file(file_type: FileTypeInfo, scanned_file: ScannedFile, file_header: bytes):
		
		file_extension = scanned_file.get_extension()
		
		items = []
		
		if file_extension not in file_type.get_extensions():
			
			# Look for each marker
			for marker in file_type.get_header_markers():
				
				pos = file_header.find(marker["bytes"])
				if marker["offset"] is None or pos == marker["offset"]:
					item = ReportItem(
						scanned_file=scanned_file,
						file_type_info=file_type
					)
					items.append(item)
		
		return items
