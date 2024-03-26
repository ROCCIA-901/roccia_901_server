from datetime import datetime, timedelta

import pytz


# Function to get the start and end of the week
# for a given date in Korea Standard Time.
# Example usage:
# monday, sunday = get_week_start_end_kst(datetime.now(pytz.utc))
def get_week_start_end_kst(current_date_utc: datetime):
    # Get date in Korea Standard Time.
    korea_timezone = pytz.timezone("Asia/Seoul")
    current_date_kst: datetime = current_date_utc.astimezone(korea_timezone)

    # Calculate the start of the week (Monday).
    start_of_week = current_date_kst - timedelta(days=current_date_kst.weekday())
    # Calculate the end of the week (Sunday).
    end_of_week = start_of_week + timedelta(days=6)

    # Return the start and end of the week
    return start_of_week.date(), end_of_week.date()
