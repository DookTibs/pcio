import csv
from PIL import Image, ImageDraw, ImageFont

factor = 1
width = 103 * factor
height = 160 * factor

red = "#FF0000"
yellow = "#FFFF00"
blue = "#0000FF"
black = "#000000"

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

def draw_card(label, background_color, points, filename):
    # on pcio, set dimensions of card to 103x159, set border=no and rounded=yes options
    stroke_width = 3

    svg = f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">\n'

    svg += f'\t<rect width="{width}" height="{height}" fill="{background_color}" stroke-width="{stroke_width}" stroke="#000000" rx="8" />\n'

    mid_x = width / 2
    mid_y = height / 2

    # big number in middle
    svg += f'\t<text x="{mid_x}" y="{mid_y}" fill="#000000" stroke="#FFFFFF" font-size="{center_size}" text-anchor="middle" alignment-baseline="middle" stroke-width=".7">{label}</text>\n'

    # small number in corner
    corner_pad_x = 12
    corner_pad_y = 14
    svg += f'\t<text x="{stroke_width + corner_pad_x}" y="{stroke_width + corner_pad_y}" fill="#000000" font-size="{corner_size}" text-anchor="middle" alignment-baseline="middle">{label}</text>\n'

    # points
    if points > 0:
        # dot_x = width - stroke_width - corner_pad_x
        # dot_y = stroke_width + corner_pad_y

        dot_x = stroke_width + 5
        dot_y = stroke_width + (corner_pad_y * 3)
        radius = 5

        i = 1
        while i <= points:
            svg += f'\t<circle fill="black" cx="{dot_x}" cy="{dot_y}" r="{radius}"/>'
            dot_y += radius * 2.5
            i += 1


    svg += '</svg>'

    print(svg)

    with open(filename, 'w') as writer:
        writer.write(svg)


if __name__ == "__main__":
    csv_rows = []
    csv_rows.append(("label","image"))
    i = 0

    cards = [
        { "rank": 1, "points": 1, "color": yellow },
        { "rank": 2, "points": 1, "color": yellow },
        { "rank": 3, "points": 2, "color": yellow },
        { "rank": 4, "points": 1, "color": blue },
        { "rank": 5, "points": 2, "color": yellow },
        { "rank": 6, "points": 1, "color": blue },
        { "rank": 7, "points": 3, "color": yellow },
        { "rank": 8, "points": 2, "color": blue },
        { "rank": 9, "points": 3, "color": yellow },
        { "rank": 10, "points": 2, "color": blue },
        { "rank": 11, "points": 1, "color": red },
        { "rank": 12, "points": 4, "color": yellow },
        { "rank": 13, "points": 3, "color": blue },
        { "rank": 14, "points": 1, "color": red },
        { "rank": 15, "points": 4, "color": yellow },
        { "rank": 16, "points": 2, "color": red },
        { "rank": 17, "points": 3, "color": blue },
        { "rank": 18, "points": 5, "color": yellow },
        { "rank": 19, "points": 0, "color": black },
        { "rank": 20, "points": 4, "color": blue },
        { "rank": 21, "points": 2, "color": red },
        { "rank": 22, "points": 5, "color": yellow },
        { "rank": 23, "points": 3, "color": red },
        { "rank": 24, "points": 4, "color": blue },
        { "rank": 25, "points": 6, "color": yellow },
        { "rank": 26, "points": 3, "color": red },
        { "rank": 27, "points": 5, "color": blue },
        { "rank": 28, "points": 6, "color": yellow },
        { "rank": 29, "points": 4, "color": red },
        { "rank": 30, "points": 5, "color": blue },
        { "rank": 31, "points": 4, "color": red },
        { "rank": 32, "points": 6, "color": blue },
        { "rank": 33, "points": 5, "color": red },
        { "rank": 34, "points": 6, "color": blue },
        { "rank": 35, "points": 5, "color": red },
        { "rank": 36, "points": 6, "color": red },
        { "rank": 37, "points": 6, "color": red }
    ]

    for card in cards:
        card_rank = card.get("rank")
        card_color = card.get("color")
        card_points = card.get("points")
        zeroed_rank = "0" + str(card_rank) if card_rank < 10 else str(card_rank)
        filename = f"../cards/bottleimp_{zeroed_rank}.svg"
        draw_card(card_rank, card_color, card_points, filename)
        csv_rows.append((f"bottleimp_{zeroed_rank}",f"https://raw.githubusercontent.com/DookTibs/pcio/master/bottle_imp/cards/{zeroed_rank}.svg"))


    if len(csv_rows) > 0:
        with open("../cards/cards.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(csv_rows)
