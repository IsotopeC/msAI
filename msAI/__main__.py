
"""msAI package main.

Future launch point for command line use.

Usage:
    python -m msAI

See package README for introduction.

"""


import msAI

import logging


logger = logging.getLogger('msAI')
"""Module logger."""


def main():
    logger.error("Command line use is not implemented yet, "
                 "import msAI package and use as a library")


if __name__ == "__main__":
    logger.info("Starting msAI")

    try:
        main()

    except Exception as e:
        logger.critical(f"Unhandled exception: {e.__class__.__name__}", exc_info=True)
        raise SystemExit(1)

    except KeyboardInterrupt:
        logger.critical("Keyboard interrupt pressed")
        raise SystemExit(3)

    except SystemExit as e:
        logger.critical("Aborting msAI")
        raise e

    else:
        logger.info("msAI Finished")
        raise SystemExit(0)

    finally:
        logger.info("msAI Closed")

