from typing import List


def array_agg_to_strings(strings: str) -> List[str]:
    """ when using array_agg in postres, transforms a string returned by psycopg2 to a List"
    """
    if strings == "{NULL}":
        return []
    return strings[1:-1].split(',')

def array_agg_is_empty(array) -> bool:
    """ when using array_agg in postres, transforms a string returned by psycopg2 to a List"
    """
    return array == "{NULL}" or array == [None] or all(e is None for e in array)