import argparse
import os
from datetime import date, datetime, timedelta

from week_slices import get_current_weeks_slice
from image import get_image
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()  # take environment variables

print(f"Updating Scoreboard...")

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
    print(f"fetching latest time logs from {week_start_date} to {week_end_date}")

    response = (
        supabase.table("time_logs")
        .select("observation, start_datetime, created_by")
        .eq("created_by", MFD_USER_ID)
        .gte("start_datetime", week_start_date)
        # when calling
        # .lte("start_datetime", week_end_date)
        # supabase doens't fetch all necessary logs.
        # likely becuase week_end_date implicitly has time set to 00:00:00
        # TODO: find out how exactly query looks like when calling
        # for now we set it to one day later to get all logs
        .lt("start_datetime", week_end_date + timedelta(days=1))
        .execute()
    )

    return response.data


def map_week(week_index,week, time_logs):
    return [map_day(day_index, day, week_index, week, time_logs) for day_index, day in enumerate(week)]

def map_day(day_index, day, week_index, week, time_logs):
    week_slice_day_index = (week_index * len(week)) + day_index
    day_in_week_slice = weeks_slice[week_slice_day_index]
    return 1 if has_focus_time_log(time_logs, day_in_week_slice) else 0

def has_focus_time_log(time_logs, day: date):
    deep_work_logs = [log for log in time_logs if is_focus_time_log_on_day(log, day)]

    if len(deep_work_logs) >= 1:
        return True

    return False

def is_focus_time_log_on_day(time_log, day:date):
    if not time_log["observation"] : return False
    has_deep_work_label = "deep work" in time_log["observation"].lower()
    has_deliberate_practice_label = "deliberate practice" in time_log["observation"].lower()
    has_long_thinking_label = "long thinking" in time_log["observation"].lower()
    log_start_datetime: datetime = datetime.fromisoformat(time_log["start_datetime"])
    log_start_date: date = log_start_datetime.date()
    is_on_day = log_start_date == day

    return (has_deep_work_label | has_deliberate_practice_label | has_long_thinking_label) & is_on_day

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

# for debugging other dates
today = date.today()
print("today", today)

weeks_slice = get_current_weeks_slice(today)

fetched_time_logs = get_time_logs(week_start_date=weeks_slice[0], week_end_date=weeks_slice[-1])

FILLED_MONTH = [map_week(week_index, week, time_logs=fetched_time_logs) for (week_index, week) in enumerate(EMPTY_MONTH)]

# Determine how to render the image
parser = argparse.ArgumentParser(description='Image processor')
parser.add_argument('--display', action='store_true', help='Render to Inky Impression screen')
args = parser.parse_args()

image = get_image(FILLED_MONTH, weeks_slice, today)

if(args.display):
    print(f"printing {FILLED_MONTH} to inky impression")
    from inky.auto import auto

    inky_display = auto(ask_user=True, verbose=True)
    inky_display.set_image(image)
    inky_display.show()
else:
    image.show()

