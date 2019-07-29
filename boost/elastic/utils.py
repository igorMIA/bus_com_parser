def escape_reserved_characters(query):
    """
    :param query:
    :return: escaped query
    Note:
    < and > can’t be escaped at all.
    The only way to prevent them from attempting
    to create a range query is to remove them from the query string entirely.
    """
    reserved_characters = ['+', '-', '=', '&&', '||', '!', '(', ')', '{', '}', '[', ']', '^', '"', '~',
                           '*', '?', ':', '\\', '/']
    s = list(query)
    for i, c in enumerate(s):
        if c in ['<', '>']:
            s[i] = ''
        elif c in reserved_characters:
            if c == '\000':
                s[i] = '\\000'
            else:
                s[i] = '\\' + c
    return ''.join(s)
