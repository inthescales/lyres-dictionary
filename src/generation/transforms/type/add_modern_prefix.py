import random

from src.generation.transforms.transform_result import TransformResult
from src.models.morph import Morph
from src.utils.logging import Logger

prefix_filter = { "and": [ { "has-type": "prefix" }, { "not": { "has-tag": "numerical" } }] }

# TODO: Merge with AddPrefixTransform
class AddModernPrefixTransform:
    name = "add modern prefix"
    
    @staticmethod
    def is_eligible(word, context):
        if word.first_morph().get_type() == "prefix":
            return False

        prefixes = context.morphothec.filter_prepends_to(word.get_type(), "modern-english", prefix_filter)
        return len(prefixes) > 0

    @staticmethod
    def override(word):
        return False

    @staticmethod
    def weight(word):
        return 5

    @staticmethod
    def apply(word, context):
        env = word.prefix_environment()
        prefixes = context.morphothec.filter_prepends_to(word.get_type(), "modern-english", prefix_filter)
        prefixes = [pref for pref in prefixes if Morph.with_key(pref, context.morphothec).meets_requirements(env)]

        if len(prefixes) > 0:
            choice = random.choice(prefixes)
            new_morph = Morph.with_key(choice, context.morphothec)
            word.add_prefix(new_morph)
            return TransformResult(True)
        else:
            return TransformResult(False)
