def flip_case(phrase, to_swap):
    """Flip [to_swap] case each time it appears in phrase.

        >>> flip_case('Aaaahhh', 'a')
        'aAAAhhh'

        >>> flip_case('Aaaahhh', 'A')
        'aAAAhhh'

        >>> flip_case('Aaaahhh', 'h')
        'AaaaHHH'

    """
    output = ""
    for letter in phrase:
        if letter.lower() == to_swap.lower():
            if letter.islower():
                output += letter.upper()
            else:
                output += letter.lower()
        else:
            output += letter
    return output
