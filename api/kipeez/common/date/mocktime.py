# in case we want to override the now (unit test)
from datetime import datetime, timezone

class mocktime:
    year = 0
    month = 0
    day = 0
    @classmethod
    def set(cls, year, month, day):
        cls.year = year
        cls.month = month
        cls.day = day
    @classmethod
    def now(cls, tz = timezone.utc):
        if cls.year != 0:
            return datetime(cls.year, cls.month, cls.day)
        return datetime.now(tz)