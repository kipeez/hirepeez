import datetime
from typing import Optional
from kipeez.common.date.mocktime import mocktime
def variable_to_yyyy_mm(variable) -> Optional[str]:
    """
    Converts strings like "CURRENT_YEAR_START", "CURRENT_YEAR_CURRENT_MONTH", etc. to 'yyyy-mm' format.
    """
    if not variable:
        return None
    current_year = mocktime.now().year
    last_year = current_year - 1

    if variable == "CURRENT_YEAR_START":
        return f"{current_year}-01"
    elif variable == "CURRENT_YEAR_CURRENT_MONTH":
        return f"{current_year}-{mocktime.now().month:02d}"
    elif variable == "LAST_YEAR_START":
        return f"{last_year}-01"
    elif variable == "LAST_YEAR_END":
        return f"{last_year}-12"
    else:
        return variable
        #raise ValueError(f"Invalid string: {variable}")

def variable_to_period_yyyy_mm(variable) -> Optional[list[str]]:
    """
    Converts strings like "CURRENT_YEAR_START", "CURRENT_YEAR_CURRENT_MONTH", etc. to a list of 'yyyy-mm' format dates [start, end].
    """
    if not variable:
        return None
    now = mocktime.now()
    now = now.replace(day=1) - datetime.timedelta(days=1)

    if variable == "LAST_3_MONTHS":
        end_date = now
        start_date = now
        for _ in range(2):
            start_date = (start_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        return [start_date.strftime("%Y-%m"), end_date.strftime("%Y-%m")]
    elif variable == "LAST_6_MONTHS":
        end_date = now
        start_date = now
        for _ in range(5):
            start_date = (start_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        return [start_date.strftime("%Y-%m"), end_date.strftime("%Y-%m")]
    elif variable == "LAST_12_MONTHS":
        end_date = now
        start_date = now
        for _ in range(11):
            start_date = (start_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        return [start_date.strftime("%Y-%m"), end_date.strftime("%Y-%m")]
    elif variable == "LAST_24_MONTHS":
        end_date = now
        start_date = now
        for _ in range(23):
            start_date = (start_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        return [start_date.strftime("%Y-%m"), end_date.strftime("%Y-%m")]
    elif variable == "LAST_36_MONTHS":
        end_date = now
        start_date = now
        for _ in range(35):
            start_date = (start_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        return [start_date.strftime("%Y-%m"), end_date.strftime("%Y-%m")]
    elif variable == "CURRENT_YEAR_TO_DATE":
        end_date = now
        start_date = now.replace(month=1)
        return [start_date.strftime("%Y-%m"), end_date.strftime("%Y-%m")]
    elif variable == "CURRENT_YEAR_FULL":
        end_date = now.replace(month=12, day=31)
        start_date = now.replace(month=1, day=1)
        return [start_date.strftime("%Y-%m"), end_date.strftime("%Y-%m")]
    elif variable == "LAST_YEAR_FULL":
        end_date = now.replace(year=now.year-1, month=12, day=31)
        start_date = now.replace(year=now.year-1, month=1, day=1)
        return [start_date.strftime("%Y-%m"), end_date.strftime("%Y-%m")]