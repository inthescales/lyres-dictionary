from word_base.forms.formset import FormSet
from word_base.senses.sense import Sense
from word_base.lexical_class.element_class import ClassData

class Morph:
    """
    Representation of a morpho-etymological element at a particular point in time.
    It may also contain forward-looking information on that element's reflexes and
    usage in later occurrences.
    """

    def __init__(self, formset: FormSet, type_data: ClassData, sense: Sense):
        self._formset = formset
        self._type_data = type_data
        self._sense = sense

    @property
    def formset(self) -> FormSet:
        """The formset belonging to this morph"""
        return self._formset

    @property
    def class_data(self) -> ClassData:
        """The type and any associated data belonging to this morph"""
        return self._type_data

    @property
    def sense(self) -> Sense:
        """The gloss belonging to with this morph"""
        return self._sense
