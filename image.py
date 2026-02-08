import os
import random
from math import floor
from tkinter.constants import ROUND

from PIL import Image, ImageDraw
from helper import get_rect_center,get_centered_rect_bounds, get_rect_size_by_content
from datetime import date

# https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
PILLOW_IMAGE_MODE = "RGB"

# Screen Size

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

def get_board_image(month, weeks_slice, today=date.today()):
    WEEKS_PER_MONTH = len(month)  # 4
    DAYS_PER_WEEK = len(month[0])  # 7

    CIRCLE_SIZE = 45
    CIRCLE_OUTLINE_WIDTH = 5
    CIRCLE_OUTLINE_WIDTH_TODAY = 10
    WEEK_MARGIN = CIRCLE_SIZE / 3
    DAY_MARGIN = CIRCLE_SIZE / 3

    BOUNDARY_X_UPPER_LEFT = 200
    BOUNDARY_Y_UPPER_LEFT = 100
    BOUNDARY_X_LOWER_RIGHT = 600
    BOUNDARY_Y_LOWER_RIGHT = BOUNDARY_Y_UPPER_LEFT + (CIRCLE_SIZE + WEEK_MARGIN) * WEEKS_PER_MONTH - WEEK_MARGIN

    # Trying to calculate the ultimate circle and margin size for our boundary
    # BOUNDARY_WIDTH = BOUNDARY_X_LOWER_RIGHT - BOUNDARY_X_UPPER_LEFT
    # BOUNDARY_HEIGHT = BOUNDARY_Y_LOWER_RIGHT - BOUNDARY_Y_UPPER_LEFT
    # FILL_SIZE = BOUNDARY_WIDTH


    # Create new PIL image with a white background
    image = Image.new(PILLOW_IMAGE_MODE, (SCREEN_WIDTH, SCREEN_HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(image)


    # Boundary Visualisation of Child Rect for Debug
    center = get_rect_center((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
    child_rect_width, child_rect_height = get_rect_size_by_content(circle_size=CIRCLE_SIZE, week_margin=WEEK_MARGIN, day_margin=DAY_MARGIN, days_count=DAYS_PER_WEEK, weeks_count=WEEKS_PER_MONTH)
    child_rect_upper_left_coords,child_rect_lower_right_coords = get_centered_rect_bounds(center, child_rect_width,child_rect_height)
    # draw.rectangle((child_rect_upper_left_coords, child_rect_lower_right_coords), fill=(230, 230, 100))


    for week_index, week in enumerate(month):
        week_x_upper_left = child_rect_upper_left_coords[0]
        week_y_upper_left = child_rect_upper_left_coords[1] + (week_index * CIRCLE_SIZE) + (week_index * WEEK_MARGIN)
        week_x_lower_right = week_x_upper_left + child_rect_width
        week_y_lower_right = week_y_upper_left + CIRCLE_SIZE + WEEK_MARGIN

        #draw.rectangle(((week_x_upper_left,week_y_upper_left),(week_x_lower_right,week_y_lower_right)), fill=(30,230, 100 + (week_index * 50)))
        #draw.line(((week_x_upper_left, week_y_upper_left), (week_x_lower_right, week_y_lower_right)), fill=(0, 0, 0))

        for day_index, day in enumerate(week):
            day_x_upper_left = week_x_upper_left + (day_index * DAY_MARGIN) + (day_index * CIRCLE_SIZE)
            day_y_upper_left = week_y_upper_left
            day_x_lower_right = day_x_upper_left + CIRCLE_SIZE
            day_y_lower_right = day_y_upper_left + CIRCLE_SIZE

            date = get_date_from_weeks_slice_by_index(weeks_slice, week_index, day_index)

            fill = get_day_fill(day, date, today)
            outline = get_day_outline(day, date, today)

            draw.ellipse((day_x_upper_left, day_y_upper_left, day_x_lower_right, day_y_lower_right),
                         fill=fill, outline=outline, width=CIRCLE_OUTLINE_WIDTH_TODAY if date == today else CIRCLE_OUTLINE_WIDTH)  # Circle (ellipse

    # Debug Center
    # draw.ellipse((center, (center[0] + 10, center[1] + 10)), fill=(255, 0, 0))  # Circle (ellipse)

    return image

def add_illustrations(image):
    ILLSTURATION_PATH = "./illustrations"
    available_illustrations_filenames = os.listdir(ILLSTURATION_PATH)
    random_illustration = random.choice(available_illustrations_filenames)
    print("from", available_illustrations_filenames, "chose", random_illustration)
    illustration = Image.open(f'{ILLSTURATION_PATH}/{random_illustration}', 'r')
    illustration = illustration.resize((80,80))
    image.paste(illustration, box = (floor(SCREEN_WIDTH/13), floor(SCREEN_HEIGHT/10)))
    return image



def get_day_fill(day, date, today):

    FILL_DEEP_WORK_DAY = (0, 0, 0)
    FILL_NON_DEEP_WORK_DAY = (255, 255, 255)
    FILL_PREVIOUS_NON_DEEP_WORK_DAY = (230,230,230)

    isInPast = date < today

    if day == 1: return FILL_DEEP_WORK_DAY
    if isInPast: return FILL_PREVIOUS_NON_DEEP_WORK_DAY
    return FILL_NON_DEEP_WORK_DAY

def get_day_outline(day,date, today):
    OUTLINE_DEEP_WORK_DAY = None
    OUTLINE_NON_DEEP_WORK_DAY = (0, 0, 0)
    OUTLINE_TODAY = (213, 62 ,79)

    if date == today: return OUTLINE_TODAY
    if day == 1: return OUTLINE_DEEP_WORK_DAY
    return OUTLINE_NON_DEEP_WORK_DAY


def get_date_from_weeks_slice_by_index(weeks_slice, week_index, day_index):
    return weeks_slice[week_index * 7 + day_index]