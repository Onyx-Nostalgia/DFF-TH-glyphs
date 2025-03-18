<div align="center">
<h1>🧠 DoubleFine Font Parser (add Thai glyphs) 🧠</h1>

<img src="http://ForTheBadge.com/images/badges/made-with-python.svg"/>
<br>
<img src="https://raw.githubusercontent.com/Onyx-Nostalgia/DFF-TH-glyphs/refs/heads/main/data/Thai/bagel_lin_with_thai_glyphs.bmp"/>

<a href="https://github.com/Onyx-Nostalgia/DFF-TH-glyphs/blob/main/README.md">EN</a>
 | <b>TH</b>

</div>

---

Project ต่อยอดจาก [TrupSteam/DFF_Parser](https://github.com/TrupSteam/DFF_Parser) โดยจะเป็นการแก้ไฟล์ BMP และไฟล์ JSON ที่ได้จากการ unpack_font โดยจะเพิ่มตัวอักษรของภาษาไทยเข้าไป

## 🚀 Step of my journey
1. 🔍 หาเลือก Font ที่ต้องการจะนำมาใช้ในเกม ในที่นี้จะใช้ Font: `Sriracha-Regular.ttf` จาก [_Google Font_](https://fonts.google.com/specimen/Sriracha?preview.text=%E0%B9%80%E0%B8%81%E0%B8%A1%E0%B9%84%E0%B8%8B%E0%B9%82%E0%B8%84%E0%B8%99%E0%B8%AD%E0%B8%97%20%E0%B8%8B%E0%B8%B2%E0%B8%8A%E0%B9%88%E0%B8%B2%20%E0%B9%84%E0%B8%99%E0%B8%99%E0%B9%8C%20%E0%B9%82%E0%B8%84%E0%B9%89%E0%B8%8A%20%E0%B9%81%E0%B8%84%E0%B8%A1%E0%B8%9B%E0%B9%8C%20%E0%B9%80%E0%B8%A3%E0%B8%B4%E0%B9%88%E0%B8%A1%E0%B9%80%E0%B8%81%E0%B8%A1%20%E0%B8%AA%E0%B8%A7%E0%B8%B1%E0%B8%AA%E0%B8%94%E0%B8%B5%E0%B8%84%E0%B8%A3%E0%B8%B1%E0%B8%9A%20%E0%B8%9E%E0%B8%A5%E0%B8%B1%E0%B8%87%E0%B8%88%E0%B8%B4%E0%B8%95)
2. 🛠️ สร้างไฟล์ config ตัวอักษรไทย เพื่อกำหนด config ของตัวอักษรไทย เนื่องจากแต่ละตัวอักษรอาจไม่ได้อยู่ในตำแหน่งที่ต้องการ จึงต้องมีการปรับค่า x, y เสริมเข้าไป
```bash
python tools/create_thai_glyph_config.py Sriracha-Regular.ttf
```
3. ✏️ เพิ่มตัวอักษรไทยในไฟล์ BMP และ JSON ที่มีอยู่ ขั้นตอนนี้อาจต้องปรับตำแหน่งตัวอักษรให้เหมาะสม
```bash
python add_thai_glyph.py data/English/bagel_lin.dff.bmp  data/English/bagel_lin.dff.json Sriracha-Regular.ttf
```
และในกรณีเดียวกันกับ `RazNotebook_lin`   
```bash
python add_thai_glyph.py data/English/RazNotebook_lin.dff.bmp  data/English/RazNotebook_lin.dff.json Sriracha-Regular.ttf
```
4. 📦 เมื่อได้ไฟล์ BMP และ JSON ที่มีตัวอักษรไทยแล้ว `data/Thai/***_with_thai_glyphs` นำมา pack เป็น DFF ด้วยคำสั่ง
```bash
script/pack_font.sh
``` 
> [!Important]
> * ❗ อย่าลืมแก้ไข `/path/of/file/Games/psychonauts/` ใน [[script/pack_font.sh](https://github.com/Onyx-Nostalgia/DFF-TH-glyphs/tree/main/script/pack_font.sh)] ให้ตรงกับ path เกมในเครื่องของคุณ
> * 💾 ควรสำรองไฟล์ DFF ของเกมไว้ก่อน

> [!NOTE]
> หากมีปัญหา permission ในการใช้งาน ลองใช้ `chmod +x script/*` และรันคำสั่งอีกครั้ง

5. 🌐 แปลไฟล์บทสนทนาต่างๆ ของเกมให้เป็นภาษาไทยโดยใช้ [psychonauts-TH-translation](https://github.com/Onyx-Nostalgia/psychonauts-TH-translation)
6. 🕹️ เข้าเกมเพื่อทดสอบ

## 🖼️ เพิ่มตัวอักษรไทยในไฟล์ BMP และ JSON
ตัวอย่างคำสั่ง 

```bash
python add_thai_glyph.py data/English/bagel_lin.dff.bmp data/English/bagel_lin.dff.json Sriracha-Regular.ttf
```
### --font-size
กำหนดขนาด Font ได้ โดยใช้ `--font-size` Default คือ **26**
```bash
python add_thai_glyph.py data/English/bagel_lin.dff.bmp data/English/bagel_lin.dff.json Sriracha-Regular.ttf --font-size 26
```
### --show-box 
แสดงกรอบ Bounding Box ของแต่ละตัวอักษรได้โดยใช้ `--show-box` มีประโยชน์ในการวางตำแหน่งตัวอักษรให้ตรงกับตำแหน่ง
```bash
python add_thai_glyph.py data/English/bagel_lin.dff.bmp data/English/bagel_lin.dff.json Sriracha-Regular.ttf --show-box 
```
ภาพที่ได้จะเป็นแบบนี้

![image](https://raw.githubusercontent.com/Onyx-Nostalgia/DFF-TH-glyphs/refs/heads/main/data/Thai/bagel_lin_with_thai_glyphs_show_box.bmp)

## 📝 Thai glyph config File

เนื่องจากตัวอักษรของแต่ละ Font จะไม่ค่อยตรงกรอบและตำแหน่งที่ต้องการ ดังนั้นคุณจึงต้องมีไฟล์นี้ในการปรับ config ของแต่ละตัวอักษร และในบางกรณีการปรับขนาดตัวอักษรก็อาจต้องปรับค่าใน Config พวกนี้ด้วย

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
| **adjust_x**        | เลื่อนเสริมตำแหน่งตามแนวแกน x ค่าสูงจะเลื่อนไปทางขวา               |
| **adjust_y**        | เลื่อนเสริมตำแหน่งตามแนวแกน y ค่าสูงจะเลื่อนลงไปด้านล่าง             |
| **vertical_offset** | ปรับตำแหน่งความสูงของตัวอักษรในเกม ค่าสูงจะยิ่งทำให้ตัวอักษรในเกมอยู่สูงขึ้น |
| **rotate**          | เอียงตัวอักษรตามองศาที่กำหนด                                    |

### สร้างไฟล์ด้วยคำสั่ง

สามารถสร้างได้โดย
```bash
python tools/create_thai_glyph_config.py Sriracha-Regular.ttf
```
#### --replace
กรณีต้องการสร้างไฟล์ใหม่ทับไฟล์ที่มีอยู่ ให้ใช้ `-w` หรือ `--overwrite` หรือ `--replace`
```bash
python tools/create_thai_glyph_config.py Sriracha-Regular.ttf -w
```

## 🛠️ Tools เพิ่มเติม

### DFF analysis
แสดงโครงสร้างไฟล์ DFF มีประโยชน์ในการดูว่าข้อมูล Binary ตำแหน่งไหนเก็บข้อมูลเกี่ยวกับอะไรไว้

```bash
python tools/dff_analysis.py data/English/RazNotebook_lin.dff
```
ผลลัพธ์จะเก็บไว้ใน **_/docs/DFF binary structure/{DFF_FILENAME}_** 

เช่น
[/docs/DFF binary structure/RazNotebook_lin](https://github.com/Onyx-Nostalgia/DFF-TH-glyphs/tree/main/docs/DFF%20binary%20structure/RazNotebook_lin)

### display json mapping
กรณีต้องการทราบว่า Json ที่ได้จากการ unpack font เป็นตัวอักษรใด หรือ coord เชื่อมกับ ascii code ใด แบบให้ดูง่ายๆ
```bash
python tools/display_json_mapping.py data/English/RazNotebook_lin.dff.json --mode coord
```
ผลลัพธ์ใน terminal
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
mode ในการแสดงผลมี 2 mode คือ `coord` เป็นค่า default และ `ascii`

`--mode ascii` จะให้ผลลัพธ์ดังนี้ (ascii_map จะมีค่า coord_arr ที่ default คือ  glyph_id=0 หรือ 'a')
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

## 🥲 Limitation
- เนื่องจากไม่มีค่า spacing ของตัวอักษรให้ปรับ ทำให้ตัวอักษรไทยในเกมจะแสดงผลออกมาไม่สวยงามนัก (1 ตัวอักษรจะแสดงออกมาเป็น 1 glyph ต่อๆ กัน) ดังนั้นพวกสระและวรรณยุกต์ ที่ควรจะอยู่ด้านบนหรือล่างพยัญชนะจะมาต่อข้างๆแทน 😭
- หากคุณปรับขนาดตัวอักษรใหญ่เกินไปจนภาพ BMP ที่ได้เกิน **512 x 256 px** อาจส่งผลให้ตัวเกมไม่รองรับและใช้งานไม่ได้
