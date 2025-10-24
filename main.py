import argparse
import os

from week_slices import get_current_weeks_slice
from image import get_image
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()  # take environment variables

MONTH = [
    [0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")
MFD_USER_ID = os.getenv("MFD_USER_ID")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

query = f"* FROM time_logs WHERE start_datetime >= '2025-10-06' AND start_datetime < '2025-11-03' AND created_by = '{MFD_USER_ID}';"

# response = (
#     supabase.table("time_logs")
#     .select(query)
#     .execute()
# )

# print(response)

weeks_slice = get_current_weeks_slice()
print(weeks_slice)


## TODO: convert the list of days from get_current_weeks_slice to the format below. then run a loop that alters each of the days in the MONTH based on logs of that particular day in the slice with

# MONTH = [
#     [0, 0, 0, 0, 0, 1, 1],
#     [1, 1, 1, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
# ]
#
# parser = argparse.ArgumentParser(description='Image processor')
# parser.add_argument('--display', action='store_true', help='Render to Inky Impression screen')
# args = parser.parse_args()
#
# image = get_image(MONTH)
#
# if(args.display):
#     print("printing to inky impression")
#     from inky.auto import auto
#
#     inky_display = auto(ask_user=True, verbose=True)
#     inky_display.set_image(image)
#     inky_display.show()
# else:
#     image.show()

