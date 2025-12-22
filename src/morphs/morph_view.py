from src.elements.env import Env
from src.forms.form_provider import FormProvider
from src.morphs.morph import Morph
from src.senses.meaningful import MeaningfulElement
from src.senses.sense import Sense

class MorphView(MeaningfulElement):
    """
    Element comprised of a morph and all information necessary to determine what
    portion of that morph's total data should be used.
    """

    def __init__(self, morph: Morph, env: Env = Env()):
        super().__init__(env)
        self.morph: Morph = morph
        self.env: Env = env
        self.form_provider: FormProvider = FormProvider.for_formset(morph.formset)
        self._sense: Sense = morph.sense

    @property
    def form(self) -> str:
        return self.form_provider.form(self.env)

    @property
    def sense(self) -> Sense:
        return self._sense
