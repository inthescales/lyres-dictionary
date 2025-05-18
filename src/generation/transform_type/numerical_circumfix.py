import random

from src.models.morph import Morph
from src.utils.logging import Logger

numerical_suffixes = {
    "latin": ["-al-number"],
    "greek": ["-ic-number", "-y-number"],
    "old-english": ["-ed-having"]
}

class NumericalCircumfixTransform:
    @staticmethod
    def is_eligible(word):
        return word.get_origin() in numerical_suffixes \
            and word.size() == 1 \
            and word.get_type() == "noun" \
            and word.root_morph().has_tag("count")

    @staticmethod
    def override(word):
        return False

    @staticmethod
    def apply(word, morphothec):
        language = word.get_origin()

        env = word.prefix_environment()
        numbers = morphothec.filter_prepends_to(word.get_type(), language, { "has-tag": "numerical" })
        numbers = [num for num in numbers if Morph.with_key(num, morphothec).meets_requirements(env)]

        if len(numbers) > 0:
            num_morph = Morph.with_key(random.choice(numbers) , morphothec)
            end_morph = Morph.with_key(random.choice(numerical_suffixes[language]), morphothec)
            word.add_affixes(num_morph, end_morph)
            return True
        else:
            return False
