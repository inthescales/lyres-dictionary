import random

import src.helpers as helpers
import src.models

from src.models.word import Word
from src.models.morph import Morph
from src.morphothec import Morphothec

def seed_word(word, morphothec):
    bag = [
        ("latin", morphothec.root_count_for_language("latin")),
        ("greek", morphothec.root_count_for_language("greek"))
    ]
    choice = helpers.choose_bag(bag)
    if choice == "latin":
        word.morphs = [get_latin_root(morphothec)]
    if choice == "greek":
        word.morphs = [get_greek_root(morphothec)]

def transform_word(word, morphothec):

    if word.get_origin() == "latin":
        return transform_word_latin(word, morphothec)
    elif word.get_origin() == "greek":
        return transform_word_greek(word, morphothec)
    else:
        print("Bad origin: " + word.get_origin())

def get_latin_root(morphothec):

    bag = [
        ("noun", 3),
        ("adj", 3),
        ("verb", 5)
    ]

    type_ = helpers.choose_bag(bag)
    key = random.choice(morphothec.filter_type(type_))
    morph = Morph(key, morphothec)
    return morph

def get_greek_root(morphothec):

    bag = [
        ("noun", 3),
        ("adj", 1),
        ("verb", 3)
    ]

    type_ = helpers.choose_bag(bag)
    key = random.choice(morphothec.filter_type(type_, language="greek"))
    morph = Morph(key, morphothec)
    return morph
        
def transform_word_latin(word, morphothec):

    language = "latin"
    current_type = word.get_type()
    last_morph = word.last_morph()
    first_morph = word.first_morph()
    has_prep = first_morph.get_type() == "prep"
    has_prefix = first_morph.get_type() == "prefix"
    
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
            bag.append(("add_prep_prefix", 33))
    
    if word.size() >= 1 and current_type == "verb" and not first_morph.get_type() in ["prep", "prefix"]:
        bag.append(("add_prefix", 10))

    if word.size() == 1 and current_type == "noun" and (last_morph.has_tag("concrete") or last_morph.has_tag("bounded")):
        bag.append(("relational", 10))

    if word.size() == 1 and current_type == "noun" and not last_morph.has_tag("singleton"):
        bag.append(("numerical", 5))
        
    # If there is no override, choose, or return if no choices ------
    if not override: 
        if len(bag) > 0:
            choice = helpers.choose_bag(bag)
        else:
            return
    
    # Transformations --------------------------

    # Add Suffix
    if choice == "add_suffix":
        
        new_morph = None
        
        if last_morph.is_root() or last_morph.suffixes() is None:
            # For unsuffixed words or ones with unlimited suffixing, choose based on type
            choices = morphothec.filter_appends_to(current_type, language)
            valid_choices = choices.copy()
            env = word.suffix_environment()
            
            for choice in choices:
                choice_morph = Morph(choice, morphothec)
                if not choice_morph.meets_requirements(env):
                    valid_choices.remove(choice)
                elif choice_morph.has_tag("rare") and random.randint(0, 10) > 0:
                    valid_choices.remove(choice)
                
            if last_morph.morph["key"] in valid_choices:
                valid_choices.remove(last_morph.morph["key"])
    
            if len(valid_choices) == 0:
                print("Error: No valid suffixes following morph:")
                print(last_morph.morph)
            
            choice = random.choice(valid_choices)
            new_morph = Morph(choice, morphothec)
                
        else:
            # For words ending in suffixes with restriction, choose from their valid list
            valid_choices = last_morph.suffixes()
            choice = random.choice(valid_choices)
            new_morph = Morph(choice, morphothec)
            
        if new_morph is not None:
            word.add_suffix(new_morph)

    # Add Preposition
    elif choice == "add_prep_prefix":
        choices = morphothec.filter_type("prep", language, { "has-tag": "verbal" })
        valid_choices = choices.copy()
        env = word.prefix_environment()

        for choice in choices:
            if not Morph(choice, morphothec).meets_requirements(env):
                valid_choices.remove(choice)
                
        if last_morph.morph["key"] in valid_choices:
            valid_choices.remove(last_morph.morph["key"])
                
        if len(valid_choices) > 0:
            choice = random.choice(valid_choices)
            new_morph = Morph(choice, morphothec)
            word.add_prefix(new_morph)
            
    # Add Prefix
    elif choice == "add_prefix":
        new_morph = Morph( random.choice(morphothec.filter_type("prefix", language)), morphothec)
        word.add_prefix(new_morph)

    # Relational
    elif choice == "relational":
        prep_choices = ["in-", "ex-", "inter-", "trans-"]
        if last_morph.has_tag("concrete"):
            prep_choices += ["circum-", "sub-", "super-", "infra-", "supra-"]
        prep_morph = Morph(random.choice(prep_choices), morphothec)
        end_morph = Morph( random.choice(["-ate", "-al", "-al", "-ary", "-ify"]), morphothec )
        word.add_affixes(prep_morph, end_morph)
    
    # Numerical
    elif choice == "numerical":
        num_morph = Morph( random.choice(morphothec.filter_type("number", language)), morphothec)
        end_morph = Morph("-al-number", morphothec)
        word.add_affixes(num_morph, end_morph)
        
def transform_word_greek(word, morphothec):

    language = "greek"
    current_type = word.get_type()
    last_morph = word.last_morph()
    first_morph = word.first_morph()
    has_prep = first_morph.get_type() == "prep"
    has_prefix = first_morph.get_type() == "prefix"
    
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

    if word.size() == 1 and first_morph.get_type() == "verb" and not first_morph.has_tag("no-prep") and not has_prep and not has_prefix:
        if last_morph.has_tag("always-prep"):
            override = True
            choice = "add_prep_prefix"
        else:
            if first_morph.has_tag("motion"):
                bag.append(("add_prep_prefix", 33))
            else:
                bag.append(("add_prep_prefix", 10))
    
    if word.size() >= 1 and current_type == "verb" and not first_morph.get_type() in ["prep", "prefix"]:
        bag.append(("add_prefix", 10))

    if word.size() == 1 and current_type == "noun":
        if (last_morph.has_tag("concrete") or last_morph.has_tag("bounded")):
            bag.append(("relational", 10))
        else:
            bag.append(("relational", 8))

    if word.size() == 1 and current_type == "noun" and not last_morph.has_tag("singleton"):
        bag.append(("numerical", 5))
    
    # If there is no override, choose, or return if no choices ------
    if not override: 
        if len(bag) > 0:
            choice = helpers.choose_bag(bag)
        else:
            return
    
    # Transformations --------------------------

    # Add Suffix
    if choice == "add_suffix":
        
        new_morph = None
        
        if last_morph.is_root() or last_morph.suffixes() is None:
            # For unsuffixed words or ones with unlimited suffixing, choose based on type
            choices = morphothec.filter_appends_to(current_type, language)
            valid_choices = choices.copy()
            env = word.suffix_environment()

            for choice in choices:
                if not Morph(choice, morphothec).meets_requirements(env):
                    valid_choices.remove(choice)
                elif Morph(choice, morphothec).has_tag("rare") and random.randint(0, 10) > 0:
                    valid_choices.remove(choice)
                
            if last_morph.morph["key"] in valid_choices:
                valid_choices.remove(last_morph.morph["key"])
            
            choice = random.choice(valid_choices)
            new_morph = Morph(choice, morphothec)
                
        else:
            # For words ending in suffixes with restriction, choose from their valid list
            valid_choices = last_morph.suffixes()
            choice = random.choice(valid_choices)
            new_morph = Morph(choice, morphothec)
            
        if new_morph is not None:
            word.add_suffix(new_morph)
        
    # Add Preposition
    elif choice == "add_prep_prefix":
        choices = morphothec.filter_type("prep", language, { "has-tag": "verbal" })
        valid_choices = choices.copy()
        env = word.prefix_environment()

        for choice in choices:
            if not Morph(choice, morphothec).meets_requirements(env):
                valid_choices.remove(choice)
                
        if len(valid_choices) > 0:
            choice = random.choice(valid_choices)
            new_morph = Morph(choice, morphothec)
            word.add_prefix(new_morph)

    # Add Prefix
    elif choice == "add_prefix":
        choices = morphothec.filter_type("prefix", language)
        valid_choices = choices.copy()
        env = word.prefix_environment()

        for choice in choices:
            if not Morph(choice, morphothec).meets_requirements(env):
                valid_choices.remove(choice)

        if len(valid_choices) > 0:
            choice = random.choice(valid_choices)
            new_morph = Morph(choice, morphothec)
            word.add_prefix(new_morph)

    # Relational
    elif choice == "relational":
        prep_choices = ["anti-", "syn-", "meta-"]
        if last_morph.has_tag("concrete") or last_morph.has_tag("bounded"):
            prep_choices += ["dia-", "en-"]
        if last_morph.has_tag("concrete"):
            prep_choices += ["epi-", "hyper-", "hypo-", "peri-"]
        prep_morph = Morph(random.choice(prep_choices), morphothec)
        end_morph = Morph( random.choice(["-ic", "-y-relative", "-ize"]), morphothec )
        word.add_affixes(prep_morph, end_morph)

    # Numerical
    elif choice == "numerical":
        num_morph = Morph( random.choice(morphothec.filter_type("number", language)), morphothec)
        end_morph = Morph(random.choice(["-ic-number", "-y-number"]), morphothec)
        word.add_affixes(num_morph, end_morph)
