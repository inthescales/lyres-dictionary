from word_base.element.env import Env
from word_base.forms.form_provider import FormProvider
from lex_data.morphs.morph import Morph
from word_base.element.meaningful_element import MeaningfulElement
from word_base.senses.sense import Sense
from word_base.element.classes.element_class import ClassData

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
    def class_data(self) -> ClassData:
        return self.morph.class_data

    @property
    def sense(self) -> Sense:
        return self._sense
