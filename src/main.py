#!/usr/bin/env python

"""A utility to give stats on source code.

Examples:
$ main.py .
$ main.py -v src/
$ main.py -v main.py
"""

import argparse

import report
from ignore import gitignore

# logging.basicConfig(level=logging.DEBUG)

def main():

    parser = argparse.ArgumentParser(description=__doc__,
                                     # keep docstring formatting
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", 
                        help="file or directory")
    parser.add_argument("-v", "--verbose", 
                        help="give detailed report for each file",
                        action="store_true")

    args = parser.parse_args()

    gitignore.init(args.path)
    report.Reporter(args.verbose).report(args.path)

if __name__ == '__main__':
    main()
