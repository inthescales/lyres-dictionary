import random

from src.generation.transforms.transform_result import TransformResult
from src.models.morph import Morph
from src.utils.logging import Logger

relational_suffixes = {
    "latin": ["-ate", "-al", "-al", "-ary", "-ify"],
    "greek": ["-ic", "-y-relative", "-ize/greek"]
}

class RelationalCircumfixTransform:
    name = "relational circumfix"
    
    @staticmethod
    def is_eligible(word, context):
        return word.get_origin() in relational_suffixes and word.size() == 1 and word.get_type() == "noun"

    @staticmethod
    def override(word):
        return False

    @staticmethod
    def weight(word):
        return 10

    @staticmethod
    def apply(word, context):
        language = word.get_origin()

        env = word.prefix_environment()
        prepositions = context.morphothec.filter_prepends_to(word.get_type(), language, { "has-type": "prep" })
        prepositions = [prep for prep in prepositions if Morph.with_key(prep, context.morphothec).meets_requirements(env)]

        if len(prepositions) > 0:
            prep_morph = Morph.with_key(random.choice(prepositions), context.morphothec)
            end_morph = Morph.with_key(random.choice(relational_suffixes[language]), context.morphothec)
            word.add_affixes(prep_morph, end_morph)
            return TransformResult(True)
        else:
            return TransformResult(False)
