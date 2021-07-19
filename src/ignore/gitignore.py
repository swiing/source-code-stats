import os

from gitignore_parser import parse_gitignore

matches = None

def init(path):
    global matches
    if os.path.isfile(path + '/.gitignore'):
        matches = parse_gitignore(path + '/.gitignore')
    else:
        matches = lambda path : False

# decorator
def ignore(func):
    """ ignores path if it matches .gitignore """
    return lambda path : None if matches(path) else func(path)