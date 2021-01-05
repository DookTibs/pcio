from math import ceil

from hexgrid import HexGrid

# generate svg's for Irish Gauge for playing on playingcards.io
# makes:
# a board (board on pcio)
# little squares for trains (cards on pcio)
# slightly bigger squares for special interest/dividend cubes (cards on pcio)
# cards for shares (cards on pcio)

sea = "#62887C"
width=1400
height=950

interests = [
    {"name": "black", "color": "black" },
    {"name": "pink", "color": "#E15C96" },
    {"name": "white", "color": "#947319" }, # actually more like a tan/brown, to make it easier to distinguish between 
                                            # interest cubes and empty card containers on pcio
]

companies = [
    {
        "name": "Cork, Bandon &amp; South Coast Railway",
        "abbrev": "CBSC",
        "readable": "yellow",
        "color": "#F9EB68",
        "shares": [ 7, 12, 17 ]
    },
    {
        "name": "Waterford, Limerick &amp; Western Railway",
        "abbrev": "WLW",
        "readable": "purple",
        "color": "#7668A1",
        "text_color": "white",
        "shares": [ 5, 10, 15, 19 ]
    },
    {
        "name": "Belfast &amp; County Down Railway",
        "abbrev": "BCD",
        "readable": "orange",
        "color": "#EB933E",
        "shares": [ 8, 13 ]
    },
    {
        "name": "Great Southern &amp; Western Railway",
        "abbrev": "GSW",
        "readable": "blue",
        "color": "#76C8E7",
        "shares": [ 4, 9, 14, 18 ]
    },
    {
        "name": "Midland Great Western Railway",
        "abbrev": "MGW",
        "readable": "red",
        "color": "#A62F2E",
        "text_color": "white",
        "shares": [ 6, 11, 16 ]
    }
]

def init_svg(w, h, bg = None):
    if bg is None:
        return f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
    else:
        return f'<svg style="background-color: {bg}" xmlns="http://www.w3.org/2000/svg" version="1.1" width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns:xlink="http://www.w3.org/1999/xlink">\n'

svg = init_svg(width, height, sea)

light_green = "#9EA76E"
dark_green = "#6D9160"
red = "red"
black = "black"

radius = 80
hg = HexGrid(HexGrid.POINTY_ON_TOP, 50, 1)

terrain_border_size = radius * .2
city_border_size = radius * .05

# super dirty function to position the "all values of shares" elements on the right side of a card
def get_card_y_position(idx, all_vals, h):
    middle_idx = int(len(all_vals) / 2)

    if len(all_vals) % 2 == 0:
        middle_idx -= .5

    offset_amount = 23
    if len(all_vals) == 2:
        offset_amount = 15
    elif len(all_vals) == 4:
        if idx < middle_idx:
            adj_factor = ceil(middle_idx - idx)
        else:
            adj_factor = ceil(idx - middle_idx)
        offset_amount = (8 * adj_factor) + (10 * (adj_factor-1))


    rv = h/2
    if (idx == middle_idx):
        pass
    elif idx < middle_idx:
        rv -= offset_amount
    elif idx > middle_idx:
        rv += offset_amount

    return rv

def draw_text(t, size, x, y, anchor, alignment, color="black"):
    return f'\t<text fill="{color}" font-size="{size}px" x="{x}" y="{y}" text-anchor="{anchor}" alignment-baseline="{alignment}">{t}</text>\n'

def draw_normal_hex(coords):
    return hg.generate_colored_hex_svg_at_slot(coords, light_green)

def draw_terrain_hex(coords):
    return hg.generate_bordered_hex_svg_at_slot(coords, light_green, dark_green, terrain_border_size)

def draw_city_hex(coords, city_name, is_bonus = False):
    city_hex = hg.generate_bordered_hex_svg_at_slot(coords, red if is_bonus else black, dark_green, city_border_size)
    origin_x, origin_y = hg.get_origin_for_coords(coords[0], coords[1])
    city_label = f'<text text-anchor="middle" x="{origin_x}" y="{origin_y + 25}">{city_name}</text>'
    return city_hex + city_label

row = 0
svg += draw_terrain_hex((0,row))
svg += draw_terrain_hex((1,row))
svg += draw_city_hex((2,row), "Belfast", True)
svg += draw_terrain_hex((3,row))
svg += draw_terrain_hex((4,row))
svg += draw_city_hex((9,row), "Wicklow")
svg += draw_city_hex((10,row), "Arklow")

row += 1
svg += draw_normal_hex((0,row))
svg += draw_normal_hex((1,row))
svg += draw_normal_hex((2,row))
svg += draw_normal_hex((3,row))
svg += draw_normal_hex((4,row))
svg += draw_city_hex((5,row), "Drogheda")
svg += draw_normal_hex((6,row))
svg += draw_city_hex((7,row), "Dublin", True)
svg += draw_terrain_hex((8,row))
svg += draw_terrain_hex((9,row))
svg += draw_normal_hex((10,row))
svg += draw_normal_hex((11,row))

row += 1
svg += draw_normal_hex((0,row))
svg += draw_normal_hex((1,row))
svg += draw_normal_hex((2,row))
svg += draw_terrain_hex((3,row))
svg += draw_normal_hex((4,row))
svg += draw_normal_hex((5,row))
svg += draw_normal_hex((6,row))
svg += draw_normal_hex((7,row))
svg += draw_normal_hex((8,row))
svg += draw_normal_hex((9,row))
svg += draw_normal_hex((10,row))
svg += draw_terrain_hex((11,row))
svg += draw_normal_hex((12,row))

row += 1
svg += draw_terrain_hex((0,row))
svg += draw_terrain_hex((1,row))
svg += draw_terrain_hex((2,row))
svg += draw_city_hex((3,row), "Monaghan")
svg += draw_normal_hex((4,row))
svg += draw_normal_hex((5,row))
svg += draw_normal_hex((6,row))
svg += draw_normal_hex((7,row))
svg += draw_normal_hex((8,row))
svg += draw_terrain_hex((9,row))
svg += draw_normal_hex((10,row))
svg += draw_city_hex((11,row), "New Ross")
svg += draw_city_hex((12,row), "Waterford")

row += 1
svg += draw_normal_hex((0,row))
svg += draw_city_hex((1,row), "Derry")
svg += draw_normal_hex((2,row))
svg += draw_terrain_hex((3,row))
svg += draw_normal_hex((4,row))
svg += draw_normal_hex((5,row))
svg += draw_normal_hex((6,row))
svg += draw_normal_hex((7,row))
svg += draw_normal_hex((8,row))
svg += draw_normal_hex((9,row))
svg += draw_normal_hex((10,row))
svg += draw_city_hex((11,row), "Kilkenny")
svg += draw_normal_hex((12,row))

row += 1
svg += draw_normal_hex((0,row))
svg += draw_terrain_hex((1,row))
svg += draw_normal_hex((2,row))
svg += draw_normal_hex((3,row))
svg += draw_normal_hex((4,row))
svg += draw_normal_hex((5,row))
svg += draw_normal_hex((6,row))
svg += draw_city_hex((7,row), "Tullamore")
svg += draw_terrain_hex((8,row))
svg += draw_normal_hex((9,row))
svg += draw_normal_hex((10,row))
svg += draw_normal_hex((11,row))
svg += draw_terrain_hex((12,row))

row += 1
svg += draw_terrain_hex((0,row))
svg += draw_terrain_hex((1,row))
svg += draw_normal_hex((2,row))
svg += draw_normal_hex((3,row))
svg += draw_normal_hex((4,row))
svg += draw_normal_hex((5,row))
svg += draw_normal_hex((6,row))
svg += draw_normal_hex((7,row))
svg += draw_normal_hex((8,row))
svg += draw_normal_hex((9,row))
svg += draw_terrain_hex((10,row))
svg += draw_normal_hex((11,row))
svg += draw_normal_hex((12,row))
svg += draw_normal_hex((13,row))

row += 1
svg += draw_normal_hex((0,row))
svg += draw_normal_hex((1,row))
svg += draw_normal_hex((3,row))
svg += draw_normal_hex((4,row))
svg += draw_normal_hex((5,row))
svg += draw_normal_hex((6,row))
svg += draw_normal_hex((7,row))
svg += draw_normal_hex((8,row))
svg += draw_normal_hex((9,row))
svg += draw_terrain_hex((10,row))
svg += draw_normal_hex((11,row))
svg += draw_normal_hex((12,row))
svg += draw_normal_hex((13,row))

row += 1
svg += draw_city_hex((3,row), "Sligo")
svg += draw_terrain_hex((4,row))
svg += draw_normal_hex((5,row))
svg += draw_normal_hex((6,row))
svg += draw_normal_hex((7,row))
svg += draw_normal_hex((8,row))
svg += draw_normal_hex((9,row))
svg += draw_normal_hex((10,row))
svg += draw_city_hex((11,row), "Limerick")
svg += draw_normal_hex((12,row))
svg += draw_terrain_hex((13,row))
svg += draw_city_hex((14,row), "Cork")

row += 1
svg += draw_terrain_hex((4,row))
svg += draw_normal_hex((5,row))
svg += draw_normal_hex((6,row))
svg += draw_city_hex((7,row), "Galway", True)
svg += draw_normal_hex((9,row))
svg += draw_city_hex((10,row), "Shannon")
svg += draw_normal_hex((11,row))
svg += draw_terrain_hex((12,row))
svg += draw_terrain_hex((13,row))
svg += draw_normal_hex((14,row))

row += 1
svg += draw_normal_hex((4,row))
svg += draw_city_hex((5,row), "Castlebar")
svg += draw_normal_hex((6,row))
svg += draw_normal_hex((7,row))
svg += draw_normal_hex((8,row))
svg += draw_normal_hex((10,row))
svg += draw_normal_hex((11,row))
svg += draw_terrain_hex((12,row))
svg += draw_terrain_hex((13,row))
svg += draw_terrain_hex((14,row))
svg += draw_terrain_hex((15,row))

row += 1
svg += draw_terrain_hex((4,row))
svg += draw_terrain_hex((5,row))
svg += draw_terrain_hex((6,row))
svg += draw_normal_hex((7,row))
svg += draw_normal_hex((11,row))
svg += draw_normal_hex((12,row))
svg += draw_city_hex((13,row), "Killarney")
svg += draw_terrain_hex((14,row))

# legend
text_offset = 1320
small_hg = HexGrid(HexGrid.POINTY_ON_TOP, 30, 0)
svg += draw_text('BUILD COSTS', 16, 1340, 15, "middle", "middle", "white")
svg += small_hg.raw_draw(1250, 55, { "fill": light_green }, 30)
svg += draw_text('1 ; 1.5', 20, text_offset, 55, "left", "middle", "white")

svg += small_hg.raw_draw(1250, 120, { "fill": light_green }, 30)
svg += small_hg.raw_draw(1250, 120, { "fill": dark_green }, 20)
svg += draw_text('2 ; N/A', 20, text_offset, 120, "left", "middle", "white")

svg += small_hg.raw_draw(1220, 185, { "fill": black }, 30)
svg += small_hg.raw_draw(1220, 185, { "fill": dark_green }, 28)
svg += small_hg.raw_draw(1280, 185, { "fill": red }, 30)
svg += small_hg.raw_draw(1280, 185, { "fill": dark_green }, 28)
svg += draw_text('1 ; 1.5', 20, text_offset, 185, "left", "middle", "white")

svg += draw_text('&#163;12 Bonus for all', 20, 1200, 250, "left", "middle", "white")
svg += draw_text('red cities connected', 20, 1200, 270, "left", "middle", "white")

svg += draw_text('Town = no interest cube', 20, 1200, 300, "left", "middle", "white")
svg += draw_text('&#163;2 Income', 20, 1200, 320, "left", "middle", "white")

svg += draw_text('City = interest cube', 20, 1200, 350, "left", "middle", "white")
svg += draw_text('&#163;4 Income', 20, 1200, 370, "left", "middle", "white")

svg += draw_text('Lines only pay if either:', 20, 1200, 400, "left", "middle", "white")
svg += draw_text('   * paying city + town', 20, 1200, 420, "left", "middle", "white")
svg += draw_text('   * 2 paying cities', 20, 1200, 440, "left", "middle", "white")

svg += '</svg>'

with open("../board.svg", "w") as text_file:
    text_file.write(svg)

interest_size = 35
for interest in interests:
    name = interest.get("name")
    color = interest.get("color")

    svg = init_svg(interest_size, interest_size)
    svg += f'\t<rect x="0" y="0" width="{interest_size}" height="{interest_size}" fill="{color}"/>\n'
    svg += '</svg>'

    with open(f"../dividend_{name}.svg", "w") as text_file:
        text_file.write(svg)

train_size = 20
share_size = (125, 75)
charter_size = (300, 85)
for company in companies:
    name = company.get("name")
    abbrev = company.get("abbrev")
    readable = company.get("readable")
    color = company.get("color")
    text_color = company.get("text_color", "black")
    shares = company.get("shares")

    # make a card svg to represent the trains
    svg = init_svg(train_size, train_size)
    svg += f'\t<rect x="0" y="0" width="{train_size}" height="{train_size}" fill="{color}"/>\n'
    svg += '</svg>'

    with open(f"../train_{readable}.svg", "w") as text_file:
        text_file.write(svg)

    # make a board svg to represent the charter
    svg = init_svg(charter_size[0], charter_size[1])
    svg += f'\t<rect x="0" y="0" width="{charter_size[0]}" height="{charter_size[1]}" fill="{color}"/>\n'
    svg += f'\t<rect x="20" y="0" width="{charter_size[0] - (20*2)}" height="{charter_size[1] - 20}" fill="white"/>\n'
    svg += draw_text(name, 16, charter_size[0] / 2, charter_size[1] - 9, "middle", "middle", text_color)
    svg += '</svg>'

    with open(f"../charter_{readable}.svg", "w") as text_file:
        text_file.write(svg)

    # make card svg's to represent the shares
    share_idx = 1
    for share in shares:
        svg = init_svg(share_size[0], share_size[1])
        svg += f'\t<rect x="0" y="0" width="{share_size[0]}" height="{share_size[1]}" fill="{color}"/>\n'
        price_idx = 0
        svg += draw_text(abbrev, 20, share_size[0] / 2 + 10, share_size[1] / 2, "middle", "middle", text_color)
        for price in shares:
            # draw the big share price on the left hand side of the card
            if share == price:
                svg += draw_text(price, 36, 0, share_size[1] / 2, "start", "middle", text_color)

            # draw all the share values for this company on the right hand side of the card
            svg += draw_text(price, 18, 115, get_card_y_position(price_idx, shares, share_size[1]), "middle", "middle", text_color)
            price_idx += 1
        svg += '</svg>'

        with open(f"../share_{readable}_{share_idx}.svg", "w") as text_file:
            text_file.write(svg)

        share_idx += 1
