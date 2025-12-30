import word_base.composition.gloss as gloss

from word_base.word_class import WordClass
from word_base.element.classes.affix_classes import DeriveClassData
from word_base.element.classes.element_class import ElementClass
from word_base.element.element import Element
from word_base.element.meaningful_element import MeaningfulElement

class ElementClassException(Exception):
    """Exception to be raised when a word's elements have incoherent lexical classes."""
    def __init__(self, message: str):
        self.args = ([message], message)

def form(elements: list[Element]) -> str:
    """Composes a final form for the list of form elements and returns it as a string"""
    f: str = ""
    for element in elements:
        f += element.form

    return f

def type(elements: list[MeaningfulElement]) -> WordClass:
    """Determines the final type of the list of meaning elements and returns it as a WordType"""
    e_type: ElementClass = elements[0].lex_class
    for element in elements[1:]:
        class_data = element.class_data
        if element.lex_class == ElementClass.derive and isinstance(class_data, DeriveClassData):
            e_type = class_data.result_data.lex_class
        else:
            raise ElementClassException(
                "Found unexpected non-derive type '" + str(element.lex_class) + "' in word's elements-by-meaning list.")

    return WordClass.from_element_type(e_type)

def definition(elements: list[MeaningfulElement]) -> str:
    """Composes a definition string based on the list of meaningful elements, in transformation order, and returns it."""
    definition: str = elements[0].gloss
    prev_element: MeaningfulElement = elements[0]
    for element in elements[1:]:
        definition = gloss.substitute(prev_element.sense, element.gloss, definition)
        prev_element = element

    return definition