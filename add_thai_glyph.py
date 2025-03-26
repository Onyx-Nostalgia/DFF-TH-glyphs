import argparse
import json
import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageOps


def get_start_position(json_path):
    # Get the last position of the latest glyph
    with open(json_path, "r") as f:
        data = json.load(f)
    last_coord_id = list(data["coord_arr"].keys())[-1]
    last_coord = data["coord_arr"][last_coord_id]
    x_end, y_start = last_coord["x_end"], last_coord["y_start"]

    x_start_new_glyph = x_end + 1
    return (x_start_new_glyph, y_start)


def thai_to_ascii(text):
    # Mapping Thai characters to ASCII code
    ascii_code = 161
    thai_ascii = {}
    for char in text:
        # skip to ascii 223 THAI CURRENCY SYMBOL BAHT
        if char == "฿":
            ascii_code = 223
        # skip to ascii 239 THAI CHARACTER FONGMAN
        if char == "๏":
            ascii_code = 239
        thai_ascii[char] = ascii_code
        ascii_code += 1

    return thai_ascii


def draw_hide_dot(draw, xy, char, font):
    if "." not in char:
        return
    x1, _, _, y2 = xy
    dot_x1, dot_y1, dot_x2, dot_y2 = font.getbbox(".")
    w = dot_x2 - dot_x1
    h = dot_y2 - dot_y1
    if any(top_char in char for top_char in "ำ"):  # case top vowels
        draw.rectangle((x1, y2 - h -1, x1 + w, y2 + h), fill="black")


def get_char_size(draw_char, font):
    raw_char = draw_char.replace(".", "")
    char_width = font.getbbox(raw_char)[2] - font.getbbox(raw_char)[0]
    char_height = font.getbbox(raw_char)[3] - font.getbbox(raw_char)[1]

    if "." in draw_char and any(top_char in draw_char for top_char in "่๋ี๊์้็" + "ึีืิั" + "ํ"):
        _, dot_y1, _, dot_y2 = font.getbbox(".")
        dot_height = dot_y2 - dot_y1
        char_height -= dot_height * 1

    return char_width, char_height


def append_thai_glyphs(
    image_path,
    output_path,
    font_path,
    font_size,
    text,
    position,
    json_path,
    new_json_path,
    is_show_box=False,
    config=None,
):
    img = Image.open(image_path)
    font = ImageFont.truetype(font_path, font_size)
    origin_img_size = img.size
    x, y = position
    max_height = 0
    glyph_coordinates = []
    thai_ascii_codes = thai_to_ascii(text)
    adjust = get_adjust(font_path,config)

    for char in text:
        draw_char = char
        # ADD '.' TO MAKE OK FORM
        if char in "ิี่๋ื์ัึ๊้็" + "ฺุู" + "ํ๎" + "ำ":
            draw_char = "." + char

        char_width, char_height = get_char_size(draw_char, font)
        x, y, img, draw, max_height = handle_new_line(
            (x, y), (char_width, char_height), img, max_height
        )
        x_start = x
        y_start = y
        x_end = x_start + char_width
        y_end = y_start + char_height
        if is_show_box:
            draw.rectangle((x_start, y_start, x_end, y_end), outline="white")
        glyph = Image.new(img.mode, (char_width, char_height))
        glyph_draw = ImageDraw.Draw(glyph)
        glyph_draw.text(
            (adjust[char]["adjust_x"], adjust[char]["adjust_y"]),
            draw_char,
            font=font,
            fill="white",
            anchor="lt",
            spacing=0,
        )

        draw_hide_dot(
            glyph_draw,
            (
                adjust[char]["adjust_x"],
                adjust[char]["adjust_y"],
                adjust[char]["adjust_x"] + char_width,
                adjust[char]["adjust_y"] + char_height,
            ),
            draw_char,
            font,
        )

        if adjust[char].get("rotate"):
            glyph = glyph.rotate(adjust[char]["rotate"], expand=1)
            gw, _ = glyph.size
            img.paste(glyph, (int(x_start - gw // 4), int(y_start)), glyph)
        else:
            img.paste(glyph, (int(x_start), int(y_start)), glyph)

        glyph_coordinates.append(
            {
                "char": char,
                "ascii": thai_ascii_codes[char],
                "x_start": x_start,
                "y_start": y_start,
                "x_end": x_end,
                "y_end": y_end,
            }
        )

        x += char_width + 1

    if img.size[0] != origin_img_size[0] or img.size[1] != origin_img_size[1]:
        print(
            f"UPDATE image size (px): ({origin_img_size[0]} × {origin_img_size[1]}) ⇨ ({img.size[0]} × {img.size[1]})"
        )
        print("WARNING: Game Maybe not support !")

    img.show()

    img.save(output_path)
    update_json_file(json_path, new_json_path, glyph_coordinates, adjust)


def handle_new_line(xy, char_size, img, max_height):
    x, y = xy
    char_width, char_height = char_size
    img_width, img_height = img.size
    max_height = max(max_height, char_height)
    if x + char_width > img_width:
        bottom_margin = 5
        x = 0
        y += max_height + bottom_margin
        max_height = char_height
    if y + char_height > img_height:
        new_img_height = img_height + char_height
        new_img = Image.new(img.mode, (img_width, new_img_height))
        new_img.paste(img, (0, 0))
        img = new_img

    draw = ImageDraw.Draw(img)
    return x, y, img, draw, max_height


def update_json_file(json_path, new_json_path, glyph_coordinates, adjust):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    last_glyph_id = list(data["coord_arr"].keys())[-1]
    last_glyph_id = int(last_glyph_id)
    for i, glyph_coordinate in enumerate(glyph_coordinates):
        glyph_id = last_glyph_id + i + 1
        x_start = glyph_coordinate["x_start"]
        y_start = glyph_coordinate["y_start"]
        x_end = glyph_coordinate["x_end"]
        y_end = glyph_coordinate["y_end"]
        vertical_offset = get_vertical_offset(glyph_coordinate["char"], adjust)
        base_y = 0

        # add glyph_coordinate
        data["coord_arr"][str(glyph_id)] = {
            "char": glyph_coordinate["char"],
            "x_start": x_start,
            "y_start": y_start,
            "x_end": x_end,
            "y_end": y_end,
            "base_x": vertical_offset,
            "base_y": base_y,
        }

        # map glyph and ascii code
        data["ascii_map"][str(glyph_coordinates[i]["ascii"])] = glyph_id

        # update thai digit ascii map with digit glyph
        thai_digit_ascii_codes = list(range(240, 249 + 1))
        digit_glyph_ids = [61] + list(range(52, 60 + 1))
        for th_digit_ascii, digit_glyph_id in zip(
            thai_digit_ascii_codes, digit_glyph_ids
        ):
            data["ascii_map"][str(th_digit_ascii)] = digit_glyph_id

    with open(new_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_adjust(font_path, config=None):
    if config:
        with open(config, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("Load config from:", config)
        return data
    font_name = os.path.splitext(os.path.basename(font_path))[0].lower()
    for s in [" ", "_"]:
        font_name = font_name.replace(s, "-")
    json_path = f"config/{font_name}.json"
    print("Load config from:", json_path)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


#! You must Custom Modify for different Font & Font Size
def get_vertical_offset(char, adjust):
    vertical_offset = adjust[char].get("vertical_offset")
    if vertical_offset:
        return int(vertical_offset)

    default_vertical_offset = {
        "่๋๊้์": [25, 26, 27],  # Top vowels and tone mark
        "ีืิึ็ั": [24],  # Top vowels
        "ุู": [4],  # Bottom vowels
        "ไใโ": [26, 27, 28],  # Tall vowels
        "ปฝฬฟำ": [24],  # Tall Char and vowels
    }

    for k, v in default_vertical_offset.items():
        if char in k:
            return random.choice(v)
    return random.choice([18, 19])


def add_thai_glyph(
    bmp_path, json_path, font_path, font_size=32, is_show_box=False, config=None
):
    filename = os.path.splitext(os.path.basename(bmp_path))[0].split(".")[0]
    new_name = f"data/Thai/{filename}_with_thai_glyphs"
    output_path = f"{new_name}.bmp"
    new_json_path = f"{new_name}.json"

    THAI_CHARACTER = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลฦวศษสหฬอฮฯะัาำิีึืฺุู฿เแโใไๅๆ็่้๊๋์ํ"
    print("Text length:", len(THAI_CHARACTER))

    position = get_start_position(json_path)

    append_thai_glyphs(
        bmp_path,
        output_path,
        font_path,
        font_size,
        THAI_CHARACTER,
        position,
        json_path,
        new_json_path,
        is_show_box,
        config,
    )


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="""
Add Thai Glyph to BMP & JSON: ex.

* python add_thai_glyph.py data/English/bagel_lin.dff.bmp  data/English/bagel_lin.dff.json Sriracha-Regular.ttf --font-size 26

* python add_thai_glyph.py data/English/bagel_lin.dff.bmp  data/English/bagel_lin.dff.json Sriracha-Regular.ttf --font-size 26 --show-box

File will save in data/Thai/*_with_thai_glyphs.json & data/Thai/*_with_thai_glyphs.bmp
                                  
"""
    )
    arg_parser.add_argument("bmp_path")
    arg_parser.add_argument("json_path")
    arg_parser.add_argument("font_path")
    arg_parser.add_argument("--font-size", type=int, default=26)
    arg_parser.add_argument("--show-box", action="store_true", default=False)
    arg_parser.add_argument("--config", type=str)
    args = arg_parser.parse_args()
    add_thai_glyph(
        args.bmp_path,
        args.json_path,
        args.font_path,
        args.font_size,
        args.show_box,
        args.config,
    )
