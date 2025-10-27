import argparse
import os
from datetime import date, datetime

from week_slices import get_current_weeks_slice
from image import get_image
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()  # take environment variables

MONTH = [
    [0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")
MFD_USER_ID = os.getenv("MFD_USER_ID")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

def get_time_logs(week_start_date, week_end_date):
    response = (
        supabase.table("time_logs")
        .select("observation, start_datetime, created_by")
        .eq("created_by", MFD_USER_ID)
        .gte("start_datetime", week_start_date)
        .lte("start_datetime", week_end_date)
        .execute()
    )

    return response.data


def map_week(week_index,week, time_logs):
    return [map_day(day_index, day, week_index, week, time_logs) for day_index, day in enumerate(week)]

def map_day(day_index, day, week_index, week, time_logs):
    print("day", day)
    # return 1
    #find the index of week_slice_day
    week_slice_day_index = (week_index * len(week)) + day_index
    print("week_slice_day_index", week_slice_day_index)
    day_in_week_slice = weeks_slice[week_slice_day_index]
    print(day_in_week_slice, type(day_in_week_slice))
    return 1 if has_deep_work_log(time_logs, day_in_week_slice) else 0

def has_deep_work_log(time_logs, day: date):
    # print("lols", day)
    deep_work_logs = [log for log in time_logs if is_deep_work_log_on_day(log, day)]

    if len(deep_work_logs) >= 1:
        return True

    return False

def is_deep_work_log_on_day(time_log, day:date):
    print("time_log", time_log)
    if not time_log["observation"] : return False
    has_deep_work_label = "deep work" in time_log["observation"].lower()
    log_start_datetime: datetime = datetime.fromisoformat(time_log["start_datetime"])
    log_start_date: date = log_start_datetime.date()
    is_on_day = log_start_date == day

    print("log_start_date",log_start_date,day)
    print("has_deep_work_label",has_deep_work_label, "is_on_day",is_on_day)

    return has_deep_work_label & is_on_day

# for testing without using network request
MOCKED_MONTH = [
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

# TODO: Make sure weeks slices always start on a monday
weeks_slice = get_current_weeks_slice()

fetched_time_logs = get_time_logs(week_start_date=weeks_slice[0], week_end_date=weeks_slice[-1])

FILLED_MONTH = [map_week(week_index, week, time_logs=fetched_time_logs) for (week_index, week) in enumerate(EMPTY_MONTH)]
print("FILLED_MONTH",FILLED_MONTH)

# Determine how to render the image
parser = argparse.ArgumentParser(description='Image processor')
parser.add_argument('--display', action='store_true', help='Render to Inky Impression screen')
args = parser.parse_args()

image = get_image(FILLED_MONTH)

if(args.display):
    print("printing to inky impression")
    from inky.auto import auto

    inky_display = auto(ask_user=True, verbose=True)
    inky_display.set_image(image)
    inky_display.show()
else:
    image.show()

