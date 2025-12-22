from abc import ABC, abstractmethod

# This class is separated out from the Element class in order to prevent a circular import between Element and Env.

class ElementBase(ABC):
    """Base data belonging to all elements."""
    @property
    @abstractmethod
    def form(self) -> str:
        pass
