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
		
	def seek(self, offset):
		self.offset = offset

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

def BuildDFF(data, width, height, ascii_map, coord_arr):
	writer = FileWriter()

	# HEAD 
	writer.write(b'\x46\x46\x46\x44') # sign
	writer.write_dword(256) # header size
	writer.write_dword(len(coord_arr)) # symobols num

	# MAP
	for i in range(len(ascii_map)):
		value = ascii_map[str(i)]
		writer.write_byte(value) 
	
	# COORD
	for i in range(len(coord_arr)):
		value = coord_arr[str(i)]
		writer.write_word(value['x_start']) 
		writer.write_word(value['y_start']) 
		writer.write_word(value['x_end']) 
		writer.write_word(value['y_end']) 
		writer.write_word(value['base_x']) 
		writer.write_word(value['base_y']) 

	# UNK
	writer.write_dword(3)
	writer.write_dword(width)
	writer.write_dword(height)

	# IMG
	writer.write(data)

	return writer.data


def ParseJSON(JSON_path):
	JSON_data = read_binary(JSON_path)
	data = json.loads(JSON_data.decode('utf-8'))
	coord_arr = data['coord_arr']
	ascii_map = data['ascii_map']
	return ascii_map, coord_arr

def ParseBMP(BMP_path):
	BMP_data = read_binary(BMP_path)
	reader = FileReader(BMP_data)
	reader.skip(2+4+2+2+4+4)
	img_width = reader.read_int32()
	img_height = reader.read_int32()
	
	# LINES
	reader.seek(0x436) 
	lines = list()

	for i in range(img_height):
		lines.append(reader.read(img_width))

	data = b''.join(reversed(lines))

	return data, img_width, img_height



def pack_font(BMP_path, JSON_path):
	ascii_map, coord_arr = ParseJSON(JSON_path)
	data, img_width, img_height = ParseBMP(BMP_path)
	dff_data = BuildDFF(data, img_width, img_height, ascii_map, coord_arr)
	save_binary(BMP_path + '.dff', dff_data)
	

if __name__ == '__main__':
	arg_parser = argparse.ArgumentParser(description='Pack JSON & BMP into DFF')
	arg_parser.add_argument('BMP_path')
	arg_parser.add_argument('JSON_path')
	args = arg_parser.parse_args()
	pack_font(args.BMP_path, args.JSON_path)
