from env import Env
from src.entry import Entry
from src.formset import LeafAndStemFormSet, SingleFormSet
from src.morph import Morph
from src.morph_view import MorphView
from src.word import Word

def entry() -> Entry:
    """Generates and returns an entry for a new word"""
    return Entry(word())

def word() -> Word:
    """Generates and returns a new word"""

    root: MorphView = MorphView(
        Morph(
            SingleFormSet("magn"),
            gloss="large"
        )
    )

    suffix: MorphView = MorphView(
        Morph(
            LeafAndStemFormSet("ificat", "ify"),
            gloss="[make] %(@)"
        )
    )

    suffix2: MorphView = MorphView(
        Morph(
            SingleFormSet("ion"),
            gloss="the act or state of %(part)"
        )
    )

    word: Word = Word(root)
    word.add_suffix(suffix)
    word.add_suffix(suffix2)
    return word
