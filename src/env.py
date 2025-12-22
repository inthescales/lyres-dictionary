from abc import ABC, abstractmethod
from typing import Optional

class AbstractElement(ABC):
    """Abstract base of Element needed to prevent circular import between Element and Env"""
    @property
    @abstractmethod
    def form(self) -> str:
        pass

class Env:
    """The environment that an element finds itself in within a given word"""
    def __init__(self, prev: Optional[AbstractElement] = None, next: Optional[AbstractElement] = None):
        self.prev = prev
        self.next = next
