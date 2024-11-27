import time
import asyncio
import functools

def log_time_spent(query_func):
    """
    Decorator to log the time spent in database queries.
    """
    if asyncio.iscoroutinefunction(query_func):
        @functools.wraps(query_func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            result = await query_func(*args, **kwargs)
            end_time = time.time()
            time_spent = end_time - start_time
            print(f"Function '{query_func.__name__}' executed in {time_spent:.4f} seconds.")
            return result
        return async_wrapper
    else:
        @functools.wraps(query_func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            result = query_func(*args, **kwargs)
            end_time = time.time()
            time_spent = end_time - start_time
            print(f"Function '{query_func.__name__}' executed in {time_spent:.4f} seconds.")
            return result
        return sync_wrapper
