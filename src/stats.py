import logging
import os
import re

from utils.count import count_match
from lang.python import TYPE_OF_LINE
import memoize


# https://stackoverflow.com/questions/30362391/how-do-you-find-the-first-key-in-a-dictionary
DEFAULT = next(iter(TYPE_OF_LINE)) # == "LOC"

_store = {}

class Analytics:

    __Logger = logging.getLogger(__name__)

    @classmethod
    def create(cls, pathname):
        """Create an instance of an Analytics if none exists for the given path.

        Otherwise returns the existing one.
        """
        if pathname not in _store:
            if type(pathname) != str:
                raise TypeError(f"pathname must be a string, not {type(pathname)}")
            if not(os.path.isfile(pathname) or os.path.isdir(pathname)):
                cls.__Logger.info("not a valid pathname: %s", str(pathname))
                raise Exception
            elif os.path.isdir(pathname) and  re.search("/_", pathname):
                # ignore directories starting with underscore
                # (e.g. I don't want to include __pycache__ stuff)
                cls.__Logger.info("ignoring %s", pathname)
            _store[pathname] = cls(pathname)
        return _store[pathname]

    def __init__(self, pathname):
        """Object to provide stats for the given path.

        Path can be a directory path or a file path.
        If a directory path, it will return the number of loc in the directory
        (counting recursively in sub-directories, if any).

        filenames or directories starting with an underscore are ignored.
        """
        self.pathname = None

        if type(pathname) != str:
            raise TypeError(f"pathname must be a string, not {type(pathname)}")

        if not(os.path.isfile(pathname) or os.path.isdir(pathname)):
            self.__Logger.info("not a valid pathname: %s", str(pathname))

        # ignore directories starting with underscore
        # (e.g. I don't want to include __pycache__ stuff)
        elif os.path.isdir(pathname) and  re.search("/_", pathname):
            self.__Logger.info("ignoring %s", pathname)

        else:
            self.pathname = pathname

    @memoize.store
    def get_stat(self, what=DEFAULT):
        """Gets a stat for a given item (e.g. SLOC)."""

        count = 0

        if not self.pathname:
            pass

        elif os.path.isfile(self.pathname):
            try:
                count = count_match(open(self.pathname), TYPE_OF_LINE[what])
            except Exception as exc:
                self.__Logger.error("An error has occured", exc)

        else: # os.path.isdir(self.pathname):
            for p in os.listdir(self.pathname):
                count += Analytics.create(self.pathname + "/" + p).get_stat(what)

        return count

    # def get_stats(self):
    #     """Gets a list of all stats."""

    #     count=[]

    #     if not self.pathname:
    #         pass

    #     elif os.path.isfile(self.pathname):
    #         for k in TYPE_OF_LINE.keys():
    #             # it may look like the loop is unecessary as only the last count 
    #             # value is used, but the decorator of _get_loc will perform its
    #             # magic of storing computed values for future use.
    #             #
    #             # @todo: I may want to allow more targeted computation,
    #             # i.e. compute only for some targeted key(s).
    #             count.append(self.get_stat(what=k))

    #     else: # os.path.isdir(self.pathname):
    #         count = [0] * len(TYPE_OF_LINE.keys())
    #         for p in os.listdir(self.pathname):
    #             stats = Analytics.create(self.pathname + "/" + p).get_stats()
    #             if len(stats):
    #                 # sum the two lists element by element
    #                 count = [sum(x) for x in zip(count, stats)]
        
    #     return count
