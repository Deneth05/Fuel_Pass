from datetime import datetime, timedelta

def get_week_start_date(dt: datetime = None) -> str:
    """
    Returns the start date of the week (Sunday) for a given date.
    Format: YYYY-MM-DD
    """
    if dt is None:
        dt = datetime.now()
    
    # weekday() returns 0 for Monday, 6 for Sunday
    # We want Sunday to be the start of the week.
    days_since_sunday = (dt.weekday() + 1) % 7
    sunday = dt - timedelta(days=days_since_sunday)
    return sunday.strftime("%Y-%m-%d")

def is_sunday() -> bool:
    """Checks if today is Sunday."""
    return datetime.now().weekday() == 6
