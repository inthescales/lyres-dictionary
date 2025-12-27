from src.forms.formset import FormSet
from src.senses.sense import Sense
from src.types.element_type import TypeData

class Morph():
    """
    Representation of a morpho-etymological element at a particular point in time.
    It may also contain forward-looking information on that element's reflexes and
    usage in later occurrences.
    """

    def __init__(self, formset: FormSet, type_data: TypeData, sense: Sense):
        self._formset = formset
        self._type_data = type_data
        self._sense = sense

    @property
    def formset(self) -> FormSet:
        """The formset belonging to this morph"""
        return self._formset

    @property
    def type_data(self) -> TypeData:
        """The type and any associated data belonging to this morph"""
        return self._type_data

    @property
    def sense(self) -> Sense:
        """The gloss belonging to with this morph"""
        return self._sense
