'''
Python 3
'''

import os
import sys
import json
import struct
import argparse


##############################################################	

def read_binary(path):
	with open(path, "rb") as f:
		return f.read()
	return False
	
def save_binary(path, data):
	with open(path, "wb") as f:
		return f.write(data)
	return False
	
##############################################################	

class FileWriter:

	def __init__(self):
		self.data = b''

	def write(self, data):
		self.data += data
		
	def write_dword(self, data):
		self.data += struct.pack('<I', data)
		
	def write_byte(self, data):
		self.data += struct.pack('B', data)

	def write_word(self, data):
		self.data += struct.pack('H', data)

##############################################################	

class FileReader:

	def __init__(self, data):
		self.offset = 0
		self.data = data
		
	def skip(self, size):
		self.offset += size
		
	def read(self, size):
		out = self.data[self.offset : self.offset + size]
		self.skip(size)
		return out
		
	def read_int32(self):
		return struct.unpack('<I', self.read(4))[0]
	
	def read_byte(self):
		return struct.unpack('B', self.read(1))[0]

	def read_word(self):
		return struct.unpack('H', self.read(2))[0]

	def read_sign(self):
		return struct.unpack('<4s', self.read(4))[0]


class Coord:

	def __init__(self, x_start, y_start, x_end, y_end, base_x, base_y):
		self.x_start = x_start
		self.y_start = y_start
		self.x_end = x_end
		self.y_end = y_end
		self.base_x = base_x
		self.base_y = base_y
		
	@staticmethod
	def read(reader):
		x_start = reader.read_word()
		y_start = reader.read_word()
		x_end = reader.read_word()
		y_end = reader.read_word()
		base_x = reader.read_word()
		base_y = reader.read_word()
		return Coord(x_start, y_start, x_end, y_end, base_x, base_y)

	def __repr__(self):
		return f'[{self.x_start}:{self.y_start} {self.x_end}:{self.y_end}]'



##############################################################	

def BuildBMP(data, width, height):
	writer = FileWriter()

	# HEAD
	writer.write(b'\x42\x4D') # sign
	writer.write_dword(1078 + width * height) # BMP size
	writer.write_word(0) # reserved
	writer.write_word(0) # reserved
	writer.write_dword(1078) # bit offset

	# INFO
	writer.write_dword(40) # size
	writer.write_dword(width)
	writer.write_dword(height)
	writer.write_word(1) # planes
	writer.write_word(8) # bit count
	writer.write_dword(0) # compression
	writer.write_dword(width * height) # image size
	writer.write_dword(3780) # pix per meter
	writer.write_dword(3780) 
	writer.write_dword(256) # color used
	writer.write_dword(256) # color important

	# PALLETE
	for i in range(256):
		for i2 in range(3):
			writer.write_byte(i)
		writer.write_byte(0)

	# LINES
	lines = []

	for i in range(height):
		line = data[i*width:i*width+width]
		lines.append(line)

	data = b''.join(reversed(lines))
	writer.write(data)

	return writer.data

##############################################################	

def BuildJSON(ascii_map, coord_arr, img_width, img_height):
	data = dict()
	data['ascii_map'] = ascii_map
	data['coord_arr'] = dict()

	for index in range(len(coord_arr)):
		item = dict()
		coord = coord_arr[index]
		item['x_start'] = coord.x_start
		item['y_start'] = coord.y_start
		item['x_end'] = coord.x_end
		item['y_end'] = coord.y_end
		item['base_x'] = coord.base_x
		item['base_y'] = coord.base_y
		data['coord_arr'][index] = item
		
	return json.dumps(data, indent=4)

##############################################################	


def unpack_font(path):
	data = read_binary(path)
	reader = FileReader(data)

	magic = reader.read_int32()
	map_size = reader.read_int32()
	coord_num = reader.read_int32()

	ascii_map = dict()

	for i in range(map_size):
		ascii_map[i] = reader.read_byte()

	coord_arr = dict()

	for i in range(coord_num):
		coord_arr[i] = Coord.read(reader)

	unk = reader.read_int32()
	img_width = reader.read_int32()
	img_height = reader.read_int32()
	image = reader.read(img_width * img_width)

	bmp = BuildBMP(image, img_width, img_height)
	save_binary(path + '.bmp', bmp)

	json_list = BuildJSON(ascii_map, coord_arr, img_width, img_height)
	save_binary(path + '.json', json_list.encode('utf-8'))
	

if __name__ == '__main__':
	arg_parser = argparse.ArgumentParser(description='Unpack *.DFF file')
	arg_parser.add_argument('dff_file_path')
	args = arg_parser.parse_args()
	unpack_font(args.dff_file_path)
