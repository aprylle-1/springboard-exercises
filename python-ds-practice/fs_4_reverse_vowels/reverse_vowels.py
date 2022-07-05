def reverse_vowels(s):
    """Reverse vowels in a string.

    Characters which re not vowels do not change position in string, but all
    vowels (y is not a vowel), should reverse their order.

    >>> reverse_vowels("Hello!")
    'Holle!'

    >>> reverse_vowels("Tomatoes")
    'Temotaos'

    >>> reverse_vowels("Reverse Vowels In A String")
    'RivArsI Vewols en e Streng'

    reverse_vowels("aeiou")
    'uoiea'

    reverse_vowels("why try, shy fly?")
    'why try, shy fly?''
    """
    vowels = [char for char in s if char.lower() in "aeiou"]
    vowel_count = len(vowels) - 1
    output = ""
    for x in range(len(s)):
        if s[x].lower() in "aeiou":
            output += vowels[vowel_count]
            vowel_count -= 1
        else:
            output+= s[x]
    return output