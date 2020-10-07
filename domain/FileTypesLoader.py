

from domain.FileTypeInfo import FileTypeInfo


import json
import os


class FileTypesLoader:
	
	CONST_DATA_FOLDER_NAME = "data"
	
	def __init__(self):
		
		self.__types = None
	
	def load(self):
		
		file_types = list()
		
		types_dir = os.path.join(
			os.path.dirname(__file__),
			self.CONST_DATA_FOLDER_NAME
		)
		for root_path, dirs, files in os.walk(types_dir):
			
			for file_name in files:
				
				file_path = os.path.join(root_path, file_name)
				
				with open(file_path, "rt") as f:
					jss = f.read()
				
				j = json.loads(jss)
				file_type = self._consume_file_json(j=j)
				file_types.append(file_type)
				print("Loaded file type: %s" % (file_type.get_label()))
		
		self.__types = file_types
	
	def _consume_file_json(self, j):
		
		marker_infos = j["header"]["markers"]
		marker_infos_decoded = []
		for marker_info in marker_infos:
			
			if "offset" in marker_info.keys():
				marker_offset = marker_info["offset"]
			else:
				marker_offset = None
			
			marker_bytes_encoded = marker_info["bytes"]
			
			marker_bytes_decoded = self._decode_header_marker_bytes(marker_bytes_encoded=marker_bytes_encoded)
			marker_infos_decoded.append({
				"offset": marker_offset,
				"bytes": marker_bytes_decoded
			})
		
		file_type_info = FileTypeInfo(
			key=j["key"],
			label=j["label"],
			mime_types=j["mime_types"],
			extensions=j["extensions"],
			header_markers=marker_infos_decoded
		)
		
		return file_type_info
	
	@staticmethod
	def _decode_header_marker_bytes(marker_bytes_encoded):
		
		marker_encoded: str
		marker_bytes_array = bytearray()
		
		i = 0
		while i < len(marker_bytes_encoded):
			
			pos = marker_bytes_encoded.find("\\0x", i)
			if pos == i:
				
				# print("Found hex stringy thing at", marker_encoded[pos:])
				
				the_hex = marker_bytes_encoded[i+3:i+5]
				# print("Pulled hex:", the_hex)
				the_byte = int(the_hex, 16)
				# print("Adding to:", marker_bytes)
				marker_bytes_array.append(the_byte)
				# print("Bytearray is now:", marker_bytes)
				i += 4
				
			else:
				# print("Appending:", marker_encoded[i])
				marker_bytes_array += marker_bytes_encoded[i].encode()
			
			i += 1
		
		marker_bytes = bytes(marker_bytes_array)
		
		return marker_bytes
	
	def get_types(self):
		
		return self.__types
