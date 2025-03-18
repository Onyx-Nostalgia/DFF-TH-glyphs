import argparse
import os
import struct
import sys

from tabulate import tabulate

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(project_root)

from unpack_font import FileReader, read_binary


def display_image(data, dimensions=(), offset=None, output_file=None):
    _offset = offset[0]
    byte_size = len(data)  # Calculate byte size of the value
    hex_value = " ".join(f"{b:02X}" for b in data)  # Convert value to hex string
    _offset += byte_size

    if output_file:
        # Reformat hex value to be multiline based on image width and height
        w, h = dimensions
        hex_lines = []
        hex_values = hex_value.strip().split(" ")
        for i in range(0, h):
            hex_lines.append("".join(hex_values[i * w : (i + 1) * w]))

        folder_path = os.path.dirname(output_file)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(output_file, "w") as f:
            f.write("\n".join(hex_lines))

    offset[0] = _offset


def display(logs, offset=None, output_file=None):
    table = []
    _offset = offset[0]
    for name, value in logs:
        try:
            byte_size = len(
                struct.pack("i", value)
            )  # Calculate byte size of the integer
            hex_value = " ".join(
                f"{b:02X}" for b in struct.pack("i", value)
            )  # Convert value to hex string
        except struct.error:
            byte_size = len(value)  # Calculate byte size of the integer
            hex_value = " ".join(
                f"{b:02X}" for b in value
            )  # Convert value to hex string

        if len(hex_value) > 24:
            hex_value = f"{hex_value[:24]}...{hex_value[-6:]}"
            value = f"{str(hex_value[:24])}...{str(hex_value[-6:])}"

        end_offset = _offset + byte_size - 1
        table.append(
            [name, f"{_offset}-{end_offset}", byte_size, hex_value, f"{value}"]
        )
        _offset += byte_size

    table_str = tabulate(
        table,
        headers=["Name", "Offset", "Byte Size", "Hex", "Value"],
        tablefmt="grid",
    )

    if output_file:
        folder_path = os.path.dirname(output_file)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(output_file, "w") as f:
            f.write(table_str)

    offset[0] = _offset


def dff_analysis(path):
    filename = os.path.splitext(os.path.basename(path))[0]
    new_folder_name = f"docs/DFF binary structure/{filename}"
    data = read_binary(path)
    reader = FileReader(data)

    logs = [
        ("magic", reader.read_int32()),
        ("ascii_num", reader.read_int32()),
        ("glyph_num", reader.read_int32()),
    ]
    offset = [0]
    display(logs, offset, os.path.join(new_folder_name, "1_Head.txt"))

    # ASCII map glyph
    ascii_map = []
    for i in range(logs[1][1]):
        ascii_map += [(f"glyph_id of ascii_{i}", reader.read_byte())]
    display(ascii_map, offset, os.path.join(new_folder_name, "2_ASCII.txt"))

    # glyph
    glyphs = []
    for i in range(logs[2][1]):
        glyphs += [
            (f"glyph_{i}(x_start)", reader.read_word()),
            (f"glyph_{i}(y_start)", reader.read_word()),
            (f"glyph_{i}(x_end)", reader.read_word()),
            (f"glyph_{i}(y_end)", reader.read_word()),
            (f"glyph_{i}(vertical_offset)", reader.read_word()),
            (f"glyph_{i}(base_y)", reader.read_word()),
        ]

    display(glyphs, offset, os.path.join(new_folder_name, "3_Glyph.txt"))
    unk = reader.read_int32()
    img_width = reader.read_int32()
    img_height = reader.read_int32()
    image = reader.read(img_width * img_height)
    display(
        [
            ("unknown???", unk),
            ("img_width", img_width),
            ("img_height", img_height),
            ("glyph_image", image),
        ],
        offset,
        os.path.join(new_folder_name, "4_Image_metadata.txt"),
    )
    display_image(
        image,
        (img_width, img_height),
        offset,
        os.path.join(new_folder_name, "5_Image.txt"),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=""" 
display DFF file structure table: ex.

python tools/dff_analysis.py data/English/RazNotebook_lin.dff
 
""")
    parser.add_argument("path", type=str, help="(.dff) DFF file path")
    args = parser.parse_args()

    if not args.path.lower().endswith(".dff"):
        parser.error("The file must have a .dff extension")

    dff_analysis(args.path)
