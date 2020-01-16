
"""
Demo of Fixed-Type Arrays and Vectorized Operations

"""


import inspect
import sys
import os
import functools
import logging
import time
import msAI.msData as msData
from msAI.samples import SampleSet
from msAI.metadata import SampleMetadata
from msAI.miscUtils import Sizer
import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)
logging.raiseExceptions = True
logger.setLevel(logging.DEBUG)
log_console = logging.StreamHandler()
log_console.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_console.setFormatter(log_formatter)
logger.addHandler(log_console)
logger.info(f"Logging starting...")
logger.info(f"Main Thread PID: {os.getpid()}")


def log_timer(callable_obj):
    """Decorator to log the runtime of a callable function or asynchronous coroutine."""

    if callable(callable_obj):

        # if inspect.isawaitable(callable_obj):
        if inspect.iscoroutinefunction(callable_obj):

            @functools.wraps(callable_obj)
            async def wrapper_timer_async(*args, **kwargs):
                start_time = time.perf_counter()
                result = await callable_obj(*args, **kwargs)
                end_time = time.perf_counter()
                run_time = end_time - start_time

                logger.info(f"Finished {callable_obj.__name__} in {run_time:.3f} seconds")

                return result

            return wrapper_timer_async

        else:
            @functools.wraps(callable_obj)
            def wrapper_timer(*args, **kwargs):
                start_time = time.perf_counter()
                result = callable_obj(*args, **kwargs)
                end_time = time.perf_counter()
                run_time = end_time - start_time

                logger.info(f"Finished {callable_obj.__name__} in {run_time:.3f} seconds")

                return result

            return wrapper_timer

    else:
        raise ValueError(f"Argument {callable_obj.__name__} received for callable_obj parameter is not callable")


# Set pandas to display all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Path to example data
sample1_mzml_path = "./examples/data/mzML/EP2421.mzML"


# Import MS data from mzML file
sample1_ms = msData.MZMLfile(sample1_mzml_path)

sample1_ms.peaks

peaks_array = sample1_ms.peaks.to_numpy()
len(peaks_array)
array_size = Sizer.obj_mb(peaks_array)
array_size

peaks_list = sample1_ms.peaks.values.tolist()
len(peaks_list)
list_size = Sizer.obj_mb(peaks_list)
list_size

list_size / array_size

