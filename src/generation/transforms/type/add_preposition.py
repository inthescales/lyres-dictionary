import random

from src.generation.transforms.transform_result import TransformResult
from src.models.morph import Morph

class AddPrepositionTransform:
    name = "add prepositional prefix"
    
    @staticmethod
    def is_eligible(word, context):
        return word.get_type() == "verb" and word.size() == 1 and not word.last_morph().has_tag("no-prep")

    @staticmethod
    def override(word):
        return word.first_morph().has_tag("always-prep")

    @staticmethod
    def weight(word):
        if word.get_origin() == "greek" and not word.root_morph().has_tag("motion"):
            return 10
        else:
            return 33
    
    @staticmethod
    def apply(word, context):
        env = word.prefix_environment()
        prepositions = context.morphothec.filter_prepends_to(word.get_type(), word.get_origin(), { "has-type": "prep" })
        prepositions = [prep for prep in prepositions if Morph.with_key(prep, context.morphothec).meets_requirements(env)]
                
        if len(prepositions) > 0:
            choice = random.choice(prepositions)
            new_morph = Morph.with_key(choice, context.morphothec)
            word.add_prefix(new_morph)
            return TransformResult(True)
        else:
            return TransformResult(False)
