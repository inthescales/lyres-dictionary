from typing import Optional

from src.morph import Morph

class Env:
    """The environment that an element finds itself in within a given word"""
    def __init__(self, prev: Optional[Morph], next: Optional[Morph]):
        self.prev = prev
        self.next = next
        return
