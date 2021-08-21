import base64, csv

factor = 1
width = 103 * factor
height = 160 * factor

gray = "#4A4A4A"
blue = "#4D64E2"
red = "#D7504A"
purple = "#AF66e7"
orange = "#DAA74B"
green = "#61C668"

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

def draw_card(suit_name, background_color, filename):
    # on pcio, set dimensions of card to 103x159, set border=no and rounded=yes options
    stroke_width = 3

    svg = f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n'

    svg += f'\t<rect width="{width}" height="{height}" fill="{background_color}" stroke-width="{stroke_width}" stroke="#000000" rx="8" />\n'

    mid_x = width / 2
    mid_y = height / 2

    svg += generate_image_embed_tags(suit_name, mid_x, mid_y)

    svg += '</svg>'

    with open(filename, 'w') as writer:
        writer.write(svg)


if __name__ == "__main__":
    csv_rows = []
    csv_rows.append(("label","image"))

    suits = [
        { "name": "red", "color": red },
        { "name": "gray", "color": gray },
        { "name": "blue", "color": blue },
        { "name": "purple", "color": purple },
        { "name": "orange", "color": orange },
        { "name": "green", "color": green },
    ]

    for suit in suits:
        suit_name = suit.get("name")
        card_color = suit.get("color")
        filename = f"../cards/maskmen_{suit_name}.svg"
        draw_card(suit_name, card_color, filename)
        csv_rows.append((f"maskmen_{suit_name}",f"https://raw.githubusercontent.com/DookTibs/pcio/master/maskmen/cards/maskmen_{suit_name}.svg"))

    # todo - spit out a "STRONG <---------> WEAK" reference card
    draw_strength_marker()

    if len(csv_rows) > 0:
        with open("../cards/cards.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(csv_rows)
