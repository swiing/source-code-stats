# decorator
def ignore(func):
    """ ignores path if it matches the given extensions """
    return lambda path : None if path.lower().endswith(
        # add whatever makes sense to the list
        ('.git', 
        '__pycache__',
        '.md', '.txt', 'license', '.png', '.jpg', '.jpeg')
        ) else func(path)