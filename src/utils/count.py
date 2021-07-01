import re

def count_match(file, pattern="$.*^"):
    """Counts the number of lines matching the passed regular expression"""
    # print([*re.finditer(re.compile(pattern, re.M), file.read())])
    return len([*re.finditer(re.compile(pattern, re.M), file.read())])

    # count = 0

    # for line in file.readlines():
    #     if re.search(pattern, line):
    #         count += 1

    # return count
