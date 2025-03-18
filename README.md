<div align="center">
<h1>🧠 DoubleFine Font Parser (add Thai glyphs) 🧠</h1>

<img src="http://ForTheBadge.com/images/badges/made-with-python.svg"/>
<img src="https://img.shields.io/badge/python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white"/>
<br>
<img src="https://raw.githubusercontent.com/Onyx-Nostalgia/DFF-TH-glyphs/refs/heads/main/data/Thai/bagel_lin_with_thai_glyphs.bmp"/>

<b>EN</b>
 | <a href="https://github.com/Onyx-Nostalgia/DFF-TH-glyphs/blob/main/docs/README-TH.md">TH</a>

</div>

---

This project builds upon [TrupSteam/DFF_Parser](https://github.com/TrupSteam/DFF_Parser) by modifying BMP and JSON files obtained from unpack_font to include Thai characters.

## 🚀 Steps of my journey
1. 🔍 Select the desired font to use in the game. In this case, the font `Sriracha-Regular.ttf` from [_Google Font_](https://fonts.google.com/specimen/Sriracha?preview.text=%E0%B9%80%E0%B8%81%E0%B8%A1%E0%B9%84%E0%B8%8B%E0%B9%82%E0%B8%84%E0%B8%99%E0%B8%AD%E0%B8%97%20%E0%B8%8B%E0%B8%B2%E0%B8%8A%E0%B9%88%E0%B8%B2%20%E0%B9%84%E0%B8%99%E0%B8%99%E0%B9%8C%20%E0%B9%82%E0%B8%84%E0%B9%89%E0%B8%8A%20%E0%B9%81%E0%B8%84%E0%B8%A1%E0%B8%9B%E0%B9%8C%20%E0%B9%80%E0%B8%A3%E0%B8%B4%E0%B9%88%E0%B8%A1%E0%B9%80%E0%B8%81%E0%B8%A1%20%E0%B8%AA%E0%B8%A7%E0%B8%B1%E0%B8%AA%E0%B8%94%E0%B8%B5%E0%B8%84%E0%B8%A3%E0%B8%B1%E0%B8%9A%20%E0%B8%9E%E0%B8%A5%E0%B8%B1%E0%B8%87%E0%B8%88%E0%B8%B4%E0%B8%95)
2. 🛠️ Create a Thai character config file to define the configuration of Thai characters, as each character may not be in the desired position and may require adjustments to x, y values.
```bash
python tools/create_thai_glyph_config.py Sriracha-Regular.ttf
```
3. ✏️ Add Thai characters to the existing BMP and JSON files. This step may require adjusting the character positions to fit properly.
```bash
python add_thai_glyph.py data/English/bagel_lin.dff.bmp  data/English/bagel_lin.dff.json Sriracha-Regular.ttf
```
Similarly for `RazNotebook_lin`
```bash
python add_thai_glyph.py data/English/RazNotebook_lin.dff.bmp  data/English/RazNotebook_lin.dff.json Sriracha-Regular.ttf
```
4. 📦 Once the BMP and JSON files with Thai characters are ready, pack them into DFF using the command
```bash
script/pack_font.sh
``` 
> [!Important]
> * ❗ Don't forget to update the `/path/of/file/Games/psychonauts/` in [[script/pack_font.sh](https://github.com/Onyx-Nostalgia/DFF-TH-glyphs/tree/main/script/pack_font.sh)] to match the game path on your machine.
> * 💾 It's recommended to backup the game's DFF files before proceeding.

> [!NOTE]
> If you encounter permission issues, try using `chmod +x script/*` and rerun the command.

5. 🌐 Translate the game's dialogue files to Thai using [psychonauts-TH-translation](https://github.com/Onyx-Nostalgia/psychonauts-TH-translation)
6. 🕹️ Launch the game to test.

## 🖼️ Adding Thai characters to BMP and JSON files
Example command

```bash
python add_thai_glyph.py data/English/bagel_lin.dff.bmp data/English/bagel_lin.dff.json Sriracha-Regular.ttf
```
### --font-size
Specify the font size using `--font-size`. The default is **26**.
```bash
python add_thai_glyph.py data/English/bagel_lin.dff.bmp data/English/bagel_lin.dff.json Sriracha-Regular.ttf --font-size 26
```
### --show-box 
Display the bounding box of each character using `--show-box`. This is useful for positioning characters accurately.
```bash
python add_thai_glyph.py data/English/bagel_lin.dff.bmp data/English/bagel_lin.dff.json Sriracha-Regular.ttf --show-box 
```
The resulting image will look like this

![image](https://raw.githubusercontent.com/Onyx-Nostalgia/DFF-TH-glyphs/refs/heads/main/data/Thai/bagel_lin_with_thai_glyphs_show_box.bmp)

## 📝 Thai glyph config File

Since each font's characters may not align perfectly, you need this file to adjust the configuration of each character. In some cases, you may also need to adjust the character size in the config.

[config/sriracha-regular.json](https://github.com/Onyx-Nostalgia/DFF-TH-glyphs/blob/main/config/sriracha-regular.json)

```json
{
 "ก": {
        "adjust_x": -2,
        "adjust_y": 0,
        "vertical_offset": 0,
        "rotate":-30
    },
    ...
}
```
|                     |                                                           |
| ------------------- | --------------------------------------------------------- |
| **adjust_x**        | Adjust the position along the x-axis. Higher values move to the right. |
| **adjust_y**        | Adjust the position along the y-axis. Higher values move downwards. |
| **vertical_offset** | Adjust the vertical position of the character in the game. Higher values move the character higher. |
| **rotate**          | Rotate the character by the specified degrees.             |

### Create the file using the command

You can create it by
```bash
python tools/create_thai_glyph_config.py Sriracha-Regular.ttf
```
#### --replace
To overwrite an existing file, use `-w`, `--overwrite`, or `--replace`.
```bash
python tools/create_thai_glyph_config.py Sriracha-Regular.ttf -w
```

## 🛠️ Additional Tools

### DFF analysis
Display the structure of the DFF file, useful for understanding which binary data corresponds to what information.

```bash
python tools/dff_analysis.py data/English/RazNotebook_lin.dff
```
The results will be saved in **_/docs/DFF binary structure/{DFF_FILENAME}_** 

For example
[/docs/DFF binary structure/RazNotebook_lin](https://github.com/Onyx-Nostalgia/DFF-TH-glyphs/tree/main/docs/DFF%20binary%20structure/RazNotebook_lin)

### display json mapping
To understand which character or coordinate corresponds to which ASCII code in the JSON file obtained from unpacking the font, use
```bash
python tools/display_json_mapping.py data/English/RazNotebook_lin.dff.json --mode coord
```
The terminal output will be
```sh
glyph_id='0': _a_ ascii_code=97 w=11 h=14 start_pos:(1,1) end_pos:(12, 15) base:(12,0)
glyph_id='1': _b_ ascii_code=98 w=11 h=24 start_pos:(13,1) end_pos:(24, 25) base:(21,0)
glyph_id='2': _c_ ascii_code=99 w=11 h=14 start_pos:(25,1) end_pos:(36, 15) base:(13,0)
...
glyph_id='170': _ü_ ascii_code=252 w=11 h=18 start_pos:(285,120) end_pos:(296, 138) base:(17,0)
glyph_id='171': _
_ ascii_code=133 w=16 h=4 start_pos:(297,120) end_pos:(313, 124) base:(6,0)
```
#### --mode
There are two modes for displaying the results: `coord` (default) and `ascii`.

`--mode ascii` will produce the following output (ascii_map will have coord_arr with the default value of glyph_id=0 or 'a')
```sh
ascii_code='0': _a_ glyph_id=0 w=11 h=14 start_pos:(1,1) end_pos:(12, 15) base:(12,0)
ascii_code='1': _a_ glyph_id=0 w=11 h=14 start_pos:(1,1) end_pos:(12, 15) base:(12,0)
...
ascii_code='95': ___ glyph_id=76 w=16 h=4 start_pos:(146,58) end_pos:(162, 62) base:(65535,65535)
ascii_code='96': _`_ glyph_id=62 w=8 h=14 start_pos:(454,28) end_pos:(462, 42) base:(28,0)
ascii_code='97': _a_ glyph_id=0 w=11 h=14 start_pos:(1,1) end_pos:(12, 15) base:(12,0)
ascii_code='98': _b_ glyph_id=1 w=11 h=24 start_pos:(13,1) end_pos:(24, 25) 
...
ascii_code='255': _a_ glyph_id=0 w=11 h=14 start_pos:(1,1) end_pos:(12, 15) base:(12,0)

```

## 🥲 Limitations
- Due to the lack of spacing adjustments for characters, Thai characters in the game may not display beautifully (each character will appear as a separate glyph). Therefore, vowels and tone marks that should be above or below consonants will appear next to them instead. 😭
- If you enlarge the characters too much, causing the resulting BMP to exceed **512 x 256 px**, the game may not support and use it.
