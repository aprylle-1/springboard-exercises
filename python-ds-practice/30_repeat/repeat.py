def repeat(phrase, num):
    """Return phrase, repeated num times.

        >>> repeat('*', 3)
        '***'

        >>> repeat('abc', 2)
        'abcabc'

        >>> repeat('abc', 0)
        ''

    Ignore illegal values of num and return None:

        >>> repeat('abc', -1) is None
        True

        >>> repeat('abc', 'nope') is None
        True
    """
    output = ""
    if isinstance(num, int) and num >= 0:
        if num == 0:
            return output
        else:
            for x in range(num):
                output += phrase
            return output
    else:
        return None
