# Double Fine Font Parser

These scripts complement the [psychonauts-translator](https://github.com/TrupSteam/psychonauts-translator) project. 
They are needed to change the fonts built into the game.

## Unpack DFF

```
python unpack_font.py RazNotebook_lin.dff
```

The unpacking script converts a dff file into bmp and json. The picture contains letters. The json contains a description of which symbol belongs to which letter. 

For example:

```
 "ascii_map": {
        "0": 0,
```

This means that the ASCII symbol 0x00 corresponds to the first image in the `coord_arr` array.

```
"coord_arr": {
    "0": {
        "x_start": 1,
        "y_start": 1,
        "x_end": 12,
        "y_end": 15,
        "base_x": 12,
        "base_y": 0
    },
```

This means that the symbol with the ordinal number zero (not the asci number, but the number within the array) is inscribed in a rectangle with coordinates (1,1) and (12,15). The remaining two parameters are responsible for the offset of the symbol relative to the text line.

## Pack DFF

```
python pack_font.py RazNotebook_lin.dff.bmp RazNotebook_lin.dff.json
```

This script performs the reverse procedure, creating a font from bmp and json.

# P/S

I have superficially tested the scripts, please write in the Issues if you find any problems. 
