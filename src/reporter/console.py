import os
import re

from stats import Analytics
from lang.python import TYPE_OF_LINE

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    # '\033[0m' would be ok for coloring, however I need to set 00
    # for consistent spacing (color codes do count as characters in format()
    # # see https://stackoverflow.com/questions/14140756/python-s-str-format-fill-characters-and-ansi-colors)
    ENDC = '\033[00m'
    BOLD = '\033[01m'
    UNDERLINE = '\033[04m'


def display(items):
    """Displays in the console a detailed report."""

    # LOC, COMMENT, ...
    # (same as keys of TYPE_OF_LINE, but better to only rely on items here)
    what = next(iter(items))[1]

    # Headers
    print(bcolors.BOLD
         +("{:<30}"+":{:>10}"*len(what)).format("path", *what)
         +bcolors.ENDC)

    # Lines
    for k,v in items:
        print((bcolors.OKGREEN if v["LOC"] == 0
              else bcolors.FAIL if v["COMMENTS"] == 0
              else bcolors.WARNING if v["COMMENTS"]/v["LOC"] < 0.2
              else bcolors.OKGREEN )
              +("{:<30}"+":{:>10}"*len(v)).format(k, *v.values())
              + bcolors.ENDC)

def display_file(path, what="LOC"):
    
    if os.path.isdir(path) and  re.search("/_", path):
        return

    if os.path.isfile(path):
        analytics = Analytics.create(path)
        print(analytics.get_stat(what), end=" ")

    elif os.path.isdir(path):
        # analytics = Analytics.create(path)
        # print(path, "=>", analytics.get_stat(what))
        for f in os.listdir(path):
            display_file(path + "/" + f, what)

    # print((bcolors.OKGREEN if v["LOC"] == 0
    #           else bcolors.FAIL if v["COMMENTS"] == 0
    #           else bcolors.WARNING if v["COMMENTS"]/v["LOC"] < 0.2
    #           else bcolors.OKGREEN )
    #           +("{:<30}"+":{:>10}"*len(v)).format(k, *v.values())
    #           + bcolors.ENDC)

def display_header():
    # LOC, COMMENT, ...
    what = TYPE_OF_LINE.keys()
    # Headers
    print(bcolors.BOLD
         +("{:<30}"+"{:>10}"*len(what)).format("path", *what)
         +bcolors.ENDC)

def display_all(path):
    if os.path.isdir(path) and  re.search("/_", path):
        return

    # LOC, COMMENT, ...
    what = TYPE_OF_LINE.keys()

    if os.path.isfile(path):
        analytics = Analytics.create(path)
        print(bcolors.ENDC
         # 20 = 5+10+5 to take into account prefix and postfix color codes returned by display_val.
         +("{:<30}"+"{:>20}"*len(what)).format(path, *[display_val(path,w) for w in what])
         +bcolors.ENDC)

    elif os.path.isdir(path):
        # analytics = Analytics.create(path)
        # print(path, "=>", analytics.get_stat(what))
        for f in os.listdir(path):
            display_all(path + "/" + f)

def display_val(path, what):
    analytics = Analytics.create(path)
    val = analytics.get_stat(what)

    if what == "COMMENTS":
        if val == 0:
            return bcolors.FAIL + str(val) + bcolors.ENDC
        elif analytics.get_stat("LOC") > 0 and val / analytics.get_stat("LOC") < 0.2:
            return bcolors.WARNING + str(val) + bcolors.ENDC

    # use color codes in all cases to ensure consistent spacing
    # because color codes DO count as characters in format().
    # See https://stackoverflow.com/questions/14140756/python-s-str-format-fill-characters-and-ansi-colors
    return bcolors.ENDC + str(val) + bcolors.ENDC
