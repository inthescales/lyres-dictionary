import random

from src.models.morph import Morph
from src.utils.logging import Logger

class AddSuffixTransform:
    name = "add suffix"
    
    @staticmethod
    def is_eligible(word, context):
        last_morph = word.last_morph()
        return last_morph.is_root() or last_morph.suffixes() == None or len(last_morph.suffixes()) > 0

    @staticmethod
    def override(word):
        return word.last_morph().has_tag("suffix-only")

    @staticmethod
    def weight(word):
        if word.root_morph().has_tag("past-participle"):
            return 5
        else:
            return 100

    @staticmethod
    def apply(word, context):
        new_morph = None
        
        if word.last_morph().suffixes() == None:
            # For morphs with unrestricted suffixing, choose based on type
            env = word.suffix_environment()
            suffixes = context.morphothec.filter_appends_to(word.get_type(), word.get_origin())
            suffixes = [suff for suff in suffixes if Morph.with_key(suff, context.morphothec).meets_requirements(env)]
    
            if len(suffixes) > 0:        
                choice = random.choice(suffixes)
                new_morph = Morph.with_key(choice, context.morphothec)
            else:
                Logger.error("No valid suffixes following morph:")
                Logger.error(" - " + word.last_morph().morph)
                
        else:
            # For words ending in suffixes with restriction, choose from their valid list
            suffixes = word.last_morph().suffixes()
            choice = random.choice(suffixes)
            new_morph = Morph.with_key(choice, context.morphothec)
            
        if new_morph is not None:
            word.add_suffix(new_morph)
            return True
        else:
            return False
