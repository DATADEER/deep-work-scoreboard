from PIL import Image, ImageDraw
from helper import get_rect_center,get_centered_rect_bounds, get_rect_size_by_content

def get_image(month):
    WEEKS_PER_MONTH = len(month)  # 4
    DAYS_PER_WEEK = len(month[0])  # 7

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 480

    CIRCLE_SIZE = 45
    CIRCLE_OUTLINE_WIDTH = 3
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

    FILL_DEEP_WORK_DAY = (0, 0, 0)
    OUTLINE_DEEP_WORK_DAY = None

    FILL_NON_DEEP_WORK_DAY = (255, 255, 255)
    OUTLINE_NON_DEEP_WORK_DAY = (0, 0, 0)

    # Create new PIL image with a white background
    image = Image.new("P", (SCREEN_WIDTH, SCREEN_HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(image)


    # Boundary Visualisation of Child Rect for Debug
    center = get_rect_center((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
    child_rect_width, child_rect_height = get_rect_size_by_content(circle_size=CIRCLE_SIZE, week_margin=WEEK_MARGIN, day_margin=DAY_MARGIN, days_count=DAYS_PER_WEEK, weeks_count=WEEKS_PER_MONTH)
    child_rect_upper_left_coords,child_rect_lower_right_coords = get_centered_rect_bounds(center, child_rect_width,child_rect_height)
    draw.rectangle((child_rect_upper_left_coords, child_rect_lower_right_coords), fill=(230, 230, 100))


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

            fill = FILL_DEEP_WORK_DAY if day == 1 else FILL_NON_DEEP_WORK_DAY
            outline = OUTLINE_DEEP_WORK_DAY if day == 1 else OUTLINE_NON_DEEP_WORK_DAY

            draw.ellipse((day_x_upper_left, day_y_upper_left, day_x_lower_right, day_y_lower_right),
                         fill=fill, outline=outline, width=CIRCLE_OUTLINE_WIDTH)  # Circle (ellipse

    # Debug Center
    # draw.ellipse((center, (center[0] + 10, center[1] + 10)), fill=(255, 0, 0))  # Circle (ellipse)

    return image
