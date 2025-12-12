import random

import src.generation.derivative_morphs as derivative_morph

from src.generation.transforms.transform_result import TransformResult

class PastParticipleTransform:
    name = "past participle"
    
    @staticmethod
    def is_eligible(word, context):
        root_morph = word.root_morph()

        return context.past_participle_form != None \
            and word.get_origin() == "old-english" \
            and root_morph.get_type() == "verb" \
            and root_morph.has_tag("transitive") \
            and (
                root_morph.morph["verb-class"] != "weak"
                or (
                    root_morph.has_tag("obscure")
                    or root_morph.has_tag("speculative"))
            )

    @staticmethod
    def override(word):
        return False

    @staticmethod
    def weight(word):
        return 20

    @staticmethod
    def apply(word, context):
        root_morph = word.root_morph()
        i = word.morphs.index(root_morph)
        env = word.environment_for_index(i)

        new_morph = derivative_morph.from_past_participle(root_morph, env, context.past_participle_form)
        word.set_morphs([new_morph])

        is_common = (not root_morph.has_tag("obscure") and not root_morph.has_tag("speculative"))
        canon_participles = []
        if "form-participle-canon" in root_morph.morph:
            canon_participles = root_morph.morph["form-participle-canon"]

        # For common participles this transform is free.
        # For others, let it be free on a random basis.
        if (
            len(canon_participles) > 0
            and new_morph.morph["form-final"] in canon_participles \
            and is_common \
           ) \
            or random.randint(0, 9) == 0:
            return TransformResult(True, free=True)
        else:
            return TransformResult(True)
