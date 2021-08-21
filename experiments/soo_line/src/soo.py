from math import ceil

from hexgrid import HexGrid

# generate svg's for Ride The Rails for playing on playingcards.io
# makes:
# a board (board on pcio)
# little squares for trains (cards on pcio)
# slightly bigger squares for special interest/dividend cubes (cards on pcio)
# cards for shares (cards on pcio)

bg = "white"
width=1450
height=950

"""
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
"""

# all 1 letters so they align and are fast to type
C = "city"
N = "normal"
R = "rough"
X = None

# each entry in map is a row of the hexgrid
mapboard = [
    [ X, X, X, X, X, X, X, C ],
    [ X, X, X, X, X, R, C ],
    [ X, X, X, X, X, C ], #HOUGHTON
    [ X, X, X, C, R, N ],
    [ X, R, R, R, R, R, C, R, R, X, X, X, X, X, X, X, N, N ], #LANSE
    [ C, R, R, C, R, R, R, R, C, C, X, X, N, N, N, N, N, X, X, C ], # IRONWOOD
    [ X, X, X, X, X, R, C, R, R, N, N, N, C, N, N, N, C, N, N, N ], #CRYSTAL FALLS
    [ X, X, X, X, X, X, R, R, N, C, N, N, N, N, N, N, N, N, N, N ], # GWINN
    [ X, X, X, X, X, X, X, R, N, N, N, N, N, C, N, N, X, N, N, N ], # MANISTIQUE
    [ X, X, X, X, X, X, X, C, N, N, C, X, N, X, X, X, X, X, C ], # IRON MOUNTAIN
    [ X, X, X, X, X, X, X, X, N, N, N ],
    [ X, X, X, X, X, X, X, X, N, N ],
    [ X, X, X, X, X, X, X, X, X, N ],
    [ X, X, X, X, X, X, X, X, C ],
]

# ordered list of cities; keeps the mapboard generation fast
city_data = [
        { "name": "Eagle Harbor" },
        { "name": "Calumet" },
        { "name": "Houghton" },
        { "name": "Ontanagon" },
        { "name": "L'Anse" },
        { "name": "Ironwood", "destination": True },
        { "name": "Watersmeet" },
        { "name": "Negaunee" },
        { "name": "Marquette" },
        { "name": "Sault Ste Marie", "destination": True },
        { "name": "Crystal Falls" },
        { "name": "Munising" },
        { "name": "Newberry" },
        { "name": "Gwinn" },
        { "name": "Manistique" },
        { "name": "Iron Mountain", "destination": True },
        { "name": "Escanaba" },
        { "name": "St. Ignace", "destination": True },
        { "name": "Menominee", "destination": True },
]

def init_svg(w, h, bg = None):
    if bg is None:
        return f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
    else:
        return f'<svg style="background-color: {bg}" xmlns="http://www.w3.org/2000/svg" version="1.1" width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns:xlink="http://www.w3.org/1999/xlink">\n'

svg = init_svg(width, height, bg)

green = "#D5E1C8"
brown = "tan"
white = "white"
red = "red"
black = "black"

hg = HexGrid(HexGrid.POINTY_ON_TOP, 41, 1)

border_factor = 80
city_border_size = border_factor * .1

def draw_text(t, size, x, y, anchor, alignment, color="black"):
    return f'\t<text fill="{color}" font-size="{size}px" x="{x}" y="{y}" text-anchor="{anchor}" alignment-baseline="{alignment}">{t}</text>\n'

def draw_normal_hex(coords):
    # return hg.generate_colored_hex_svg_at_slot(coords, green)
    return hg.generate_bordered_hex_svg_at_slot(coords, black, green, 1)

def draw_rough_hex(coords):
    # return hg.generate_colored_hex_svg_at_slot(coords, brown)
    return hg.generate_bordered_hex_svg_at_slot(coords, black, brown, 1)

def draw_city_hex(coords, city_name = "", destination = False):
    if destination:
        city_hex = hg.generate_bordered_hex_svg_at_slot(coords, red, white, city_border_size)
    else:
        city_hex = hg.generate_bordered_hex_svg_at_slot(coords, black, white, 1)
        # city_hex = hg.generate_colored_hex_svg_at_slot(coords, white)
    origin_x, origin_y = hg.get_origin_for_coords(coords[0], coords[1])
    city_label = draw_text(city_name, 10, origin_x, origin_y + 15, "middle", "middle", "black")
    return city_hex + city_label

city_idx = 0

row = 0
for maprow in mapboard:
    col = 0
    for mapcol in maprow:
        args = {}
        fxn = None
        if mapcol == N:
            fxn = draw_normal_hex
        elif mapcol == C:
            fxn = draw_city_hex
            this_city_data = city_data[city_idx] if city_idx < len(city_data) else {}

            args = { "city_name": this_city_data.get("name", "?"),
                    "destination": this_city_data.get("destination", False),
                    }
            # args = { "city_name": city_data[city_idx]["name"] if city_idx < len(city_data) else '?' }
            city_idx += 1
        elif mapcol == R:
            fxn = draw_rough_hex
        col += 1

        if fxn is not None:
            svg += fxn((col, row), **args)
    row += 1


"""
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
"""

svg += '</svg>'

with open("../board.svg", "w") as text_file:
    text_file.write(svg)

"""
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
"""
