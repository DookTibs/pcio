# NOT SURE IF THIS REALLY WORKS OR NOT...
import base64, csv

factor = 1
width = 103 * factor
height = 160 * factor

# blue = "#434290"
# yellow = "#D1A543"
# green = "#95A84A"
blue = "#508FC6"
yellow = "#FEC706"
green = "#97BE49"
black = "#000000"
white = "#FFFFFF"

center_size = 80
corner_size = 28

def load_external_svg(icon):
    # print(f"loading {icon}...")
    try:
        with open(f"../assets/{icon}.svg", "r") as svg_file:
            data = svg_file.read().replace('\n', '')
            return data
    except Exception as e:
        print(f"ERRO: {e}")

def make_objective(num_stars, num_points, required_values):
    return {
        "stars": num_stars,
        "points": num_points,
        "yellow_val": required_values[0],
        "blue_val": required_values[1],
        "green_val": required_values[2]
    }

def draw_objective(card_data, filename_base):
    stroke_width = 3

    # background_color = white
    card_val = card_data["rank"]
    suits = card_data["suits"]

    svg = f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n'

    rank_icon_name = None
    suit_icon_name = None

    svg += f'<defs>\n'
    
    for suit in suits:
        if "icon" in suit:
            suit_icon_name = suit["icon"]
            if suit_icon_name is not None:
                icon_data = load_external_svg(suit_icon_name)
                icon_data = icon_data.replace('<svg ', f'<svg id="{suit_icon_name}" ')
                svg += f'{icon_data}'
    svg += f'</defs>\n'

    # svg += f'\t<rect width="{width}" height="{height}" fill="{background_color}" stroke-width="{stroke_width}" stroke="#000000" rx="8" />\n'

    """
    inset = 10
    if len(suits) == 1:
        svg += f'\t<rect x="{inset}" y="{inset}" width="{width - (inset*2)}" height="{height - (inset*2)}" fill="{suits[0]["color"]}" rx="8" />\n'
    """
    if len(suits) == 1:
        svg += f'\t<rect width="{width}" height="{height}" fill="{suits[0]["color"]}" stroke-width="{stroke_width}" stroke="#000000" rx="8" />\n'
    else:
        svg += f'\t<rect stroke="black" stroke-width="{stroke_width}" width="{width}" x="0" y="{height/2 - 20}" height="40" fill="black" />\n'
        svg += f'\t<rect width="{width}" height="{height/2}" fill="{suits[0]["color"]}" stroke-width="{stroke_width}" stroke="#000000" rx="8" />\n'
        svg += f'\t<rect width="{width}" y="{height/2}" height="{height/2}" fill="{suits[1]["color"]}" stroke-width="{stroke_width}" stroke="#000000" rx="8" />\n'

    # big number
    svg += f'\t<text x="{width/2}" y="{height/2 + 3}" fill="{white}" font-size="56" text-anchor="middle" alignment-baseline="middle" stroke="#000000" stroke-width="0">{card_val}</text>\n'

    suit_counter = 0
    for suit in suits:
        suit_color = suit["color"]
        suit_color = white
        suit_icon = suit["icon"]

        second_suit_offset = 80
        svg += f'\t<text x="2" y="{20 + suit_counter * second_suit_offset}" fill="{suit_color}" font-size="28" text-anchor="left" alignment-baseline="middle">{card_val}</text>\n'

        if suit_icon is not None:
            svg += f'<use x="15" y="{-62 + suit_counter * second_suit_offset}" width="20%" xlink:href="#{suit_icon}" fill="{suit_color}"/>\n'
        suit_counter += 1

    svg += '</svg>'

    with open(filename, 'w') as writer:
        writer.write(svg)

def draw_card(card_data, filename):
    # on pcio, set dimensions of card to 103x159, set border=no and rounded=yes options
    stroke_width = 3

    # background_color = white
    card_val = card_data["rank"]
    suits = card_data["suits"]

    svg = f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n'

    rank_icon_name = None
    suit_icon_name = None

    svg += f'<defs>\n'
    
    for suit in suits:
        if "icon" in suit:
            suit_icon_name = suit["icon"]
            if suit_icon_name is not None:
                icon_data = load_external_svg(suit_icon_name)
                icon_data = icon_data.replace('<svg ', f'<svg id="{suit_icon_name}" ')
                svg += f'{icon_data}'
    svg += f'</defs>\n'

    # svg += f'\t<rect width="{width}" height="{height}" fill="{background_color}" stroke-width="{stroke_width}" stroke="#000000" rx="8" />\n'

    """
    inset = 10
    if len(suits) == 1:
        svg += f'\t<rect x="{inset}" y="{inset}" width="{width - (inset*2)}" height="{height - (inset*2)}" fill="{suits[0]["color"]}" rx="8" />\n'
    """
    if len(suits) == 1:
        svg += f'\t<rect width="{width}" height="{height}" fill="{suits[0]["color"]}" stroke-width="{stroke_width}" stroke="#000000" rx="8" />\n'
    else:
        svg += f'\t<rect stroke="black" stroke-width="{stroke_width}" width="{width}" x="0" y="{height/2 - 20}" height="40" fill="black" />\n'
        svg += f'\t<rect width="{width}" height="{height/2}" fill="{suits[0]["color"]}" stroke-width="{stroke_width}" stroke="#000000" rx="8" />\n'
        svg += f'\t<rect width="{width}" y="{height/2}" height="{height/2}" fill="{suits[1]["color"]}" stroke-width="{stroke_width}" stroke="#000000" rx="8" />\n'

    # big number
    svg += f'\t<text x="{width/2}" y="{height/2 + 3}" fill="{white}" font-size="56" text-anchor="middle" alignment-baseline="middle" stroke="#000000" stroke-width="0">{card_val}</text>\n'

    suit_counter = 0
    for suit in suits:
        suit_color = suit["color"]
        suit_color = white
        suit_icon = suit["icon"]

        second_suit_offset = 80
        svg += f'\t<text x="2" y="{20 + suit_counter * second_suit_offset}" fill="{suit_color}" font-size="28" text-anchor="left" alignment-baseline="middle">{card_val}</text>\n'

        if suit_icon is not None:
            svg += f'<use x="15" y="{-62 + suit_counter * second_suit_offset}" width="20%" xlink:href="#{suit_icon}" fill="{suit_color}"/>\n'
        suit_counter += 1

    svg += '</svg>'

    with open(filename, 'w') as writer:
        writer.write(svg)


if __name__ == "__main__":
    csv_rows = []
    csv_rows.append(("label","image"))

    suits = [
        { "name": "blue", "color": blue, "icon": "talk" },
        { "name": "green", "color": green, "icon": "magnifying-glass" },
        { "name": "yellow", "color": yellow, "icon": "scroll-quill" },
    ]
    black_suit = { "name": "black", "color": black, "icon": None }

    cards = []

    for suit in suits:
        for rank in range(3,10):
            cards.append({ "suits": [ suit ], "rank": rank })

    cards.append({ "suits": [ suits[0], suits[1] ], "rank": 2 })
    cards.append({ "suits": [ suits[0], suits[2] ], "rank": 2 })
    cards.append({ "suits": [ suits[2], suits[1] ], "rank": 2 })

    cards.append({ "suits": [ black_suit ], "rank": 1 })

    card_counter = 1
    for card in cards:
        # print(card)
        filename = f"../generated/tnt_{card_counter}.svg"
        draw_card(card, filename)
        csv_rows.append((f"tnt{card_counter}",f"https://raw.githubusercontent.com/DookTibs/pcio/master/tnt/generated/tnt_{card_counter}.svg"))
        card_counter += 1

    with open("../generated/cards.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(csv_rows)

    objectives = []
    # stars, points, [yellow / blue / green]
    objectives.append(make_objective(1, 2, [ 3, 3, 0 ]))

    # swap height and width
    foo = width
    width = height
    height = width

    card_counter = 1
    for objective in objectives:
        filename_base = f"generated/objective_{card_counter}"
        # draw_objective(objective, filename_base)
        card_counter += 1
