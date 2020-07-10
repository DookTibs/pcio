import csv
from PIL import Image, ImageDraw, ImageFont

factor = 1
width = 103 * factor
height = 160 * factor

red = "#FF0000"
yellow = "#FFFF00"
blue = "#0000FF"
black = "#000000"
white = "#FFFFFF"

center_size = 80
corner_size = 28

def draw_ruler(max_val):
    box_dim = 10
    font_size = 9
    y_wiggle = 1

    ref_width = box_dim * max_val
    ref_height = box_dim

    svg = f'<svg viewBox="0 0 {ref_width} {ref_height}" xmlns="http://www.w3.org/2000/svg">\n'


    drawn = 0
    x = 0
    y = 0
    bg_colors = [ blue, white ]
    fg_colors = [ white, blue ]
    for i in range(1, max_val+1):
        bg_color = bg_colors[i%len(bg_colors)]
        fg_color = fg_colors[i%len(fg_colors)]
        print(f"box {i} ({fg_color} on {bg_color})")

        svg += f'\t<rect x="{x}" y="{y}" width="{box_dim}" height="{box_dim}" fill="{bg_color}" stroke="{black}" />\n'
        svg += f'\t<text x="{x + (box_dim / 2)}" y="{y + (box_dim / 2) + y_wiggle}" fill="{fg_color}" font-size="{font_size}" text-anchor="middle" alignment-baseline="middle">{i}</text>\n'

        x += box_dim

    svg += '</svg>'

    with open(f"../svg/ruler_1_{max_val}.svg", 'w') as writer:
        writer.write(svg)

if __name__ == "__main__":
    draw_ruler(15)
