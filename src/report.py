from stats import Analytics
from reporter import console
# import memoize

class Reporter:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def report(self, path):
        # print(f'{path} => {Analytics.create(path).get_stats()}')
        # if self.verbose:
        #     console.display(memoize.get_items())
        # console.display_file(path, "SLOC")
        console.display_header()
        console.display_all(path)
        