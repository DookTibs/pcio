from PIL import Image, ImageDraw, ImageFont

width = 103
height = 161

pink = "#BB4F7E"
blue = "#60A1BF"
orange = "#CF8335"
green = "#88AB4E"

def draw_card(label, background_color, filename):
    img = Image.new("RGB", (width, height), color = background_color)

    # draw the big # in the middle
    center_size = 64
    corner_size = 22
    big_font = ImageFont.truetype("/Library/Fonts/Arial.ttf", center_size)
    little_font = ImageFont.truetype("/Library/Fonts/Arial.ttf", corner_size)

    d = ImageDraw.Draw(img)

    center_size = d.textsize(label, font=big_font)
    d.text(((width / 2) - (center_size[0]/2), (height / 2) - (center_size[1]/2)), label, fill="black", font=big_font, align="center")


    # draw the small number in the upper left
    offset = 3
    center_size = d.textsize(label, font=little_font)
    d.text((offset, offset), label, fill="black", font=little_font)
    # d.text((width - offset - center_size[0], offset), label, fill="black", font=little_font)
    # d.text((offset, height - (offset*2) - center_size[1]), label, fill="black", font=little_font)
    # d.text((width - offset - center_size[0], height - (offset*2) - center_size[1]), label, fill="black", font=little_font)

    """
    icon_img = Image.open("assets/time_palatrix/delorean.jpg")
    thumbnail_size = 25
    icon_img.thumbnail((thumbnail_size, thumbnail_size), Image.ANTIALIAS)
    img.paste(icon_img, (offset, 30))
    """


    img.save(filename)

if __name__ == "__main__":
    color_names = [ "pink", "blue", "orange", "green" ]
    i = 0
    for color in [ pink, blue, orange, green ]:
        color_name = color_names[i]

        for rank in range(0,12):
            # print(f"in here, i={i}, color={color}, rank={rank}")
            card_rank = str(rank+1)
            zeroed_rank = "0" + card_rank if rank < 9 else card_rank
            filename = f"../cards/{color_name}{zeroed_rank}.png"
            draw_card(card_rank, color, filename)

        i += 1
