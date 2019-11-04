
"""msAI package main.

Future launch point for command line use.

See package README for introduction.

"""


import msAI

import logging


logger = logging.getLogger('msAI')
"""Module logger."""


def main():
    logger.info("Starting from __main__.py")
    logger.error("Command line use is not implemented yet,"
                 "import msAI package and use as a library")


if __name__ == "__main__":
    try:
        main()
    except:
        logger.exception(f"Unhandled error in main")
        raise
