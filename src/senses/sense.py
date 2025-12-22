from src.elements.env import Env
from src.senses.countability import Countability
from src.senses.gloss_provider import GlossProvider

class Sense:
    """
    The sense of a meaningful element, including a gloss provider and related semantic properties.
    Subclasses should also add type-specific syntactic properties needed for rendering.
    """
    def __init__(self, gloss_provider: GlossProvider):
        self.gloss_provider: GlossProvider = gloss_provider

    def gloss(self, env: Env) -> str:
        return self.gloss_provider.gloss(env)

class NounSense(Sense):
    """A sense with additional properties for rendering noun glosses."""
    def __init__(self, gloss_provider: GlossProvider, countability: Countability):
        super().__init__(gloss_provider)
        self.countability: Countability = countability
