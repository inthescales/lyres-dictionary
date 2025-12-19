from abc import ABC, abstractmethod

# An element that makes up part of a word
class Element(ABC):
    @property
    @abstractmethod
    def form(self) -> str:
        pass
