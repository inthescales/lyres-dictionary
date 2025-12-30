from typing import Optional

import word_base.composition as compose

from word_base.element.element import Element
from word_base.element.meaningful_element import MeaningfulElement
from word_base.word_class import WordClass

class Word:
    """Representation of a word as a collection of elements."""

    def __init__(self, root: Element):
        self._form_elements: list[Element] = [root]
        self._meaning_elements: list[MeaningfulElement] = []
        if isinstance(root, MeaningfulElement):
            self._meaning_elements = [root]


    def add_prefix(self, prefix: Element):
        prefix.env.next = self.head_element
        self.head_element.env.prev = prefix
        self._form_elements = [prefix] + self._form_elements

        if isinstance(prefix, MeaningfulElement):
            self._meaning_elements.append(prefix)

    def add_suffix(self, suffix: Element):
        suffix.env.prev = self.tail_element
        self.tail_element.env.next = suffix
        self._form_elements.append(suffix)

        if isinstance(suffix, MeaningfulElement):
            self._meaning_elements.append(suffix)

    @property
    def form(self) -> str:
        """The word's form as a string"""
        return compose.form(self._form_elements)

    @property
    def type(self) -> WordClass:
        """The type of the word"""
        return compose.type(self._meaning_elements)

    @property
    def definition(self) -> str:
        """The word's definition as a string"""
        return compose.definition(self._meaning_elements)

    @property
    def head_element(self) -> Optional[Element]:
        return self._form_elements[0]

    @property
    def tail_element(self) -> Optional[Element]:
        return self._form_elements[-1]
