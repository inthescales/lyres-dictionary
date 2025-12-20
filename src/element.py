from abc import ABC, abstractmethod

class Element(ABC):
    """An element that makes up part of a word"""

    @property
    @abstractmethod
    def form(self) -> str:
        pass
