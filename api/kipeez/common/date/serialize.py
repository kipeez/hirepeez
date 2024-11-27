#serialise a date for fastapi

from datetime import datetime, timezone
from typing import List


def serialize_date(date: datetime|str):
    return str(date)+"Z" if date else None 

def serialize_dates(dates: List[datetime|str]):
    return [str(date)+"Z" if date else None for date in dates]