from abc import ABC

# Representing all forms of a morph that are part of the same complex
class FormSet(ABC):
    pass

# FormSet for elements having only a single constant form
class SingleFormSet(FormSet):
    def __init__(self, form):
        self._form = form

    @property
    def form(self) -> str:
        return self._form

# FormSet for elements having a form that varies depending on whether another element follows
class LeafAndStemFormSet(FormSet):
    def __init__(self, stem, leaf):
        self._stem = stem
        self._leaf = leaf

    @property
    def stem(self) -> str:
        return self._stem

    @property
    def leaf(self) -> str:
        return self._leaf
