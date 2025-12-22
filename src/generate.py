from src.senses.countability import Countability
from src.entry import Entry
from src.formset import LeafAndStemFormSet, SingleFormSet
from src.senses.gloss_provider import SingleGlossProvider
from src.morphs.morph import Morph
from src.morphs.morph_view import MorphView
from src.senses.sense import NounSense, Sense
from src.word import Word

def entry() -> Entry:
    """Generates and returns an entry for a new word"""
    return Entry(word())

def word() -> Word:
    """Generates and returns a new word"""

    root: MorphView = MorphView(
        Morph(
            SingleFormSet("magn"),
            Sense(SingleGlossProvider("large"))
        )
    )

    suffix: MorphView = MorphView(
        Morph(
            LeafAndStemFormSet("ificat", "ify"),
            Sense(SingleGlossProvider("[make] %(@)"))
        )
    )

    suffix2: MorphView = MorphView(
        Morph(
            SingleFormSet("ion"),
            NounSense(SingleGlossProvider("the act or state of %(part)"), Countability.uncountable)
        )
    )

    word: Word = Word(root)
    word.add_suffix(suffix)
    word.add_suffix(suffix2)
    return word
