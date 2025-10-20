import src.generation.derivative_morphs as derivative_morph

from src.generation.transforms.transform_result import TransformResult

# TODO: Instead of a custom morph, should this be part of a morphs 'fixing' process?
class AlternateGlossTransform:
    name = "alternate gloss"
    
    @staticmethod
    def is_eligible(word, context):
        return context.alternate_gloss != None

    @staticmethod
    def override(word):
        return False

    @staticmethod
    def weight(word):
        return 10

    @staticmethod
    def apply(word, context):
        new_morph = derivative_morph.with_alternate_gloss(word.root_morph(), context.alternate_gloss)
        word.set_morphs([new_morph])
        return TransformResult(True)
