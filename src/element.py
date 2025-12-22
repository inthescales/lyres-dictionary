from abc import ABC

from env import ElementBase, Env

class Element(ElementBase, ABC):
    """
    Base class representing all word-elements.
    An element is any discernible part of a word's form. It usually, but not necessarily, contributes to the word's
    meaning.
    """
    def __init__(self, env: Env):
        self.env = env
