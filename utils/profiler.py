import time
from functools import wraps
from utils.logger import LogSystem
logger = LogSystem()


def time_profile(fn):
    """
    Time profiler for functions and methods. Use it as decorator as "@time_profile"
    :param fn: A class method or function
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        # fn_kwargs_str = ', '.join(f'{k}={v}' for k, v in kwargs.items())
        # logger.log_info(f'Executing: {fn.__name__}')

        # Measure time
        t = time.perf_counter()
        retval = fn(*args, **kwargs)
        elapsed = time.perf_counter() - t
        logger.log_info(f'Execution Time: {elapsed:0.4}')

        return retval

    return inner

