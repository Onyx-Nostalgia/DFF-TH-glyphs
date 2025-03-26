import argparse
import json
import os


def create_thai_glyph_config(font_path, is_replace=False, output_file=None):
    text = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลฦวศษสหฬอฮฯะัาำิีึืฺุู฿เแโใไๅๆ็่้๊๋์ํ"
    if not output_file:
        font_name = os.path.splitext(os.path.basename(font_path))[0].lower()
        for s in [" ", "_"]:
            font_name = font_name.replace(s, "-")
        json_path = f"config/{font_name}.json"
    else:
        if not output_file.endswith(".json"):
            print("Output file must be a JSON file.")
            return
        output_file = output_file.replace("\\", "/")
        if output_file.startswith("./"):
            output_file = output_file[2:]
        if not output_file.startswith("config/"):
            output_file = os.path.join("config", output_file)
        json_path = output_file
    print(f"name: {json_path}")
    if not is_replace and os.path.exists(json_path):
        print(
            "File already exists. If you want to replace the file, please use the '--replace' or '-w' option."
        )
        return
    char_dict = {}
    for char in text:
        char_dict[char] = {
            "adjust_x": 0,
            "adjust_y": 0,
            "vertical_offset": 0,
            "rotate": 0,
        }

    json_data = json.dumps(char_dict, ensure_ascii=False, indent=4)

    with open(json_path, "w", encoding="utf-8") as json_file:
        json_file.write(json_data)

    print(f"JSON data has been written to {json_path}")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="""
Generate Thai glyph configuration JSON for a given font.
- python tools/create_thai_glyph_config.py Sriracha-Regular.ttf
- python tools/create_thai_glyph_config.py Sriracha-Regular.ttf -w
- python tools/create_thai_glyph_config.py Sriracha-Regular.ttf -o sriracha-regular-small.json
                                         """
    )
    arg_parser.add_argument("font_path")
    arg_parser.add_argument(
        "-w",
        "--overwrite",
        "--replace",
        dest="is_replace",
        action="store_true",
        help="overwrite file mode",
        default=False,
    )
    arg_parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        help="output file name (.json)",
    )
    args = arg_parser.parse_args()
    create_thai_glyph_config(args.font_path, args.is_replace, args.output_file)
