
"""Miscellaneous decorator functions used by msAI.

"""


# from msAI.errors import MiscDecosError

import functools
import logging
import time
import inspect
import pandas


logger = logging.getLogger(__name__)
"""Module logger."""


def log_timer_df(method):
    """Decorator to log the method runtime and shape of the instance object's dataframe attribute (`df`).

    The wrapped methods's own module logger will be used to create the log.
    Use the `log_timer` decorator for logging time of function / methods without dataframes.
    """

    @functools.wraps(method)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = method(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time

        wrapped_logger = logging.getLogger(method.__module__)

        inst_obj = args[0]

        if hasattr(inst_obj, 'df') and isinstance(inst_obj.df, pandas.DataFrame):
            df_shape = inst_obj.df.shape
            wrapped_logger.info(f"Finished {inst_obj.__class__.__name__}:{method.__name__} [df shape={df_shape}] in {run_time:.2f} seconds")
        else:
            wrapped_logger.info(f"Finished {inst_obj.__class__.__name__}:{method.__name__} [no df attribute] in {run_time:.2f} seconds")

        return value

    return wrapper_timer


def log_timer(callable_obj):
    """Decorator to log the runtime of a callable function, including asynchronous coroutines.

    The wrapped callable's own module logger will be used to create the log.
    Wrapped asynchronous coroutines will be awaited for.
    """

    if callable(callable_obj):

        # if inspect.isawaitable(callable_obj):
        if inspect.iscoroutinefunction(callable_obj):

            @functools.wraps(callable_obj)
            async def wrapper_timer_async(*args, **kwargs):
                start_time = time.perf_counter()
                result = await callable_obj(*args, **kwargs)
                end_time = time.perf_counter()
                run_time = end_time - start_time

                wrapped_logger = logging.getLogger(callable_obj.__module__)
                wrapped_logger.info(f"Finished {callable_obj.__name__} in {run_time:.2f} seconds")

                return result

            return wrapper_timer_async

        else:
            @functools.wraps(callable_obj)
            def wrapper_timer(*args, **kwargs):
                start_time = time.perf_counter()
                result = callable_obj(*args, **kwargs)
                end_time = time.perf_counter()
                run_time = end_time - start_time

                wrapped_logger = logging.getLogger(callable_obj.__module__)
                wrapped_logger.info(f"Finished {callable_obj.__name__} in {run_time:.2f} seconds")

                return result

            return wrapper_timer

    else:
        # raise ValueError(f"Argument {callable_obj.__name__} received for callable_obj parameter is not callable")
        raise ValueError(f"Argument received for callable_obj parameter is not callable")

