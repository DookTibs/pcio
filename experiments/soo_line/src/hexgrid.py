import math, sys

class HexGrid:
    # this class supports either "flat_on_top" or "pointy_on_top" schemes, set during initialization

    # see also https://www.redblobgames.com/grids/hexagons/
    FLAT_ON_TOP = "flat_on_top"
    """
    FLAT_ON_TOP means the flat edge of the hex is on the top and the farthest left/right bits are pointy. Uses
    this grid positioning (odd-q)

    [0,0]  [1,0]
       [1,0]
    [0,1]  [1,1]
       [1,1]
    [0,2]  [1,2]
    """

    POINTY_ON_TOP = "pointy_on_top" # NOTE - not yet supported!!!
    """
    POINTY_ON_TOP means the flat edge of the hex is on the side and the farthest top/down bits are pointy. Uses
    this grid positioning (odd-r):

    [0,0]  [1,0]
       [0,1]  [1,1]
    [0,2]  [1,2]
       [0,3]  [1,3]
    [0,4]  [1,4]
    """

    def __init__(self, render_mode, radius, padding):
        self.radius = radius
        self.drawable_radius = radius - padding
        self.render_mode = render_mode

        self.point_to_point = radius*2

        if self.render_mode == HexGrid.FLAT_ON_TOP:
            self.half_hex_height = math.sqrt(radius*radius - ((radius/2) * (radius/2)))
            self.hex_height = self.half_hex_height * 2
        elif self.render_mode == HexGrid.POINTY_ON_TOP:
            self.half_hex_width = math.sqrt(radius*radius - ((radius/2) * (radius/2)))
            self.hex_width = self.half_hex_width * 2
        else:
            print("only flat allowed!")
            sys.exit(1)


    # pass in something like 4,2 and get back x/y coordinates. render_mode will affect this so decide early!
    def get_origin_for_coords(self, x_grid_slot, y_grid_slot):
        X_OFFSET = -95
        if self.render_mode == HexGrid.FLAT_ON_TOP:
            # normal (even x-vals) columns have x positions of radius, radius + radius*3, radius + radius*6, etc.
            # normal (even x-vals) columns have y positions of radius + (hex_height*y_idx)

            # offset (odd x-vals) columns have x positions of 2.5radius, 5.5 radius, 8.5 radius, etc.
            # offset columns have y positions of radius+half_hex_height+(hex_height*y_idx)

            if x_grid_slot % 2 == 0:
                return (self.radius + (self.radius * (x_grid_slot/2) * 3) + X_OFFSET, self.radius + (self.hex_height * y_grid_slot))
            else:
                return ((2.5 * self.radius) + (self.radius * ((x_grid_slot-1)/2) * 3) + X_OFFSET, self.radius + self.half_hex_height + (self.hex_height * y_grid_slot))
        elif self.render_mode == HexGrid.POINTY_ON_TOP:
            x_pos = self.radius + (x_grid_slot * self.hex_width) + (self.half_hex_width if y_grid_slot % 2 == 1 else 0)
            x_pos += X_OFFSET
            distance_between_dots = self.radius + self.radius/2
            y_pos = (self.radius) + (y_grid_slot * distance_between_dots)
            return (x_pos, y_pos)

    def generate_bordered_hex_svg_at_slot(self, slot_info, border_color, fill_color, border_amount, radius = None):
        if radius is None:
            radius = self.drawable_radius

        back_hex = self.generate_hex_svg_at_slot(slot_info, { "fill": border_color }, radius)
        front_hex = self.generate_hex_svg_at_slot(slot_info, { "fill": fill_color }, radius - border_amount)

        return back_hex + front_hex

    def generate_colored_hex_svg_at_slot(self, slot_info, color, radius = None):
        return self.generate_hex_svg_at_slot(slot_info, { "fill": color }, radius)

    def generate_hex_svg_at_slot(self, slot_info, styling, radius = None):
        if radius is None:
            radius = self.drawable_radius

        origin_x, origin_y = self.get_origin_for_coords(slot_info[0], slot_info[1])
        return self.raw_draw(origin_x, origin_y, styling, radius)

    def raw_draw(self, origin_x, origin_y, styling, radius):
        if self.render_mode == HexGrid.FLAT_ON_TOP:
            top_y = origin_y - (math.sqrt(3) * radius) / 2
            bottom_y = origin_y + (math.sqrt(3) * radius) / 2
            points = [
                (origin_x + radius, origin_y),
                (origin_x + radius / 2, bottom_y),
                (origin_x - radius / 2, bottom_y),
                (origin_x - radius, origin_y),
                (origin_x - radius / 2, top_y),
                (origin_x + radius / 2, top_y)
            ]
        elif self.render_mode == HexGrid.POINTY_ON_TOP:
            left_x = origin_x - (math.sqrt(3) * radius) / 2
            right_x = origin_x + (math.sqrt(3) * radius) / 2
            points = [
                (origin_x, origin_y - radius),
                (right_x, origin_y - radius/2),
                (right_x, origin_y + radius/2),
                (origin_x, origin_y + radius),
                (left_x, origin_y + radius/2),
                (left_x, origin_y - radius/2),
            ]

        points_as_string = ""
        for p in points:
            if points_as_string != "":
                points_as_string += " "
            points_as_string += f"{p[0]},{p[1]}"

        style = ""
        for key in styling:
            if style != "":
                style += "; "
            style += f"{key}: {styling[key]}"

        rv = f'<polygon style="{style}" points="{points_as_string}"></polygon>\n'
        return rv
