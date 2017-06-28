#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Trevor Day"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from game import Game
from logger import setup_logger
import asyncio


logger = setup_logger(logfile="log.txt")


def main(args):
    """ Main entry point of the app """
    logger.info("hello world")
    logger.info(args)
    loop = asyncio.get_event_loop()
    g = Game("data/db.json", logger)
    loop.run_until_complete(g.test_loop())


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Optional argument flag which defaults to False
    parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-n", "--name", action="store", dest="name")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
