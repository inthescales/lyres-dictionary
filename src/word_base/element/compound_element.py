import word_base.composition as compose

from word_base.element.classes.element_class import ClassData
from word_base.element.element import Element
from word_base.element.env import Env
from word_base.element.meaningful_element import MeaningfulElement
from word_base.senses.sense import Sense

class CompoundElement(MeaningfulElement):
    def __init__(self, elements: list[Element], lex_data: ClassData, sense: Sense, env: Env = Env()):
        super().__init__(env)
        self.elements = elements
        self._lex_data = lex_data
        self._sense = sense

    @property
    def form(self) -> str:
        return compose.form(self.elements)

    @property
    def class_data(self) -> ClassData:
        return self._lex_data

    @property
    def sense(self) -> Sense:
        return self._sense