import random

from src.models.morph import Morph
from src.utils.logging import Logger

relational_suffixes = {
    "latin": ["-ate", "-al", "-al", "-ary", "-ify"],
    "greek": ["-ic", "-y-relative", "-ize/greek"]
}

class RelationalCircumfixTransform:
    @staticmethod
    def is_eligible(word):
        return word.get_origin() in relational_suffixes and word.size() == 1 and word.get_type() == "noun"

    @staticmethod
    def override(word):
        return False

    @staticmethod
    def apply(word, morphothec):
        language = word.get_origin()

        env = word.prefix_environment()
        prepositions = morphothec.filter_prepends_to(word.get_type(), language, { "has-type": "prep" })
        prepositions = [prep for prep in prepositions if Morph.with_key(prep, morphothec).meets_requirements(env)]

        if len(prepositions) > 0:
            prep_morph = Morph.with_key(random.choice(prepositions), morphothec)
            end_morph = Morph.with_key(random.choice(relational_suffixes[language]), morphothec)
            word.add_affixes(prep_morph, end_morph)
            return True
        else:
            return False
