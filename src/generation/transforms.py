import random

import src.models

import src.generation.former as former
import src.utils.helpers as helpers

from src.models.word import Word
from src.models.morph import Morph
from src.morphs.morphothec import Morphothec
from src.utils.logging import Logger

def seed_word(word, morphothec):
    bag = [
        # ("latin", morphothec.root_count_for_language("latin")),
        # ("greek", morphothec.root_count_for_language("greek")),
        ("old-english", morphothec.root_count_for_language("old-english"))
    ]
    choice = helpers.choose_bag(bag)
    if choice == "latin":
        word.morphs = [get_latin_root(morphothec)]
    elif choice == "greek":
        word.morphs = [get_greek_root(morphothec)]
    elif choice == "old-english":
        word.morphs = [get_old_english_root(morphothec)]

def get_latin_root(morphothec):

    bag = [
        ("noun", 3),
        ("adj", 3),
        ("verb", 5)
    ]

    type_ = helpers.choose_bag(bag)
    key = random.choice(morphothec.filter_type(type_, "latin"))
    morph = Morph(key, morphothec)
    return morph

def get_greek_root(morphothec):

    bag = [
        ("noun", 3),
        ("adj", 1),
        ("verb", 3)
    ]

    type_ = helpers.choose_bag(bag)
    key = random.choice(morphothec.filter_type(type_, "greek"))
    morph = Morph(key, morphothec)
    return morph

def get_old_english_root(morphothec):

    bag = [
        ("noun", 3),
        ("adj", 3),
        ("verb", 3)
    ]

    type_ = helpers.choose_bag(bag)
    key = random.choice(morphothec.filter_type(type_, "old-english"))
    morph = Morph(key, morphothec)
    return morph
 
def transform_word(word, morphothec, is_single):

    language = word.get_origin()
    current_type = word.get_type()

    last_morph = word.last_morph()
    first_morph = word.first_morph()
    root_morph = word.root_morph()
    has_prep = first_morph.get_type() == "prep"
    has_prefix = first_morph.get_type() == "prefix"

    relational_suffixes = []
    numerical_suffixes = []
    if language == "latin":
        relational_suffixes = ["-ate", "-al", "-al", "-ary", "-ify"]
        numerical_suffixes = ["-al-number"]
    elif language == "greek":
        relational_suffixes = ["-ic", "-y-relative", "-ize/greek"]
        numerical_suffixes = ["-ic-number", "-y-number"]
    # elif language == "old-english":
        # numerical_suffixes = ["-ed-having"]

    choice = None
    override = False
    bag = []
    
    # Conditions and probabilities --------------------------
    
    if last_morph.is_root() or last_morph.suffixes() is None or len(last_morph.suffixes()) > 0:
        if last_morph.has_tag("suffix-only"):
            override = True
            choice = "add_suffix"
        else:
            bag.append(("add_suffix", 100))
        
    if word.size() == 1 and current_type == "verb" and not last_morph.has_tag("no-prep") and not has_prep and not has_prefix:
        if last_morph.has_tag("always-prep"):
            override = True
            choice = "add_prep_prefix"
        else:
            if language == "greek" and not first_morph.has_tag("motion"):
                bag.append(("add_prep_prefix", 10))
            else:
                bag.append(("add_prep_prefix", 33))
    
    if word.size() >= 1 and current_type == "verb" and not first_morph.get_type() == "prefix":
        if len(morphothec.filter_prepends_to(current_type, language, { "has-type": "prefix" })) > 0:
            bag.append(("add_prefix", 5))

        if len(morphothec.filter_prepends_to(current_type, language, { "has-type": "prefix" })) > 0:
            bag.append(("add_modern_prefix", 1))

    if len(relational_suffixes) > 0 and word.size() == 1 and current_type == "noun":
        bag.append(("relational", 10))

    if len(numerical_suffixes) > 0 and word.size() == 1 and current_type == "noun" and not last_morph.has_tag("singleton"):
        bag.append(("numerical", 5))

    # See if an alternate form is available
    # TODO: Find a way to generate all possible alt. forms rather than relying on rolling one
    alternate_form = None
    if is_single \
        and "form-canon" in root_morph.morph \
        and not root_morph.has_tag("speculative") \
        and not root_morph.has_tag("obscure"):
            env = word.environment_for_index(0)
            config = former.Former_Config(True, False)
            form = former.form(root_morph, env, config)
            form_canon = root_morph.morph["form-canon"]
            if form != form_canon:
                alternate_form = form

    # Show an alternate form for common words
    if alternate_form != None:
        bag.append(("alternate_form", 10))

    # Show alternate gloss
    if "gloss-alt" in root_morph.morph:
        bag.append(("alternate_gloss", 10))

    # Show alternate form and gloss
    if alternate_form != None \
        and "gloss-alt" in root_morph.morph:
        bag.append(("alternate_form_and_gloss", 30))
        
    # If there is no override, choose, or return False if no choices ------
    if not override: 
        if len(bag) > 0:
            choice = helpers.choose_bag(bag)
        else:
            return False
    
    # Transformations --------------------------

    # Add Suffix
    if choice == "add_suffix":
        
        new_morph = None
        
        if last_morph.suffixes() is None:
            # For morphs with unrestricted suffixing, choose based on type
            env = word.suffix_environment()
            suffixes = morphothec.filter_appends_to(current_type, language)
            suffixes = [suff for suff in suffixes if Morph(suff, morphothec).meets_requirements(env)]
    
            if len(suffixes) > 0:        
                choice = random.choice(suffixes)
                new_morph = Morph(choice, morphothec)
            else:
                Logger.error("No valid suffixes following morph:")
                Logger.error(" - " + last_morph.morph)
                
        else:
            # For words ending in suffixes with restriction, choose from their valid list
            suffixes = last_morph.suffixes()
            choice = random.choice(suffixes)
            new_morph = Morph(choice, morphothec)
            
        if new_morph is not None:
            word.add_suffix(new_morph)

    # Add Preposition
    elif choice == "add_prep_prefix":
        env = word.prefix_environment()
        prepositions = morphothec.filter_prepends_to(current_type, language, { "has-type": "prep" })
        prepositions = [prep for prep in prepositions if Morph(prep, morphothec).meets_requirements(env)]
                
        if len(prepositions) > 0:
            choice = random.choice(prepositions)
            new_morph = Morph(choice, morphothec)
            word.add_prefix(new_morph)
            
    # Add Prefix
    elif choice == "add_prefix":
        env = word.prefix_environment()
        prefixes = morphothec.filter_prepends_to(current_type, language, { "has-type": "prefix" })
        prefixes = [pref for pref in prefixes if Morph(pref, morphothec).meets_requirements(env)]

        if len(prefixes) > 0:
            choice = random.choice(prefixes)
            new_morph = Morph(choice, morphothec)
            word.add_prefix(new_morph)
    
    # Add Modern Prefix
    elif choice == "add_modern_prefix":
        env = word.prefix_environment()
        prefixes = morphothec.filter_prepends_to(current_type, "modern-english", { "has-type": "prefix" })
        prefixes = [pref for pref in prefixes if Morph(pref, morphothec).meets_requirements(env)]

        if len(prefixes) > 0:
            choice = random.choice(prefixes)
            new_morph = Morph(choice, morphothec)
            word.add_prefix(new_morph)

    # Relational
    elif choice == "relational":
        env = word.prefix_environment()
        prepositions = morphothec.filter_prepends_to(current_type, language, { "has-type": "prep" })
        prepositions = [prep for prep in prepositions if Morph(prep, morphothec).meets_requirements(env)]

        if len(prepositions) > 0:
            choice = random.choice(prepositions)
            prep_morph = Morph(choice, morphothec)
            end_morph = Morph(random.choice(relational_suffixes), morphothec )
            word.add_affixes(prep_morph, end_morph)
    
    # Numerical
    elif choice == "numerical":
        env = word.prefix_environment()
        numbers = morphothec.filter_type("number", language)
        numbers = [num for num in numbers if Morph(num, morphothec).meets_requirements(env)]

        if len(numbers) > 0:
            choice = random.choice(numbers)
            num_morph = Morph(choice , morphothec)
            end_morph = Morph(random.choice(numerical_suffixes), morphothec)
            word.add_affixes(num_morph, end_morph)

    # Alternate form
    elif choice == "alternate_form" and alternate_form != None:
        root_morph.morph["key"] += "-adhoc:alt"
        root_morph.morph["gloss"] = "alternate form of '" + form_canon + "'"
        del root_morph.morph["form-raw"]
        del root_morph.morph["form-canon"]
        root_morph.morph["form-final"] = alternate_form
        if "tags" in root_morph.morph:
            root_morph.morph["tags"] += ["fixed-gloss"]
        else:
            root_morph.morph["tags"] = ["fixed-gloss"]

    # Alternate gloss
    elif choice == "alternate_gloss":
        root_morph.morph["key"] += "-adhoc:alt"
        if isinstance(root_morph.morph["gloss-alt"], list):
            root_morph.morph["gloss"] = random.choice(root_morph.morph["gloss-alt"])
        elif isinstance(root_morph.morph["gloss-alt"], str):
            root_morph.morph["gloss"] = root_morph.morph["gloss-alt"]

    # Alternate form and gloss
    elif choice == "alternate_form_and_gloss" and alternate_form != None:
        root_morph.morph["key"] += "-adhoc:alt"
        if isinstance(root_morph.morph["gloss-alt"], list):
            root_morph.morph["gloss"] = random.choice(root_morph.morph["gloss-alt"])
        elif isinstance(root_morph.morph["gloss-alt"], str):
            root_morph.morph["gloss"] = root_morph.morph["gloss-alt"]
        del root_morph.morph["form-raw"]
        del root_morph.morph["form-canon"]
        root_morph.morph["form-final"] = alternate_form

    return True
