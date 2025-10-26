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

# DEBUG which logs satisfy "is deep work"

# option1
# for each day in weeks_slice
    # take the index of that day in weeks_slice and find which place it is in Month (build a function that finds this)
    # 0 = [0,0], 7 = [0,7], 8 = [1,0]
    # check if there is a log in response that is deep work and the same day (stop after the first result)
        # if yes turn that position in MONTH to 1
        # if no turn that position in MONTH to 0

# return the adjusted MONTH

# option2
# filled_month = []
# for day,day_index in weeks_slice
    # find out if day has deep work log
    # if yes circle = 1
    # if yes circle = 0
    # if (day_index + 1 % 7 == 0):
        # append circle to current week
        # append current week to month
        # overwrite current week week with empty array

# return filled_month


# option3
# filled_month = []
# for each week, week_index in EMPTY_MONTH
    # filled_week = []
    # for each day, day_index in week
        # find the index of week_slice_day
        # week_slice_day_index = (week_index * len(week)) + day_index
        # day_in_week_slice = weeks_slice[week_slice_day_index]
        # find out if day has deep work log
        # if yes append 1 to filled_week
        # if no append 0 to filled_week
    # append filled_week to filled_month
# return filled_month

# option3 with map
def map_week(week_index,week):
    return [map_day(day_index, day, week_index) for day_index, day in enumerate(week)]
    return list(map(lambda day_tuple : map_day_wrapper(day_tuple, week_index), enumerate(week)))

def map_week_wrapper(week_tuple):
    (week_index, week ) = week_tuple
    return map_week(week_index, week)


def map_day(day_index, day, week_index):
    return 1
    #find the index of week_slice_day
    #week_slice_day_index = (week_index * len(week)) + day_index
    #day_in_week_slice = weeks_slice[week_slice_day_index]
    #find out if day has deep work log
    #if yes return 1
    # if no return 0

def map_day_wrapper(day_tuple, week_index):
    (day_index, day) = day_tuple
    return map_day(day_index, day, week_index)

# map(map_week, enumerate(EMPTY_MONTH))








# TODO: how to make this functional? so I don't manipulate the MONTH but instead build up the month over time?
# option2: build the month from scratch by looping over the days in week_slice and for every 7th day create a new array.
# problem: no guarantee that the structure will be correct unless you test it rigorously and foolproof the logic
# option3: use the MONTH filled with 0's as the base and loop over it. to find it's matching date, take the index of the current outer and inner loop
# for each outer loop, calc * 7 (e.g outerloop index 1 and inner loop index 2 == (1*7) + 2 == 9, so index 9 day 10)
# pro: very visual, flexible, if the format changes I can just change input array. no manipulation of array

## TODO: convert the list of days from get_current_weeks_slice to the format below. then run a loop that alters each of the days in the MONTH based on logs of that particular day in the slice with

MONTH = [
    [0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

EMPTY_MONTH = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

# FILLED_MONTH = list(map(map_week_wrapper, enumerate(EMPTY_MONTH)))
FILLED_MONTH = [map_week(week_index, week) for (week_index, week) in enumerate(EMPTY_MONTH)]

print("FILLED_MONTH",FILLED_MONTH)

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

