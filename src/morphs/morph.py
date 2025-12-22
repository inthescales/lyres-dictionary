from src.formset import FormSet
from src.senses.sense import Sense

class Morph():
    """
    Representation of a morpho-etymological element at a particular point in time.
    It may also contain forward-looking information on that element's reflexes and
    usage in later occurrences.
    """

    def __init__(self, formset: FormSet, sense: Sense):
        self._formset = formset
        self._sense = sense

    @property
    def formset(self) -> FormSet:
        """The formset associated with this morph"""
        return self._formset

    @property
    def sense(self) -> Sense:
        """The gloss associated with this morph"""
        return self._sense
