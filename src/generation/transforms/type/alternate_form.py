import src.generation.derivative_morphs as derivative_morph

from src.generation.transforms.transform_result import TransformResult

# TODO: Instead of a custom morph, should this be handled with some kind of 'presentation context'?
class AlternateFormTransform:
    name = "alternate form"
    
    @staticmethod
    def is_eligible(word, context):
        return not word.root_morph().has_tag("obscure") \
            and not word.root_morph().has_tag("speculative") \
            and context.alternate_form != None

    @staticmethod
    def override(word):
        return False

    @staticmethod
    def weight(word):
        return 10

    @staticmethod
    def apply(word, context):
        new_morph = derivative_morph.with_alternate_form(word.root_morph(), context.alternate_form, context.canon_form)
        word.set_morphs([new_morph])
        return TransformResult(True)

        # TODO: Add a small chance to not use the special gloss, and return False
        # so we can get more transforms with an alternate form
