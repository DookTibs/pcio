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

def generate_image_embed_tags(icon, x, y, scale_factor = 1, flipped = False):
    # image - just referencing the image tends to not work, either in display or when
    # exporting to png. So instead we read the contents of the image and base64encode it,
    # and include it inline.
    encoded_img = None

    # use maskmen images
    real_or_fake = ""

    # use real wrestlers
    real_or_fake = "_real"

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
    # draw_reference_card(cards)

    if len(csv_rows) > 0:
        with open("../cards/cards.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(csv_rows)
