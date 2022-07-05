def titleize(phrase):
    """Return phrase in title case (each word capitalized).

        >>> titleize('this is awesome')
        'This Is Awesome'

        >>> titleize('oNLy cAPITALIZe fIRSt')
        'Only Capitalize First'
    """
    words = [word.lower().capitalize() for word in phrase.split(" ")]
    output = ""
    for word in words:
        if words.index(word) == len(words) - 1:
            output += word
        else:
            output += f"{word} "
    return output
