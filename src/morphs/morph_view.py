from src.elements.element import Element
from src.elements.env import Env
from src.form_provider import FormProvider
from src.gloss_provider import GlossProvider
from src.gloss_provider import SingleGlossProvider
from src.morphs.morph import Morph

class MorphView(Element):
    """
    Element comprised of a morph and all information necessary to determine what
    portion of that morph's total data should be used.
    """

    def __init__(self, morph: Morph, env: Env = Env()):
        self.morph = morph
        self.env = env
        self.form_provider: FormProvider = FormProvider.for_formset(morph.formset)
        self.gloss_provider: GlossProvider = SingleGlossProvider(morph.gloss)

    @property
    def form(self) -> str:
        return self.form_provider.form(self.env)

    @property
    def gloss(self) -> str:
        return self.gloss_provider.gloss(self.env)
