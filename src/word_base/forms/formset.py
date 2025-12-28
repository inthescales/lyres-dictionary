from abc import ABC

class FormSet(ABC):
    """Representing all forms of a morph that are part of the same complex"""
    pass

class SingleFormSet(FormSet):
    """FormSet for element having only a single constant form"""

    def __init__(self, form):
        self._form = form

    @property
    def form(self) -> str:
        return self._form

class StemAndLeafFormSet(FormSet):
    """FormSet for element having a form that varies depending on whether another element follows"""

    def __init__(self, stem, leaf):
        self._stem = stem
        self._leaf = leaf

    @property
    def stem(self) -> str:
        return self._stem

    @property
    def leaf(self) -> str:
        return self._leaf
