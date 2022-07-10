"""Madlibs Stories."""


class Story:
    """Madlibs story.

    To  make a story, pass a list of prompts, and the text
    of the template.

        >>> s = Story(["noun", "verb"],
        ...     "I love to {verb} a good {noun}.")

    To generate text from a story, pass in a dictionary-like thing
    of {prompt: answer, promp:answer):

        >>> ans = {"verb": "eat", "noun": "mango"}
        >>> s.generate(ans)
        'I love to eat a good mango.'
    """

    def __init__(self, words, text):
        """Create story with words and template text."""

        self.prompts = words
        self.template = text

    def generate(self, answers):
        """Substitute answers into text."""

        text = self.template

        for (key, val) in answers.items():
            text = text.replace("{" + key + "}", val)

        return text


# Here's a story to get you started


story = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """Once upon a time in a long-ago {place}, there lived a
       large {adjective} {noun}. It loved to {verb} {plural_noun}."""
)

story1 = Story(
    ["adjective","type_of_bird","room_in_house","verb_past","verb","relative_name","noun","a_liquid", "ing_verb","plural_body_part",],
    """
    Woke up to the {adjective} smell of {type_of_bird} roasting in the
    {room_in_house} downstairs. I {verb_past} down the stairs to see if I could help
    {verb} the dinner. My mom said, "See if {relative_name} needs a fresh {noun}."
    So I carried a tray of glasses full of {a_liquid} into the {ing_verb}. When I got there I
    couldn't believe my {plural_body_part} 
    """
)

stories = [story, story1]