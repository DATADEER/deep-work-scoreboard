from collections import namedtuple

def get_rect_center(upper_left_coords, lower_right_coords):
    (x_upper_left, y_upper_left) = upper_left_coords
    (x_lower_right, y_lower_right) = lower_right_coords
    x = (x_upper_left + x_lower_right) / 2
    y = (y_upper_left + y_lower_right) / 2
    return x, y

def get_centered_rect_bounds(center_coord, width, height):
    (x_center, y_center) = center_coord
    upper_left_coords = ((x_center - (width / 2)), y_center - (height / 2))
    lower_right_coords = ((x_center + (width / 2)), y_center + (height / 2))
    RectBoundCoords = namedtuple('RectBoundCoords', ['upper_left_coords', 'lower_right_coords'])
    return RectBoundCoords(upper_left_coords=upper_left_coords,lower_right_coords=lower_right_coords)