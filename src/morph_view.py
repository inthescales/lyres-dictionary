from src.element import Element
from src.env import Env
from src.form_provider import FormProvider
from src.morph import Morph

# Element comprised of a morph and all information necessary to determine what portion of that morph's
# total data should be used.
class MorphView(Element):
    def __init__(self, morph: Morph, env: Env):
        self.morph = morph
        self.env = env
        self.form_provider: FormProvider = FormProvider.for_formset(morph.formset)

    @property
    def form(self) -> str:
        return self.form_provider.form(self.env)
