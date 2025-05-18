import random

import src.generation.derivative_morphs as derivative_morph
import src.evolutor.evolutor as evolutor

from src.evolutor.engine.config import Config

class PastParticipleTransform:
    name = "past participle"
    
    @staticmethod
    def is_eligible(word, context):
        root_morph = word.root_morph()
        return word.get_origin() == "old-english" \
            and root_morph.get_type() == "verb" \
            and root_morph.has_tag("transitive") \
            and (
                root_morph.morph["verb-class"] != "weak"
                or (
                    not root_morph.has_tag("obscure")
                    and not root_morph.has_tag("speculative"))
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

        config = Config(overrides=[["PPart:use-strong", True], ["OSL:iy", False], ["OSL:u", False]])
        form = root_morph.morph["form-raw"]
        if isinstance(form, list):
            form = random.choice(form)
        past_participle_form = evolutor.get_participle_form(form, root_morph.morph["verb-class"], config)

        is_common = (not root_morph.has_tag("obscure") and not root_morph.has_tag("speculative"))
        canon_participles = []
        if "form-participle-canon" in root_morph.morph:
            canon_participles = root_morph.morph["form-participle-canon"]

        new_morph = derivative_morph.from_past_participle(root_morph, past_participle_form)
        word.set_morphs([new_morph])

        return True

        # TODO: Return this behavior when I have a more complex return type
        # HACK: I want common participles to always be put through at least one more transform.
        # Pretend that we failed a transform if the participle is in the canon list.
        # This only applies to common roots.
        #
        # Also do this randomly for all participles
        # if (
        #     len(canon_participles) > 0
        #     and new_morph.morph["form-final"] in canon_participles \
        #     and is_common \
        #    ) \
        #     or random.randint(0, 9) == 0:
        #     return False
