from abc import ABC

from word_base.element.element_base import ElementBase
from word_base.element.env import Env

class Element(ElementBase, ABC):
    """
    Base class representing all word-element.
    An element is any discernible part of a word's form. It usually, but not necessarily, contributes to the word's
    meaning.
    """

    def __init__(self, env: Env):
        self.env = env
