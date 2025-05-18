import random

from src.models.morph import Morph
from src.utils.logging import Logger

prefix_filter = { "and": [ { "has-type": "prefix" }, { "not": { "has-tag": "numerical" } }] }

# TODO: Merge with AddPrefixTransform
class AddModernPrefixTransform:
    @staticmethod
    def is_eligible(word, morphothec):
        if word.first_morph().get_type() == "prefix":
            return False

        prefixes = morphothec.filter_prepends_to(word.get_type(), "modern-english", prefix_filter)
        return len(prefixes) > 0

    @staticmethod
    def override(word):
        return False

    @staticmethod
    def apply(word, morphothec):
        env = word.prefix_environment()
        prefixes = morphothec.filter_prepends_to(word.get_type(), "modern-english", prefix_filter)
        prefixes = [pref for pref in prefixes if Morph.with_key(pref, morphothec).meets_requirements(env)]

        if len(prefixes) > 0:
            choice = random.choice(prefixes)
            new_morph = Morph.with_key(choice, morphothec)
            word.add_prefix(new_morph)
            return True
        else:
            return False
