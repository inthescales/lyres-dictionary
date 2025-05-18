import random

from src.models.morph import Morph
from src.utils.logging import Logger

numerical_suffixes = {
    "latin": ["-al-number"],
    "greek": ["-ic-number", "-y-number"],
    "old-english": ["-ed-having"]
}

class NumericalCircumfixTransform:
    name = "numerical circumfix"
    
    @staticmethod
    def is_eligible(word, context):
        return word.get_origin() in numerical_suffixes \
            and word.size() == 1 \
            and word.get_type() == "noun" \
            and word.root_morph().has_tag("count")

    @staticmethod
    def override(word):
        return False

    @staticmethod
    def weight(word):
        return 5

    @staticmethod
    def apply(word, context):
        language = word.get_origin()

        env = word.prefix_environment()
        numbers = context.morphothec.filter_prepends_to(word.get_type(), language, { "has-tag": "numerical" })
        numbers = [num for num in numbers if Morph.with_key(num, context.morphothec).meets_requirements(env)]

        if len(numbers) > 0:
            num_morph = Morph.with_key(random.choice(numbers) , context.morphothec)
            end_morph = Morph.with_key(random.choice(numerical_suffixes[language]), context.morphothec)
            word.add_affixes(num_morph, end_morph)
            return True
        else:
            return False
