from PIL import Image, ImageDraw
import argparse


def get_image(month):
    WEEKS = len(month)  # 4
    DAYS_PER_WEEK = len(month[0])  # 7

    BOUNDARY_X_UPPER_LEFT = 200
    BOUNDARY_Y_UPPER_LEFT = 100
    BOUNDARY_X_LOWER_RIGHT = 600
    BOUNDARY_Y_LOWER_RIGHT = 380

    # Trying to calculate the ultimate circle and margin size for our boundary
    # BOUNDARY_WIDTH = BOUNDARY_X_LOWER_RIGHT - BOUNDARY_X_UPPER_LEFT
    # BOUNDARY_HEIGHT = BOUNDARY_Y_LOWER_RIGHT - BOUNDARY_Y_UPPER_LEFT
    # FILL_SIZE = BOUNDARY_WIDTH

    CIRCLE_SIZE = 45
    CIRCLE_OUTLINE_WIDTH = 3
    WEEK_MARGIN = CIRCLE_SIZE / 3
    DAY_MARGIN = CIRCLE_SIZE / 3

    FILL_DEEP_WORK_DAY = (0, 0, 0)
    OUTLINE_DEEP_WORK_DAY = None

    FILL_NON_DEEP_WORK_DAY = (255, 255, 255)
    OUTLINE_NON_DEEP_WORK_DAY = (0, 0, 0)

    # Create new PIL image with a white background
    image = Image.new("P", (800, 480), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Boundary Visualisation for Debug
    # draw.rectangle((BOUNDARY_X_UPPER_LEFT, BOUNDARY_Y_UPPER_LEFT, BOUNDARY_X_LOWER_RIGHT, BOUNDARY_Y_LOWER_RIGHT), fill=(230, 230, 230))

    # draw.ellipse((150, 150, 300, 300), fill=(0,0,0))  # Circle (ellipse)
    # draw.ellipse((300, 300, 600, 600), outline=(0,0,0), width=10)  # Circle (ellipse)

    for week_index, week in enumerate(month):
        week_x_upper_left = BOUNDARY_X_UPPER_LEFT
        week_y_upper_left = BOUNDARY_Y_UPPER_LEFT + (week_index * CIRCLE_SIZE) + (week_index * WEEK_MARGIN)
        # week_x_lower_right = BOUNDARY_X_UPPER_LEFT + CIRCLE_SIZE
        week_y_lower_right = BOUNDARY_Y_UPPER_LEFT + CIRCLE_SIZE + (week_index * CIRCLE_SIZE) + (
                week_index * WEEK_MARGIN)

        for day_index, day in enumerate(week):
            day_x_upper_left = week_x_upper_left + (day_index * DAY_MARGIN) + (day_index * CIRCLE_SIZE)
            day_y_upper_left = week_y_upper_left
            day_x_lower_right = day_x_upper_left + CIRCLE_SIZE
            day_y_lower_right = week_y_lower_right

            fill = FILL_DEEP_WORK_DAY if day == 1 else FILL_NON_DEEP_WORK_DAY
            outline = OUTLINE_DEEP_WORK_DAY if day == 1 else OUTLINE_NON_DEEP_WORK_DAY

            draw.ellipse((day_x_upper_left, day_y_upper_left, day_x_lower_right, day_y_lower_right),
                         fill=fill, outline=outline, width=CIRCLE_OUTLINE_WIDTH)  # Circle (ellipse

    return image

MONTH = [
    [0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

parser = argparse.ArgumentParser(description='Image processor')
parser.add_argument('--display', action='store_true', help='Render to Inky Impression screen')
args = parser.parse_args()

image = get_image(MONTH)

if(args.display):
    print("printing to inky impression")
    from inky.auto import auto

    inky_display = auto(ask_user=True, verbose=True)
    inky_display.set_image(image)
    inky_display.show()
else:
    image.show()

