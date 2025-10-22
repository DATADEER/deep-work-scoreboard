from collections import namedtuple

def get_rect_size_by_content(circle_size, week_margin, day_margin, weeks_count, days_count):
    NO_MARGIN_ON_LAST_DAY = 1
    NO_MARGIN_ON_LAST_WEEK = 1
    width = circle_size * days_count + day_margin * (days_count - NO_MARGIN_ON_LAST_DAY)
    height = circle_size * weeks_count + week_margin * (weeks_count - NO_MARGIN_ON_LAST_WEEK)
    return width, height

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