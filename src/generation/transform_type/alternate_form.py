import random

import src.generation.derivative_morphs as derivative_morph

from src.models.morph import Morph
from src.utils.logging import Logger

# TODO: Instead of a custom morph, should this be handled with some kind of 'presentation context'?
class AlternateFormTransform:
    name = "alternate form"
    
    @staticmethod
    def is_eligible(word, context):
        return context.alternate_form != None

    @staticmethod
    def override(word):
        return False

    @staticmethod
    def weight(word):
        return 10

    @staticmethod
    def apply(word, context):
        new_morph = derivative_morph.with_alternate_form(word.root_morph(), context.alternate_form)
        word.set_morphs([new_morph])
        return True

        # TODO: Add a small chance to not use the special gloss, and return False
        # so we can get more transforms with an alternate form
