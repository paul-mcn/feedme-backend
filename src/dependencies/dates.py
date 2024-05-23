from datetime import date, timedelta
from typing import Optional


def get_start_of_week(d: Optional[date]):
    if d is None:
        d = date.today()
    return d - timedelta(days=d.weekday())
