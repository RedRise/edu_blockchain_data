from datetime import datetime, timedelta
from typing import Iterator


def first_day_of_month(date: datetime.date) -> datetime.date:
    return datetime(date.year, date.month, 1).date()


def range_end_of_month(
        date_start: datetime.date,
        date_stop: datetime.date = datetime.now().date()) -> Iterator[datetime.date]:

    buffer_date = date_start
    buffer_month = buffer_date.month

    current_date = buffer_date
    while current_date < date_stop:
        if current_date.month != buffer_month:
            yield buffer_date
        buffer_date = current_date
        buffer_month = buffer_date.month
        current_date = current_date + timedelta(days=1)
