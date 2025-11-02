from calendar import MONDAY
from datetime import date, timedelta

# get the currently displayed weeks (as slice of days) of this year
def get_current_weeks_slice():
    today = date.today()
    first_day_of_year = today.replace(day=1, month=1)
    last_day_of_year = today.replace(day=31, month=12)
    slice_beginning = get_monday_around_start_of_year(first_day_of_year)
    slices_in_year = []

    days_per_slice = 28

    # TODO: make sure we always see 28 days. regardless of between the years or not
    while slice_beginning <= last_day_of_year:

        dates_in_slice = [slice_beginning + timedelta(days=x) for x in range(days_per_slice)]
        slices_in_year.append(dates_in_slice)
        slice_beginning = slice_beginning + timedelta(days=days_per_slice)

    todays_slice = list(filter(lambda slice : is_date_in_slice(today, slice), slices_in_year))
    return todays_slice[0]


# I want the scoreboard to always start on a monday. There is no guarantee that the year starts on a monday.
# If 1. of the year isn't a monday we include enough of the previous year on the board so we can start on a monday.
def get_monday_around_start_of_year(first_day_of_year):
    if first_day_of_year.weekday() == MONDAY:
        return first_day_of_year

    ## figure out if there is another way to do this
    day = first_day_of_year - timedelta(days=1)
    while day.weekday() != MONDAY:
        day = day - timedelta(days=1)

    return day

def is_date_in_slice(date, slice):
    return date in slice