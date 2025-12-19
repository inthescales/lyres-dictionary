import src.utils.logging as log

from abc import ABC, abstractmethod
from src.env import Env
from src.formset import FormSet, LeafAndStemFormSet, SingleFormSet
from typing import Self

# Being provisioned with the necessary data, a FormProvider is able to return the particular form
# to be used in any given environment.
class FormProvider(ABC):
    # Return the form to be used based on the given environment
    @abstractmethod
    def form(self, env: Env) -> str:
        pass

    # Instantiates and returns a FormProvider appropriate to the given FormSet type
    @classmethod
    def for_formset(cls, formset: FormSet) -> Self:
        if isinstance(formset, SingleFormSet):
            return SingleFormProvider(formset)
        if isinstance(formset, LeafAndStemFormSet):
            return LeafAndStemFormProvider(formset)

        log.error("unable to initialize FormProvider for formset of type '" + str(type(formset)) + "'")
        exit(1)

# Form provider when a single, constant form is used
class SingleFormProvider(FormProvider):
    def __init__(self, formset: SingleFormSet):
        self._formset: SingleFormSet = formset

    def form(self, env: Env) -> str:
        return self._formset.form

# Form provider when the form depends on whether another element follows the current one
class LeafAndStemFormProvider(FormProvider):
    def __init__(self, formset: LeafAndStemFormSet):
        self._formset: LeafAndStemFormSet = formset

    def form(self, env: Env) -> str:
        if env.next is None:
            return self._formset.leaf
        else:
            return self._formset.stem
