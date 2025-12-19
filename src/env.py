from src.morph import Morph
from typing import Optional

# The environment that an element finds itself in within a given word
class Env:
    def __init__(self, prev: Optional[Morph], next: Optional[Morph]):
        self.prev = prev
        self.next = next
        return
