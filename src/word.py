from src.env import Env
from src.morph import Morph
from src.morph_view import Element, MorphView
from typing import Optional

# A word
class Word:
    def __init__(self, elements: Optional[list[Element]]=None):
        if elements is None:
            elements = []

        self._elements: list[Element] = elements

    def set_morphs(self, morphs: list[Morph]) -> None:
        for i in range(0, len(morphs)):
            env: Env = Env(
                prev=morphs[i-1] if i > 0 else None,
                next=morphs[i+1] if i < len(morphs) - 1 else None
            )
            self._elements.append(MorphView(morph=morphs[i], env=env))

    def form(self):
        f: str = ""
        for element in self._elements:
            f += element.form

        return f

    def type(self):
        return "noun"

    def definition(self):
        return "definition"
