from enum import Enum
from typing import Protocol

from word_base.element.classes.element_class import ElementClass, ClassData

class AffixPosition(Enum):
    """The position on the word where an affix is to be added."""
    prefix = "prefix"
    suffix = "suffix"

class AffixData(Protocol):
    """Protocol exposing an affix position property."""
    @property
    def position(self) -> AffixPosition:
        pass

class DeriveClassData(ClassData, AffixData):
    """Base class data type for derivational affixes."""
    def __init__(self, position: AffixPosition, result_data: ClassData):
        ClassData.__init__(self, ElementClass.derive)
        self._position = position
        self.result_data = result_data

    @property
    def position(self) -> AffixPosition:
        return self._position

class InflectClassData(ClassData, AffixData):
    """Base class data type for inflectional affixes."""
    def __init__(self, position: AffixPosition):
        ClassData.__init__(self, ElementClass.inflect)
        self._position = position

    @property
    def position(self) -> AffixPosition:
        return self._position
