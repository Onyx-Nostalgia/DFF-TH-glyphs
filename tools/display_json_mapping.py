import argparse
import json


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def display_by_ascii_number(data):
    for ascii_code, glyph_id in data["ascii_map"].items():
        coord_arr = data["coord_arr"][str(glyph_id)]
        char = coord_arr.get("char", chr(int(ascii_code))) if glyph_id != 0 else "a"
        x_start, y_start = coord_arr["x_start"], coord_arr["y_start"]
        x_end, y_end = coord_arr["x_end"], coord_arr["y_end"]
        w, h = x_end - x_start, y_end - y_start
        base_x, base_y = coord_arr["base_x"], coord_arr["base_y"]

        print(
            f"{ascii_code=}: _{char}_ {glyph_id=} {w=} {h=} start_pos:({x_start},{y_start}) end_pos:({x_end}, {y_end}) base:({base_x},{base_y})"
        )


def display_by_coord_arr(data):
    ascii_swap = {}
    for ascii_code, glyph_id in data["ascii_map"].items():
        if f"{glyph_id}" in ascii_swap:
            continue
        if glyph_id == 0:  # char a
            ascii_swap[f"{glyph_id}"] = 97
            continue
        ascii_swap[f"{glyph_id}"] = int(ascii_code)

    for glyph_id, coord_arr in data["coord_arr"].items():
        x_start, y_start = coord_arr["x_start"], coord_arr["y_start"]
        x_end, y_end = coord_arr["x_end"], coord_arr["y_end"]
        w, h = x_end - x_start, y_end - y_start
        base_x, base_y = coord_arr["base_x"], coord_arr["base_y"]

        if f"{glyph_id}" not in ascii_swap:
            print(
                f"{glyph_id=}: NO ASCII MAP {w=} {h=} start_pos:({x_start},{y_start}) end_pos:({x_end}, {y_end}) base:({base_x},{base_y})"
            )
            continue

        ascii_code = ascii_swap[f"{glyph_id}"]
        char = coord_arr.get("char", chr(int(ascii_code)))

        print(
            f"{glyph_id=}: _{char}_ {ascii_code=} {w=} {h=} start_pos:({x_start},{y_start}) end_pos:({x_end}, {y_end}) base:({base_x},{base_y})"
        )


if __name__ == "__main__":
    description = """
    display json mapping 
    ex: 
    python display_json_mapping.py RazNotebook_lin.json --mode coord
    """
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument("file_path", type=str, help="Path to the JSON file")
    arg_parser.add_argument(
        "--mode",
        type=str,
        choices=["coord", "ascii"],
        default="coord",
        help="(Default: 'coord') Mode to display data: 'coord' or 'ascii'",
    )
    args = arg_parser.parse_args()

    data = load_json(args.file_path)

    match args.mode:
        case "coord":
            display_by_coord_arr(data)
        case "ascii":
            display_by_ascii_number(data)
