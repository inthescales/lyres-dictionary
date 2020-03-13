import random
import src.helpers as helpers
from src.models import Morph, Word, check_req
from src.morphothec import Morphothec

def seed_word(word, morphothec):
    word.morphs = [get_latin_root(morphothec)]

def transform_word(word, morphothec):

    if word.get_origin() == "latin":
        return transform_word_latin(word, morphothec)
    else:
        print("Bad origin: " + word.get_origin())

def get_latin_root(morphothec):

    bag = [
        ("noun", 2),
        ("adj", 1),
        ("verb", 4)
    ]

    type = helpers.choose_bag(bag)
    key = random.choice(morphothec.type_morphs[type])
    morph = Morph(key, morphothec)
    return morph
        
def transform_word_latin(word, morphothec):

    current_type = word.get_type()
    last_morph = word.last_morph()
    first_morph = word.first_morph()
    has_prep = first_morph.get_type() == "prep"
    has_prefix = first_morph.get_type() == "prefix"

    choice = None
    override = False
    bag = [
        ("add_suffix", 100),
    ]

    # Conditions and probabilities --------------------------
    
    if word.size() == 1 and current_type == "verb" and not last_morph.has_tag("no-prep") and not has_prep and not has_prefix:
        if last_morph.has_tag("always-prep"):
            override = True
            choice = "add_prep_prefix"
        else:
            bag.append(("add_prep_prefix", 33))
    
    if word.size() >= 1 and current_type == "verb" and not first_morph.get_type() in ["prep", "prefix"]:
        bag.append(("add_prefix", 10))

    if word.size() == 1 and current_type == "noun":
        bag.append(("relational", 10))

    if word.size() == 1 and current_type == "noun":
        bag.append(("numerical", 5))

    if last_morph.morph["key"] in ["ble", "ify"]:
        bag.append(("negate", 1000000))
        
    # Choose --------------------------
    if not override:
        choice = helpers.choose_bag(bag)
    
    # Transformations --------------------------
    
    # Add Suffix
    if choice == "add_suffix":
        choices = morphothec.morphs_from[current_type]
        valid_choices = choices.copy()

        for choice in choices:
            if not check_req(Morph(choice, morphothec).as_dict(), { "preceding": last_morph.morph } ):
                valid_choices.remove(choice)
            elif Morph(choice, morphothec).has_tag("rare") and random.randint(0, 10) > 0:
                valid_choices.remove(choice)
                
        if last_morph.morph["key"] in valid_choices:
            valid_choices.remove(last_morph.morph["key"])

        choice = random.choice(valid_choices)
        new_morph = Morph(choice, morphothec)
        word.add_suffix(new_morph)

    # Add Preposition
    elif choice == "add_prep_prefix":
        choices = morphothec.filter_type("prep", { "has-tag": "verbal" })
        valid_choices = choices.copy()

        for choice in choices:
            if not check_req(Morph(choice, morphothec).as_dict(), { "following": first_morph.morph } ):
                valid_choices.remove(choice)
                
        if last_morph.morph["key"] in valid_choices:
            valid_choices.remove(last_morph.morph["key"])
                
        choice = random.choice(choices)
        new_morph = Morph(choice, morphothec)
        word.add_prefix(new_morph)
            
    # Add Prefix
    elif choice == "add_prefix":
        new_morph = Morph( random.choice(morphothec.type_morphs["prefix"]), morphothec)
        word.add_prefix(new_morph)

    # Relational
    elif choice == "relational":
        prep_choices = ["in", "ex", "inter", "trans"]
        if last_morph.has_tag("concrete"):
            prep_choices += ["sub", "super", "infra", "supra"]
        prep_morph = Morph(random.choice(prep_choices), morphothec)
        end_morph = Morph( random.choice(["ate", "al", "al", "ary", "ify"]), morphothec )
        word.add_affixes(prep_morph, end_morph)
    
    # Numerical
    elif choice == "numerical":
        num_morph = Morph( random.choice(morphothec.type_morphs["number"]), morphothec)
        end_morph = Morph("al-number", morphothec)
        word.add_affixes(num_morph, end_morph)
        
    elif choice == "negate":
        morph = Morph("in-negative", morphothec)
        word.add_prefix(morph)
