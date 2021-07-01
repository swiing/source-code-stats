"""Memoize computed stats"""

_store = {}

# decorator
def store(func):
    # @todo: https://stackoverflow.com/questions/34832573/python-decorator-to-display-passed-and-default-kwargs
    # so I can get "LOC" programmatically
    def wrapper(analytics, what="LOC"):
        path = analytics.pathname
        if path not in _store:
            _store[path] = {}
        if what not in _store[path]:
            _store[path][what] = func(analytics, what)
        return _store[path][what]
    return wrapper

def get_items():
    return _store.items()
