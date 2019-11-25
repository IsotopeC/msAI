
"""msAI package initialization.

See package README for introduction.

"""


from msAI.errors import RootError
from msAI.miscUtils import EnvInfo

import os
import logging
from datetime import datetime
from enum import Enum, auto
from typing import Tuple, Union

# Package Name
name = "msAI"


class LogMode(Enum):
    """Enumeration of arguments accepted by the `set_logging` function's `mode` parameter.

    See `set_logging` for mode details.
    """

    DEV = auto()
    """Specifies logging mode for development."""

    RELEASE = auto()
    """Specifies logging mode for release."""

    LIB = auto()
    """Specifies logging mode for use as a library."""

    NONE = auto()
    """Specifies a silent logging mode."""


def set_logging(mode: LogMode) -> logging.Logger:
    """Configures msAI logging for development, release, library, or silent use.

    Args:
        mode: The logging configuration to set.

            `LogMode.DEV`:
                * Logging exceptions will be raised
                * Messages of severity INFO and higher are displayed on console
                * Messages of severity DEBUG and higher are saved to the log file
                * Log file is overwritten each run

            `LogMode.RELEASE`:
                * Logging exceptions will NOT be raised
                * Messages of severity WARNING and higher are displayed on console
                * Messages of severity INFO and higher are saved to the log file
                * All log files are saved for each run - named with date/time

            `LogMode.LIB`:
                * Logging exceptions will NOT be raised
                * Log handlers are left unconfigured
                  Python default will write messages or severity WARNING or higher to console

            `LogMode.NONE`:
                * Logging exceptions will NOT be raised
                * Root logger will use NullHandler to prevent messages from being displayed

    Returns:
        The msAI root logger.

    Raises:
        RootError: For an invalid logging mode.
    """

    # Module names are used as logger names- thus submodules are automatically child loggers
    root_logger = logging.getLogger(__name__)

    # Create / ensure log directory exists
    os.makedirs("./logs", exist_ok=True)

    if mode == LogMode.DEV:
        logging.raiseExceptions = True
        root_logger.setLevel(logging.DEBUG)

        # Console handler to display INFO and higher messages
        log_console = logging.StreamHandler()
        log_console.setLevel(logging.INFO)

        # File handler to write over log file on each run
        log_file = logging.FileHandler('./logs/msAI_log-dev', mode='w')
        log_file.setLevel(logging.DEBUG)

    elif mode == LogMode.RELEASE:
        logging.raiseExceptions = False
        root_logger.setLevel(logging.INFO)

        # Console handler to display WARNING and higher messages
        log_console = logging.StreamHandler()
        log_console.setLevel(logging.WARNING)

        # File handler to create a new file each run with a datetime name
        log_file = logging.FileHandler("./logs/msAI_log-" + datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
        log_file.setLevel(logging.INFO)

    elif mode == LogMode.LIB:
        logging.raiseExceptions = False

    elif mode == LogMode.NONE:
        logging.raiseExceptions = False
        root_logger.addHandler(logging.NullHandler())

    else:
        raise RootError(f"Invalid logging mode: {mode}")

    # Configure components shared by dev and release modes
    if mode == LogMode.DEV or mode == LogMode.RELEASE:
        # Log formatter
        log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_file.setFormatter(log_formatter)
        log_console.setFormatter(log_formatter)

        # Add the handlers to logger
        root_logger.addHandler(log_file)
        root_logger.addHandler(log_console)

    # Log logging mode
    root_logger.info(f"Root logging as {mode}")

    return root_logger


def set_mp_support(mode: str = 'auto', workers: Union[str, int] = 'auto') -> Tuple[bool, int]:
    """Configures msAI multiprocessing.

    The package variable MP_SUPPORT is a boolean set to enable / disable multiprocessing in the msAI package.
    This is necessary as certain operations will fail if the multiprocessing module uses the 'spawn' start method.
    The start method default is determined by OS type.

    Args:
        mode: A string specifying the multiprocessing configuration.

            `auto`: Configures multiprocessing support automatically based on OS.
            Multiprocessing will be enabled if the multiprocessing start method in use is 'fork'.

            `enable`: Manually enables multiprocessing.
            Errors may occur if multiprocessing is not fully supported by OS.

            `disable`: Manually disables multiprocessing.

        workers: The number of worker processes to use for multiprocessing.

            `auto`: Sets number of workers to CPU count.
    """

    if EnvInfo.mp_method() == 'fork':
        os_mp_support = True
    else:
        os_mp_support = False

    if workers == 'auto':
        worker_count = os.cpu_count()
    else:
        worker_count = workers

    if mode == 'enable':
        logger.info(f"Multiprocessing manually enabled, using {worker_count} workers")
        if not os_mp_support:
            logger.warning("Multiprocessing not fully supported by OS")
        return True, worker_count

    elif mode == 'disable':
        logger.info("Multiprocessing manually disabled")
        return False, worker_count

    elif mode == 'auto':
        if os_mp_support:
            logger.info(f"Multiprocessing enabled, using {worker_count} workers")
            return True, worker_count
        else:
            logger.info("Multiprocessing disabled- not supported by operating system")
            return False, worker_count
    else:
        raise RootError(f"Invalid multiprocessing mode: {mode}")


# Set logging mode
logger = set_logging(LogMode.DEV)
# logger = set_logging(LogMode.RELEASE)
# logger = set_logging(LogMode.LIB)
# logger = set_logging(LogMode.NONE)

logger.info("msAI Starting")

# Set multiprocessing support
MP_SUPPORT, WORKER_COUNT = set_mp_support(mode='auto', workers='auto')
# MP_SUPPORT, WORKER_COUNT = set_mp_support(mode='disable')

# Log environment info
logger.debug(f"Run Environment:\n{EnvInfo.all()}")
