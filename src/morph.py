from src.formset import FormSet

# Contains all data for a morpho-etymological element
class Morph:
    def __init__(self, formset: FormSet):
        self._formset = formset

    @property
    def formset(self) -> FormSet:
        return self._formset
