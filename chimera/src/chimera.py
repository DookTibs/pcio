import base64, csv

factor = 1
width = 103 * factor
height = 160 * factor

blue = "#1564B3"
red = "#97151C"
green = "#205E42"
black = "#000000"
white = "#FFFFFF"
gold = "#FFD700"

center_size = 80
corner_size = 28

def draw_strength_marker():
    ref_width = 140
    ref_height = 75
    svg = f'<svg viewBox="0 0 {ref_width} {ref_height}" xmlns="http://www.w3.org/2000/svg">\n'

    foo = 10

    svg += f'\t<text x="70" y="{foo}" fill="black" font-size="12" text-anchor="middle" alignment-baseline="middle">UNKNOWN</text>\n'
    foo+=3.5
    svg += f'\t<line x1="0" y1="{foo}" x2="135" y2="{foo}" stroke="black"/>'

    foo = 20

    svg += f'\t<text x="0" y="{foo}" fill="black" font-size="12" text-anchor="left" alignment-baseline="middle">STRONG</text>\n'
    svg += f'\t<text x="100" y="{foo}" fill="black" font-size="12" text-anchor="left" alignment-baseline="middle">WEAK</text>\n'

    line_start = 50
    line_end = 100
    line_y = foo-1
    svg += f'\t<line x1="{line_start}" y1="{line_y}" x2="{line_end}" y2="{line_y}" stroke="black"/>'

    arrow_height = 4
    arrow_draw = 5
    line_start += .3
    line_end -= .3
    svg += f'\t<line x1="{line_start}" y1="{line_y}" x2="{line_start + arrow_draw}" y2="{line_y - arrow_height}" stroke="black"/>'
    svg += f'\t<line x1="{line_start}" y1="{line_y}" x2="{line_start + arrow_draw}" y2="{line_y + arrow_height}" stroke="black"/>'

    svg += f'\t<line x1="{line_end}" y1="{line_y}" x2="{line_end - arrow_draw}" y2="{line_y - arrow_height}" stroke="black"/>'
    svg += f'\t<line x1="{line_end}" y1="{line_y}" x2="{line_end - arrow_draw}" y2="{line_y + arrow_height}" stroke="black"/>'

    svg += '</svg>'

    with open("../cards/strength_board.svg", 'w') as writer:
        writer.write(svg)

"""
def generate_image_embed_tags(icon, x, y, scale_factor = 1, flipped = False):
    # image - just referencing the image tends to not work, either in display or when
    # exporting to png. So instead we read the contents of the image and base64encode it,
    # and include it inline.
    encoded_img = None

    # use maskmen images
    real_or_fake = "_oink"

    # use real wrestlers
    # real_or_fake = "_real"

    try:
        with open(f"../images/{icon}{real_or_fake}.png", "rb") as img_file:
            encoded_img = base64.b64encode(img_file.read())
            encoded_img = encoded_img.decode('utf-8')
    except Exception as e:
        print(f"ERRO: {e}")

    img_w = 80
    img_h = 140

    img_w *= scale_factor
    img_h *= scale_factor

    translate_x = img_w * -.5
    translate_y = img_h * -.5

    # return f'\t<image x="{x}" y="{y}" transform="translate({translate_x}, {translate_y})" xlink:href="data:image/png;base64,{encoded_img}" height="{img_h}" width="{img_w}"/>\n'
    transform = f"translate({translate_x}, {translate_y})"

    return f'\t<image x="{x}" y="{y}" transform="{transform}" xlink:href="data:image/png;base64,{encoded_img}" height="{img_h}" width="{img_w}"/>\n'
"""

def load_external_svg(icon):
    print(f"loading {icon}...")
    try:
        with open(f"../assets/{icon}.svg", "r") as svg_file:
            data = svg_file.read().replace('\n', '')
            return data
    except Exception as e:
        print(f"ERRO: {e}")

def draw_card(card_data, filename):
    # on pcio, set dimensions of card to 103x159, set border=no and rounded=yes options
    stroke_width = 3

    background_color = white
    card_val = card_data["rank"]["strength"]
    points = card_data["rank"].get("points")
    suit = card_data["suit"]
    text_color = suit["color"] if suit is not None else gold

    svg = f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n'

    rank_icon_name = None
    suit_icon_name = None

    svg += f'<defs>\n'
    if "icon" in card_data["rank"]:
        rank_icon_name = card_data["rank"]["icon"]
        icon_data = load_external_svg(rank_icon_name)
        icon_data = icon_data.replace('<svg ', f'<svg id="{rank_icon_name}" ')
        svg += f'{icon_data}'

    if card_data["suit"] is not None and "icon" in card_data["suit"]:
        suit_icon_name = card_data["suit"]["icon"]
        icon_data = load_external_svg(suit_icon_name)
        icon_data = icon_data.replace('<svg ', f'<svg id="{suit_icon_name}" ')
        svg += f'{icon_data}'
    svg += f'</defs>\n'

    svg += f'\t<rect width="{width}" height="{height}" fill="{background_color}" stroke-width="{stroke_width}" stroke="#000000" rx="8" />\n'

    svg += f'\t<text x="2" y="20" fill="{text_color}" font-size="32" text-anchor="left" alignment-baseline="middle">{card_val}</text>\n'

    if points is not None:
        svg += f'\t<text x="2" y="{height-10}" fill="{black}" font-size="16" text-anchor="left" alignment-baseline="middle">+{points}</text>\n'

    if rank_icon_name is not None:
        svg += f'<use x="13" y="0" width="75%" xlink:href="#{rank_icon_name}" fill="{text_color}"/>\n'
    else:
        svg += f'\t<text x="{width/2}" y="{height/2 + 5}" fill="{text_color}" font-size="64" text-anchor="middle" alignment-baseline="middle">{card_val}</text>\n'

    if suit_icon_name is not None:
        svg += f'<use x="3" y="-40" width="15%" xlink:href="#{suit_icon_name}" fill="{text_color}"/>\n'
    """

    mid_x = width / 2
    mid_y = height / 2

    svg += generate_image_embed_tags(suit_name, mid_x, mid_y)
    """

    svg += '</svg>'

    with open(filename, 'w') as writer:
        writer.write(svg)


if __name__ == "__main__":
    csv_rows = []
    csv_rows.append(("label","image"))

    suits = [
        { "name": "red", "color": red, "icon": "round-star" },
        { "name": "blue", "color": blue, "icon": "pagoda" },
        { "name": "green", "color": green, "icon": "amethyst" },
        { "name": "black", "color": black, "icon": "plain-dagger" },
    ]

    ranks = [
        { "strength": "1" },
        { "strength": "2", "points": 10, "icon": "frog" },
        { "strength": "3" },
        { "strength": "4" },
        { "strength": "5" },
        { "strength": "6" },
        { "strength": "7" },
        { "strength": "8" },
        { "strength": "9" },
        { "strength": "10" },
        { "strength": "11", "points": 5, "icon": "cat" },
        { "strength": "12" },
        { "strength": "H", "icon": "swords-power" }
    ]

    """
    suits = [
        { "name": "red", "color": red },
        { "name": "blue", "color": blue }
    ]

    ranks = [
        { "strength": "1" },
        { "strength": "2", "points": 10, "icon": "frog" },
        { "strength": "3" },
        { "strength": "H", "icon": "swords-power" }
    ]
    """

    cards = []

    for suit in suits:
        for rank in ranks:
            cards.append({ "suit": suit, "rank": rank })

    cards.append({ "suit": None, "rank": { "strength": "P", "icon": "lion" }})
    cards.append({ "suit": None, "rank": { "strength": "C", "icon": "tiger-head" }})

    for card in cards:
        print(card)
        suit_name = card["suit"]["name"] if card["suit"] is not None else "special"
        filename = f"../generated/chimera_{suit_name}_{card['rank']['strength']}.svg"
        draw_card(card, filename)
        csv_rows.append((f"chimera_{suit_name}_{card['rank']['strength']}",f"https://raw.githubusercontent.com/DookTibs/pcio/master/chimera/generated/chimera_{suit_name}_{card['rank']['strength']}.svg"))

    with open("../generated/cards.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(csv_rows)
