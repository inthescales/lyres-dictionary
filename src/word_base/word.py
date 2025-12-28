from typing import Optional

import glosses as gloss
from word_base.element.element import Element
from word_base.element.meaningful_element import MeaningfulElement
from word_base.element.classes.affix_classes import DeriveClassData
from word_base.element.classes.element_class import ElementClass
from word_base.word_class import WordClass

class ElementClassException(Exception):
    """Exception to be raised when a word's elements have incoherent lexical classes."""
    def __init__(self, message: str):
        self.args = ([message], message)

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
        f: str = ""
        for element in self._form_elements:
            f += element.form

        return f

    @property
    def type(self) -> WordClass:
        """The type of the word"""
        e_type: ElementClass = self._meaning_elements[0].lex_class
        for element in self._meaning_elements[1:]:
            class_data = element.class_data
            if element.lex_class == ElementClass.derive and isinstance(class_data, DeriveClassData):
                e_type = class_data.result_data.lex_class
            else:
                raise ElementClassException("Found unexpected non-derive type '" + str(element.lex_class) + "' in word's elements-by-meaning list.")

        return WordClass.from_element_type(e_type)

    @property
    def definition(self) -> str:
        """The word's definition as a string"""
        definition: str = self._meaning_elements[0].gloss
        prev_element: MeaningfulElement = self._meaning_elements[0]
        for element in self._meaning_elements[1:]:
            definition = gloss.substitute(prev_element.sense, element.gloss, definition)
            prev_element = element

        return definition

    @property
    def head_element(self) -> Optional[Element]:
        return self._form_elements[0]

    @property
    def tail_element(self) -> Optional[Element]:
        return self._form_elements[-1]
