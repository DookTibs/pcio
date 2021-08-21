import csv
from PIL import Image, ImageDraw, ImageFont

print("THIS ONE WAS NEVER FINISHED!!!")

factor = 1
width = 103 * factor
height = 160 * factor

red = "#FF0000"
yellow = "#FFFF00"
blue = "#0000FF"
cyan = "#00FFFF"
green = "#00FF00"
black = "#000000"
white = "#FFFFFF"

center_size = 80
corner_size = 28

def draw_card(label, background_color, text_color, filename):
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

    svg += '</svg>'

    # print(svg)

    with open(filename, 'w') as writer:
        writer.write(svg)


if __name__ == "__main__":
    csv_rows = []
    csv_rows.append(("label","image"))
    i = 0

    cards = [
    ]

    for i in range(5, 19):
        cards.append({ "rank": i, "suit": "red", "bg_color": red, "text_color": black })

    for i in range(4, 17):
        cards.append({ "rank": i, "suit": "blue", "bg_color": cyan, "text_color": black })

    for i in range(3, 15):
        cards.append({ "rank": i, "suit": "green", "bg_color": green, "text_color": black })

    for i in range(1, 14):
        cards.append({ "rank": i, "suit": "yellow", "bg_color": yellow, "text_color": black })

    for card in cards:
        card_rank = card.get("rank")
        card_color = card.get("bg_color")
        text_color = card.get("text_color")
        suit = card.get("suit")
        zeroed_rank = "0" + str(card_rank) if card_rank < 10 else str(card_rank)
        filename = f"../cards/potatoman_{suit}_{zeroed_rank}.svg"
        draw_card(card_rank, card_color, text_color, filename)
        csv_rows.append((f"potatoman_{suit}_{zeroed_rank}",f"https://raw.githubusercontent.com/DookTibs/pcio/master/potato_man/cards/potatoman_{suit}_{zeroed_rank}.svg"))


    if len(csv_rows) > 0:
        with open("../cards/cards.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(csv_rows)
