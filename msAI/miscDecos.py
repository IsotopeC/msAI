
"""Miscellaneous decorator functions used by msAI.

"""


# from msAI.errors import MiscDecosError

import functools
import logging
import time

import pandas


logger = logging.getLogger(__name__)
"""Module logger."""


def log_timer_df(func):
    """Decorator to log the method runtime and shape of the instance object's dataframe attribute (`df`).

    The wrapped methods's own module logger will be used to create the log.
    Use the `log_timer` decorator for logging time of function / methods without dataframes.
    """

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time

        logger = logging.getLogger(func.__module__)

        inst_obj = args[0]

        if hasattr(inst_obj, 'df') and isinstance(inst_obj.df, pandas.DataFrame):
            df_shape = inst_obj.df.shape
            logger.info(f"Finished {inst_obj.__class__.__name__}:{func.__name__} [df shape={df_shape}] in {run_time:.3f} seconds")
        else:
            logger.info(f"Finished {inst_obj.__class__.__name__}:{func.__name__} [no df attribute] in {run_time:.2f} seconds")

        return value

    return wrapper_timer

