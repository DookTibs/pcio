import csv
from PIL import Image, ImageDraw, ImageFont

factor = 1
width = 103 * factor
height = 160 * factor

border_thickness = 3

pink = "#BB4F7E"
blue = "#60A1BF"
orange = "#CF8335"
green = "#88AB4E"

center_size = 80
corner_size = 28

def round_corner(radius, fill):
    """Draw a round corner"""
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
    return corner
 
def round_rectangle(size, radius, fill):
    """Draw a rounded rectangle"""
    width, height = size
    rectangle = Image.new('RGBA', size, fill)
    corner = round_corner(radius, fill)
    rectangle.paste(corner, (0, 0))
    rectangle.paste(corner.rotate(90), (0, height - radius)) # Rotate the corner and paste it
    rectangle.paste(corner.rotate(180), (width - radius, height - radius))
    rectangle.paste(corner.rotate(270), (width - radius, 0))
    return rectangle

def draw_card(label, background_color, filename, card_format):
    if card_format == "png":
        draw_card_png(label, background_color, filename)
    elif card_format == "svg":
        draw_card_svg(label, background_color, filename)

def draw_card_svg(label, background_color, filename):
    # on pcio, set dimensions of card to 103x159, set border=no and rounded=yes options
    stroke_width = 3

    svg = f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">\n'

    svg += f'\t<rect width="{width}" height="{height}" fill="{background_color}" stroke-width="{stroke_width}" stroke="#000000" rx="8" />\n'

    mid_x = width / 2
    mid_y = height / 2

    # big number in middle
    svg += f'\t<text x="{mid_x}" y="{mid_y}" fill="#000000" stroke="#FFFFFF" font-size="{center_size}" text-anchor="middle" alignment-baseline="middle" stroke-width=".7">{label}</text>\n'

    # small number in corner
    corner_pad_x = 11
    corner_pad_y = 14
    svg += f'\t<text x="{stroke_width + corner_pad_x}" y="{stroke_width + corner_pad_y}" fill="#000000" font-size="{corner_size}" text-anchor="middle" alignment-baseline="middle">{label}</text>\n'

    svg += '</svg>'

    print(svg)

    with open(filename, 'w') as writer:
        writer.write(svg)

def draw_card_png(label, background_color, filename):
    # img = Image.new("RGB", (width, height), color = background_color)
    radius = 10
    img = round_rectangle((width, height), radius, "black")

    inset_width = width - (border_thickness*2)
    inset_height = height - (border_thickness*2)
    colored_inset = round_rectangle((inset_width, inset_height), 0, background_color)
    img.paste(colored_inset, (border_thickness, border_thickness))

    # draw the big # in the middle
    big_font = ImageFont.truetype("/Library/Fonts/Arial.ttf", center_size)
    little_font = ImageFont.truetype("/Library/Fonts/Arial.ttf", corner_size)

    d = ImageDraw.Draw(img)

    center_size = d.textsize(label, font=big_font)
    d.text(((width / 2) - (center_size[0]/2), (height / 2) - (center_size[1]/2)), label, fill="black", font=big_font, align="center")


    # draw the small number in the upper left
    offset = 3
    center_size = d.textsize(label, font=little_font)
    d.text((offset, offset), label, fill="black", font=little_font)
    # d.text((width - offset - center_size[0], offset), label, fill="black", font=little_font)
    # d.text((offset, height - (offset*2) - center_size[1]), label, fill="black", font=little_font)
    # d.text((width - offset - center_size[0], height - (offset*2) - center_size[1]), label, fill="black", font=little_font)

    """
    icon_img = Image.open("assets/time_palatrix/delorean.jpg")
    thumbnail_size = 25
    icon_img.thumbnail((thumbnail_size, thumbnail_size), Image.ANTIALIAS)
    img.paste(icon_img, (offset, 30))
    """

    """
    # draw a border
    d.line((0,0,width,0), fill="black")
    """


    img.save(filename)

if __name__ == "__main__":
    csv_rows = []
    csv_rows.append(("label","image"))
    color_names = [ "pink", "blue", "orange", "green" ]
    i = 0

    card_format = "svg"
    for color in [ pink, blue, orange, green ]:
        color_name = color_names[i]

        for rank in range(0,12):
            # print(f"in here, i={i}, color={color}, rank={rank}")
            card_rank = str(rank+1)
            zeroed_rank = "0" + card_rank if rank < 9 else card_rank
            filename = f"../cards/{color_name}{zeroed_rank}.{card_format}"
            draw_card(card_rank, color, filename, card_format)
            csv_rows.append((f"{color_name}_{card_rank}",f"https://raw.githubusercontent.com/DookTibs/pcio/master/time_palatrix/cards/{color_name}{zeroed_rank}.{card_format}"))

        i += 1

    if len(csv_rows) > 0:
        with open("../assets/cards.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(csv_rows)
