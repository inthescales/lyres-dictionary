from abc import ABC, abstractmethod
from typing import Self

import utils.logging as log
from word_base.element.env import Env
from word_base.forms.formset import FormSet, LeafAndStemFormSet, SingleFormSet

class FormProvider(ABC):
    """
    Being provisioned with the necessary data, a FormProvider is able to return the particular form
    to be used in any given environment.
    """

    @abstractmethod
    def form(self, env: Env) -> str:
        """Returns the form to be used based on the given environment"""
        pass

    @classmethod
    def for_formset(cls, formset: FormSet) -> Self:
        """Instantiates and returns a FormProvider appropriate to the given FormSet type"""

        if isinstance(formset, SingleFormSet):
            return SingleFormProvider(formset)
        if isinstance(formset, LeafAndStemFormSet):
            return LeafAndStemFormProvider(formset)

        log.error("unable to initialize FormProvider for formset of type '" + str(type(formset)) + "'")
        exit(1)

class SingleFormProvider(FormProvider):
    """Form provider when a single, constant form is used"""

    def __init__(self, formset: SingleFormSet):
        self._formset: SingleFormSet = formset

    def form(self, env: Env) -> str:
        return self._formset.form

class LeafAndStemFormProvider(FormProvider):
    """Form provider when the form depends on whether another element follows the current one"""

    def __init__(self, formset: LeafAndStemFormSet):
        self._formset: LeafAndStemFormSet = formset

    def form(self, env: Env) -> str:
        if env.prev is None:
            return self._formset.leaf
        else:
            return self._formset.stem
