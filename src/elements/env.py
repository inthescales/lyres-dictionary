from typing import Optional

from src.elements.element_base import ElementBase

class Env:
    """The environment that an element finds itself in within a given word"""

    def __init__(self, prev: Optional[ElementBase] = None, next: Optional[ElementBase] = None):
        self.prev = prev
        self.next = next
