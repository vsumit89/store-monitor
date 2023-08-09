from datetime import datetime

def get_day_of_week(timestamp):
    # Parse the timestamp
    # dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f%z")
    
    # # Get the day of the week (Monday is 0, Sunday is 6)
    # day_of_week = dt.weekday()
    # return day_of_week
    return timestamp.weekday()