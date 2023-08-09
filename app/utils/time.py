def get_day_of_week(timestamp):
    """
    Get the day of the week (0-6) from a given timestamp.

    Args:
        timestamp: A datetime object representing the timestamp.

    Returns:
        An integer representing the day of the week (0: Monday, 1: Tuesday, ..., 6: Sunday).
    """
    return timestamp.weekday()
