import src.test_morphs as test_morphs

from src.entry import Entry
from src.word import Word

def entry() -> Entry:
    """Generates and returns an entry for a new word"""
    return Entry(word())

def word() -> Word:
    """Generates and returns a new word"""

    word: Word = Word(test_morphs.magnus)
    word.add_suffix(test_morphs.ify)
    word.add_suffix(test_morphs.ion)

    return word
