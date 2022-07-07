"""Word Finder: finds random words from a dictionary."""
from random import choice
class WordFinder:
    """Gets Random Word From a File
    
    >>> wf = WordFinder("/home/aprylle/springboard-exercises/python-oo-practice/test.txt")
    3 words read
    
    >>> wf.random() in ["Apple", "Batman", "Cat"]
    True
    
    >>> wf.random() in ["Apple", "Batman", "Cat"]
    True
    """
    def __init__(self, file_path):
        self.path = file_path
        self.words = self.get_words(file_path)
        print(f"{len(self.words)} words read")
    
    def get_words(self, p):
        file = open(p, 'r')
        words = [line.strip() for line in file]
        file.close()
        return words

    def random(self):
        return choice(self.words)


class SpecialWordFinder(WordFinder):
    """Random Word Finder that will disregard Spaces and Comments(#)
    
    >>> wf1 = SpecialWordFinder("/home/aprylle/springboard-exercises/python-oo-practice/test1.txt")
    3 words read

    >>> wf1.random() in ['Apple', 'Batman', 'Dog']
    True

    >>> wf1.random() in ['Apple', 'Batman', 'Dog']
    True
    """
    def __init__(self, file_path):
        super().__init__(file_path)
    
    def get_words(self, p):
        file = open(p, 'r') 
        words = [line.strip() for line in file if line.strip() and line[0] != '#']
        file.close()
        return words