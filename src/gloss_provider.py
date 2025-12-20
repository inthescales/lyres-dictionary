from abc import ABC

from src.env import Env

class GlossProvider(ABC):
    """
    Being provisioned with the necessary data, a GlossProvider is able to return the particular gloss
    to be used in any given environment.
    """
    def gloss(self, env: Env) -> str:
        pass

class SingleGlossProvider(GlossProvider):
    """Gloss provider when a single, constant form is used"""

    def __init__(self, gloss: str):
        self._gloss = gloss

    def gloss(self, env: Env) -> str:
        return self._gloss
