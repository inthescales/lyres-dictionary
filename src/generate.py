from src.entry import Entry
from src.formset import LeafAndStemFormSet, SingleFormSet
from src.morph import Morph
from src.word import Word

def entry() -> Entry:
    """Generates and returns an entry for a new word"""
    return Entry(word())

def word() -> Word:
    """Generates and returns a new word"""

    root: Morph = Morph(
        SingleFormSet("magn")
    )

    suffix: Morph = Morph(
        LeafAndStemFormSet("ificat", "ify")
    )

    suffix2: Morph = Morph(
        SingleFormSet("ion")
    )

    word: Word = Word()
    word.set_morphs([root, suffix, suffix2])
    return word
