# regexp for the python language


TYPE_OF_LINE = {
    # "LINES": r"^[\s\S]*$",
    "LOC": r"^.*$",
    "SLOC": r"^.*\w.*$",
    "COMMENTS": r'#.*|\'\'\'|"""',
    "BLANK": r"^\s*$",
    
    # "WORDS": r"\b\w+\b",
    # "SPACES": r"\s",
    # "CHARS": r"\w",

    # https://stackoverflow.com/questions/44532041/strip-multiline-python-docstrings-with-regex
    "DOCSTRING_LINES": r'^.*$'                  # any line
                +r'(?='                         # followed by
                +r'([\s\S](?!"""))*[\s\S]"""'   # - a closing docstring
                +r'('                           # - and any number of
                +r'([\s\S](?!"""))*'                        # anything
                +r'([\s\S]"""([\s\S](?!"""))*[\s\S]""")'    # that includes closed docstrings
                +r')*'
                +r'([\s\S](?!"""))*'            # - and anything with no more docstrings
                +r'\Z)'                         # until the end of the text
}
