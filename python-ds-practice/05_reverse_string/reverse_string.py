def reverse_string(phrase):
    """Reverse string,

        >>> reverse_string('awesome')
        'emosewa'

        >>> reverse_string('sauce')
        'ecuas'
    """
    output = ""
    for x in range(len(phrase)):
        output += phrase[-(x+1)]
    return output