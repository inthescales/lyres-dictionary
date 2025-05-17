import random

from src.models.morph import Morph
from src.utils.logging import Logger

class AddPrepositionTransform:
    @staticmethod
    def is_eligible(word):
        return word.get_type() == "verb" and word.size() == 1 and not word.last_morph().has_tag("no-prep")

    @staticmethod
    def override(word):
        return word.first_morph().has_tag("always-prep")

    @staticmethod
    def apply(word, morphothec):
        env = word.prefix_environment()
        prepositions = morphothec.filter_prepends_to(word.get_type(), word.get_origin(), { "has-type": "prep" })
        prepositions = [prep for prep in prepositions if Morph.with_key(prep, morphothec).meets_requirements(env)]
                
        if len(prepositions) > 0:
            choice = random.choice(prepositions)
            new_morph = Morph.with_key(choice, morphothec)
            word.add_prefix(new_morph)
            return True
        else:
            return False
