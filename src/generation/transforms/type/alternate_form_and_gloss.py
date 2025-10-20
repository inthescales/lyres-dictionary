import random

import src.generation.derivative_morphs as derivative_morph

from src.generation.transforms.transform_result import TransformResult

# TODO: Instead of a custom morph, should this be part of a morphs 'fixing' process?
class AlternateFormAndGlossTransform:
    name = "alternate form and gloss"
    
    @staticmethod
    def is_eligible(word, context):
        return context.alternate_form != None and context.alternate_gloss != None

    @staticmethod
    def override(word):
        return False

    @staticmethod
    def weight(word):
        return 30

    @staticmethod
    def apply(word, context):
        new_morph = derivative_morph.with_alternate_form_and_gloss(word.root_morph(), context.alternate_form, context.alternate_gloss)
        word.set_morphs([new_morph])

        # Half of the time, let this be a free transform
        if random.randint(1, 2) > 1:
            return TransformResult(True, free=True)
        else:
            return TransformResult(True)
