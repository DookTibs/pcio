import base64, csv

factor = 1
width = 103 * factor
height = 160 * factor

"""
blue = "#1564B3"
red = "#97151C"
green = "#205E42"
black = "#000000"
white = "#FFFFFF"
gold = "#FFD700"
"""
blue = "#0000FF"
red = "#CF4F3D"
green = "#95C990"
black = "#000000"
white = "#FFFFFF"
gold = "#FFD700"
purple = "#923AE7"

center_size = 80
corner_size = 28

def load_external_svg(icon):
    print(f"loading {icon}...")
    try:
        with open(f"../assets/{icon}.svg", "r") as svg_file:
            data = svg_file.read().replace('\n', '')
            return data
    except Exception as e:
        print(f"ERRO: {e}")

def draw_bid(bid_amt, filename):
    stroke_width = 1

    background_color = white
    
    dim = 50
    svg = f'<svg viewBox="0 0 {dim} {dim}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n'

    svg += f'\t<text x="{dim/2}" y="{dim/2}" fill="{black}" font-size="24" text-anchor="middle" alignment-baseline="middle">{bid_amt}</text>\n'

    svg += '</svg>'

    with open(filename, 'w') as writer:
        writer.write(svg)

def draw_card(card_data, filename):
    # on pcio, set dimensions of card to 103x159, set border=no and rounded=yes options
    stroke_width = 3

    background_color = white
    card_val = card_data["rank"]["strength"]
    points = card_data["rank"].get("points")
    suit = card_data["suit"]
    text_color = suit["color"] if suit is not None else purple

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

    # now do bid "cards"
    csv_rows = []
    csv_rows.append(("label","image","back_image"))
    for bid in [ 20, 30, 40 ]:
        filename = f"../generated/chimera_bid_{bid}.svg"
        draw_bid(bid, filename)
        img_url = f"https://raw.githubusercontent.com/DookTibs/pcio/master/chimera/generated/chimera_bid_{bid}.svg"
        csv_rows.append((f"chimera_bid_{bid}",img_url, img_url))

    with open("../generated/bid_cards.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(csv_rows)

    draw_reference_card("../generated/card_ranks.svg")
