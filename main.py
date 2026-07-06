import argparse
import os
from datetime import date, datetime, timedelta

from week_slices import get_current_weeks_slice
from image import get_board_image, add_illustrations
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

def get_activity_logs(week_start_date, week_end_date):
    print(f"fetching latest activity logs from {week_start_date} to {week_end_date}")

    response = (
        supabase.table("activity_logs")
        .select("observation, date")
        .eq("created_by", MFD_USER_ID)
        .gte("date", week_start_date)
        .lt("date", week_end_date + timedelta(days=1))
        .execute()
    )

    return response.data


def map_week(week_index,week, time_logs, activity_logs):
    return [map_day(day_index, day, week_index, week, time_logs, activity_logs) for day_index, day in enumerate(week)]

def map_day(day_index, day, week_index, week, time_logs, activity_logs):
    week_slice_day_index = (week_index * len(week)) + day_index
    day_in_week_slice = weeks_slice[week_slice_day_index]
    return 1 if has_focus_log(time_logs, activity_logs, day_in_week_slice) else 0

def has_focus_log(time_logs, activity_logs, day):
    return has_focus_time_log(time_logs, day) or has_focus_activity_log(activity_logs, day)

def has_focus_time_log(time_logs, day: date):
    deep_work_logs = [log for log in time_logs if is_focus_time_log_on_day(log, day)]

    if len(deep_work_logs) >= 1:
        return True

    return False

def has_focus_activity_log(activity_logs, day: date):
    deep_work_logs = [log for log in activity_logs if is_activity_log_on_day(log, day)]

    if len(deep_work_logs) >= 1:
        return True

    return False

def is_focus_observation(observation):

    text = observation.strip().lower()

    has_deep_work_label = text.startswith("deep work")
    has_deliberate_practice_label = text.startswith("deliberate practice")
    has_long_thinking_label = text.startswith("long thinking")
    has_focus_session_label = text.startswith("focus session")
    has_reflection_session_label = text.startswith("reflection")

    return has_deep_work_label | has_deliberate_practice_label | has_long_thinking_label | has_focus_session_label | has_reflection_session_label

def is_focus_time_log_on_day(time_log, day:date):
    if not time_log["observation"] : return False

    log_start_datetime: datetime = datetime.fromisoformat(time_log["start_datetime"])
    log_start_date: date = log_start_datetime.date()
    is_on_day = log_start_date == day

    return is_focus_observation(time_log["observation"]) & is_on_day

def is_activity_log_on_day(activity_log, day:date):
    if not activity_log["observation"] : return False
    log_start_date: date = datetime.strptime(activity_log["date"], "%Y-%m-%d").date()
    is_on_day = log_start_date == day

    return is_focus_observation(activity_log["observation"]) & is_on_day

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

def fetch_and_render(inky_display):
    print("Starting Fetch and Rerender...")
    global weeks_slice
    today = date.today()
    print("today", today)
    weeks_slice = get_current_weeks_slice(today)

    fetched_time_logs = get_time_logs(week_start_date=weeks_slice[0], week_end_date=weeks_slice[-1])
    fetched_activity_logs = get_activity_logs(week_start_date=weeks_slice[0], week_end_date=weeks_slice[-1])

    filled_month = [
        map_week(week_index, week, time_logs=fetched_time_logs, activity_logs=fetched_activity_logs)
        for (week_index, week) in enumerate(EMPTY_MONTH)
    ]

    image = get_board_image(filled_month, weeks_slice, today)
    image = add_illustrations(image)

    if inky_display:
        print(f"printing {filled_month} to inky impression")
        inky_display.set_image(image)
        inky_display.show()
    else:
        image.show()


def already_has_focus_session_today():
    today = date.today()
    print("Fetching focus sessions of " + today.strftime("DD.MM.YYYY"))
    time_logs = get_time_logs(week_start_date=today, week_end_date=today)
    activity_logs = get_activity_logs(week_start_date=today, week_end_date=today)

    return has_focus_log(time_logs, activity_logs, today)

def log_focus_session():
    print("Logging Focus session")
    supabase.table("activity_logs").insert({
        "date": date.today().isoformat(),
        "duration_minutes": 60,
        "observation": "Focus session",
        "activity_type": "DESIRED",
        "created_by": MFD_USER_ID,
    }).execute()


def seconds_until_next_hour():
    now = datetime.now()
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    return (next_hour - now).total_seconds()


parser = argparse.ArgumentParser(description='Image processor')
parser.add_argument('--display', action='store_true', help='Render to Inky Impression screen')
args = parser.parse_args()

SW_A = 5  # BCM GPIO 5 = button A on Inky Impression

if args.display:
    from inky.auto import auto
    import gpiod
    import gpiodevice
    from gpiod.line import Bias, Direction, Edge

    inky_display = auto(ask_user=True, verbose=True)
    fetch_and_render(inky_display)

    button_settings = gpiod.LineSettings(
        direction=Direction.INPUT, bias=Bias.PULL_UP, edge_detection=Edge.FALLING
    )
    chip = gpiodevice.find_chip_by_platform()
    offset = chip.line_offset_from_id(SW_A)
    request = chip.request_lines(
        consumer="deep-work-scoreboard",
        config={offset: button_settings},
    )

    print("Listening for button A + hourly refresh…")
    while True:
        wait = timedelta(seconds=seconds_until_next_hour())
        if request.wait_edge_events(timeout=wait):
            for event in request.read_edge_events():
                print("Pressed button A")
                if already_has_focus_session_today():
                    print("Already logged today")
                    fetch_and_render(inky_display)
                else:
                    log_focus_session()
                    fetch_and_render(inky_display)

        else:
            print("Hourly refresh")
            fetch_and_render(inky_display)
else:
    fetch_and_render(None)

