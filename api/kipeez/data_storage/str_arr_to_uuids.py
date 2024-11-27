from typing import List


def str_arr_to_uuids(ids: List[str]) -> str:
    """ transform a list of uuids as string to a single string representing an array of uuids
    use it directly in postgres query
    example
        uuids = str_arr_to_uuids(ids)
        insert_query = f"SELECT id, name FROM organisations WHERE id = ANY({uuids})"
    """
    return "ARRAY["+','.join([f"UUID('{id}')" for id in ids])+"]"