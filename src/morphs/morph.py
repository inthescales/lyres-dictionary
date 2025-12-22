from src.formset import FormSet

class Morph:
    """
    Representation of a morpho-etymological element at a particular point in time.
    It may also contain forward-looking information on that element's reflexes and
    usage in later occurrences.
    """

    def __init__(self, formset: FormSet, gloss: str):
        self._formset = formset
        self._gloss = gloss

    @property
    def formset(self) -> FormSet:
        """The formset associated with this morph"""
        return self._formset

    @property
    def gloss(self) -> FormSet:
        """The gloss associated with this morph"""
        return self._gloss
