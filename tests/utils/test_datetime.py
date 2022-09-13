from utils.datetime import first_day_of_month, range_end_of_month
from datetime import datetime


def test_first_day_of_month():
    cd = datetime(2001, 1, 10).date()
    fd = first_day_of_month(cd)
    assert fd == datetime(2001, 1, 1).date()


def test_range_end_of_month():
    date_start = datetime(2019, 12, 30).date()
    date_stop = datetime(2020, 2, 2).date()
    eoms = list(range_end_of_month(date_start, date_stop))
    assert len(eoms) == 2
    assert eoms[0] == datetime(2019, 12, 31).date()
    assert eoms[1] == datetime(2020, 1, 31).date()
