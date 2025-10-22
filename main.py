import argparse

from image import get_image

MONTH = [
    [0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

parser = argparse.ArgumentParser(description='Image processor')
parser.add_argument('--display', action='store_true', help='Render to Inky Impression screen')
args = parser.parse_args()

image = get_image(MONTH)

if(args.display):
    print("printing to inky impbression")
    from inky.auto import auto

    inky_display = auto(ask_user=True, verbose=True)
    inky_display.set_image(image)
    inky_display.show()
else:
    image.show()

