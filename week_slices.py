from datetime import date, timedelta

# get the currently displayed weeks (as slice of days) of this year
def get_current_weeks_slice():
    today = date.today()
    first_day_of_year = today.replace(day=1, month=1)
    last_day_of_year = today.replace(day=31, month=12)
    slice_beginning = first_day_of_year
    slices_in_year = []

    days_per_slice = 28

    while slice_beginning <= last_day_of_year:

        date_list = [slice_beginning + timedelta(days=x) for x in range(days_per_slice)]
        slices_in_year.append(date_list)
        slice_beginning = slice_beginning + timedelta(days=days_per_slice)


    todays_slice = list(filter(lambda slice : is_date_in_slice(today, slice), slices_in_year))
    return todays_slice


def is_date_in_slice(date, slice):
    return date in slice