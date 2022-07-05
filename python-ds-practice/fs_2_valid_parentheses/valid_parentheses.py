from re import L


def valid_parentheses(parens):
    """Are the parentheses validly balanced?

        >>> valid_parentheses("()")
        True

        >>> valid_parentheses("()()")
        True

        >>> valid_parentheses("(()())")
        True

        >>> valid_parentheses(")()")
        False

        >>> valid_parentheses("())")
        False

        >>> valid_parentheses("((())")
        False

        >>> valid_parentheses(")()(")
        False
    """
    is_balanced = 0
    for char in parens:
        if char == "(":
            is_balanced += 1
        else:
            is_balanced -= 1
    if is_balanced == 0:
        return True
    else:
        return False
