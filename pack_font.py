import argparse
import json
import struct

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
        self.data = b""

    def write(self, data):
        self.data += data

    def write_dword(self, data):
        self.data += struct.pack("<I", data)

    def write_byte(self, data):
        self.data += struct.pack("B", data)

    def write_word(self, data):
        self.data += struct.pack("H", data)


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
        return struct.unpack("<I", self.read(4))[0]

    def read_byte(self):
        return struct.unpack("B", self.read(1))[0]

    def read_word(self):
        return struct.unpack("H", self.read(2))[0]

    def read_sign(self):
        return struct.unpack("<4s", self.read(4))[0]


def build_dff(data, width, height, ascii_map, coord_arr):
    writer = FileWriter()

    # HEAD
    writer.write(b"\x46\x46\x46\x44")  # sign
    writer.write_dword(256)  # ascii size
    writer.write_dword(len(coord_arr))  # glyph num

    # MAP
    for i in range(len(ascii_map)):
        value = ascii_map[str(i)]
        writer.write_byte(value)

    # COORD
    for i in range(len(coord_arr)):
        value = coord_arr[str(i)]
        writer.write_word(value["x_start"])
        writer.write_word(value["y_start"])
        writer.write_word(value["x_end"])
        writer.write_word(value["y_end"])
        writer.write_word(value["base_x"])
        writer.write_word(value["base_y"])

    writer.write_dword(3)  # UNK
    writer.write_dword(width)
    writer.write_dword(height)

    # IMG
    writer.write(data)

    return writer.data


def parse_json(json_path):
    json_data = read_binary(json_path)
    data = json.loads(json_data.decode("utf-8"))
    coord_arr = data["coord_arr"]
    ascii_map = data["ascii_map"]
    return ascii_map, coord_arr


def parse_bmp(bmp_path):
    bmp_data = read_binary(bmp_path)
    reader = FileReader(bmp_data)
    reader.skip(2 + 4 + 2 + 2 + 4 + 4)
    img_width = reader.read_int32()
    img_height = reader.read_int32()

    # LINES
    reader.seek(0x436)
    lines = list()

    for _ in range(img_height):
        lines.append(reader.read(img_width))

    data = b"".join(reversed(lines))

    return data, img_width, img_height


def pack_font(bmp_path, json_path):
    ascii_map, coord_arr = parse_json(json_path)
    data, img_width, img_height = parse_bmp(bmp_path)
    dff_data = build_dff(data, img_width, img_height, ascii_map, coord_arr)
    dff_path = bmp_path.split(".")[0] + ".dff"
    save_binary(dff_path, dff_data)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Pack JSON & BMP into DFF")
    arg_parser.add_argument("bmp_path")
    arg_parser.add_argument("json_path")
    args = arg_parser.parse_args()
    pack_font(args.bmp_path, args.json_path)
