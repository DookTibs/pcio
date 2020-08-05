import csv
from PIL import Image, ImageDraw, ImageFont

factor = 1
width = 103 * factor
height = 160 * factor

# red = "#FF0000"
# yellow = "#FFFF00"
# blue = "#0000FF"
red = "#CC3839"
yellow = "#DEC86E"
blue = "#4499D6"
black = "#000000"
white = "#FFFFFF"

center_size = 80
corner_size = 28

def draw_reference_card(cards):
    ref_width = 240
    ref_height = 75
    svg = f'<svg viewBox="0 0 {ref_width} {ref_height}" xmlns="http://www.w3.org/2000/svg">\n'

    box_dim = 20

    drawn = 0
    x = 0
    y = 0
    for card in cards:
        points = card.get("points")
        if points > 0:
            background_color = card.get("bg_color")
            text_color = card.get("text_color")
            svg += f'\t<rect x="{x}" y="{y}" width="{box_dim}" height="{box_dim}" fill="{background_color}" stroke="{black}" />\n'
            drawn += 1

            svg += f'\t<text x="{x + (box_dim / 2)}" y="{y + (box_dim / 2)}" fill="{text_color}" font-size="12" text-anchor="middle" alignment-baseline="middle">{card.get("rank")}</text>\n'

            if drawn % 12 == 0:
                y += box_dim * 1.2
                x = 0
            else:
                x += box_dim

    svg += '</svg>'

    with open("../cards/reference_card.svg", 'w') as writer:
        writer.write(svg)

def draw_card(label, background_color, text_color, points, filename):
    # on pcio, set dimensions of card to 103x159, set border=no and rounded=yes options
    stroke_width = 3

    svg = f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">\n'

    svg += f'\t<rect width="{width}" height="{height}" fill="{background_color}" stroke-width="{stroke_width}" stroke="#000000" rx="8" />\n'

    mid_x = width / 2
    mid_y = height / 2

    # big number in middle
    fill = text_color
    stroke = white if text_color == black else black
    svg += f'\t<text x="{mid_x}" y="{mid_y}" fill="{fill}" stroke="{stroke}" font-size="{center_size}" text-anchor="middle" alignment-baseline="middle" stroke-width=".7">{label}</text>\n'

    # small number in corner
    corner_pad_x = 12
    corner_pad_y = 14
    svg += f'\t<text x="{stroke_width + corner_pad_x}" y="{stroke_width + corner_pad_y}" fill="{text_color}" font-size="{corner_size}" text-anchor="middle" alignment-baseline="middle">{label}</text>\n'

    # points
    if points > 0:
        # dot_x = width - stroke_width - corner_pad_x
        # dot_y = stroke_width + corner_pad_y

        dot_x = stroke_width + 5
        dot_y = stroke_width + (corner_pad_y * 3)
        radius = 5

        i = 1
        while i <= points:
            svg += f'\t<circle stroke="white" fill="black" cx="{dot_x}" cy="{dot_y}" r="{radius}"/>'
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
        { "rank": 1, "points": 1, "bg_color": yellow, "text_color": black },
        { "rank": 2, "points": 1, "bg_color": yellow, "text_color": black },
        { "rank": 3, "points": 2, "bg_color": yellow, "text_color": black },
        { "rank": 4, "points": 1, "bg_color": blue, "text_color": white },
        { "rank": 5, "points": 2, "bg_color": yellow, "text_color": black },
        { "rank": 6, "points": 1, "bg_color": blue, "text_color": white },
        { "rank": 7, "points": 3, "bg_color": yellow, "text_color": black },
        { "rank": 8, "points": 2, "bg_color": blue, "text_color": white },
        { "rank": 9, "points": 3, "bg_color": yellow, "text_color": black },
        { "rank": 10, "points": 2, "bg_color": blue, "text_color": white },
        { "rank": 11, "points": 1, "bg_color": red, "text_color": black },
        { "rank": 12, "points": 4, "bg_color": yellow, "text_color": black },
        { "rank": 13, "points": 3, "bg_color": blue, "text_color": white },
        { "rank": 14, "points": 1, "bg_color": red, "text_color": black },
        { "rank": 15, "points": 4, "bg_color": yellow, "text_color": black },
        { "rank": 16, "points": 2, "bg_color": red, "text_color": black },
        { "rank": 17, "points": 3, "bg_color": blue, "text_color": white },
        { "rank": 18, "points": 5, "bg_color": yellow, "text_color": black },
        { "rank": 19, "points": 0, "bg_color": black, "text_color": black },
        { "rank": 20, "points": 4, "bg_color": blue, "text_color": white },
        { "rank": 21, "points": 2, "bg_color": red, "text_color": black },
        { "rank": 22, "points": 5, "bg_color": yellow, "text_color": black },
        { "rank": 23, "points": 3, "bg_color": red, "text_color": black },
        { "rank": 24, "points": 4, "bg_color": blue, "text_color": white },
        { "rank": 25, "points": 6, "bg_color": yellow, "text_color": black },
        { "rank": 26, "points": 3, "bg_color": red, "text_color": black },
        { "rank": 27, "points": 5, "bg_color": blue, "text_color": white },
        { "rank": 28, "points": 6, "bg_color": yellow, "text_color": black },
        { "rank": 29, "points": 4, "bg_color": red, "text_color": black },
        { "rank": 30, "points": 5, "bg_color": blue, "text_color": white },
        { "rank": 31, "points": 4, "bg_color": red, "text_color": black },
        { "rank": 32, "points": 6, "bg_color": blue, "text_color": white },
        { "rank": 33, "points": 5, "bg_color": red, "text_color": black },
        { "rank": 34, "points": 6, "bg_color": blue, "text_color": white },
        { "rank": 35, "points": 5, "bg_color": red, "text_color": black },
        { "rank": 36, "points": 6, "bg_color": red, "text_color": black },
        { "rank": 37, "points": 6, "bg_color": red, "text_color": black }
    ]

    for card in cards:
        card_rank = card.get("rank")
        card_color = card.get("bg_color")
        text_color = card.get("text_color")
        card_points = card.get("points")
        zeroed_rank = "0" + str(card_rank) if card_rank < 10 else str(card_rank)
        filename = f"../cards/bottleimp_{zeroed_rank}.svg"
        draw_card(card_rank, card_color, text_color, card_points, filename)
        csv_rows.append((f"bottleimp_{zeroed_rank}",f"https://raw.githubusercontent.com/DookTibs/pcio/master/bottle_imp/cards/bottleimp_{zeroed_rank}.svg"))

    draw_reference_card(cards)


    if len(csv_rows) > 0:
        with open("../cards/cards.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(csv_rows)
