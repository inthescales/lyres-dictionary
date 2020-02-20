import random
from src.morphary import Morphary
from src.models import Morph, Word, check_req
import src.helpers as helpers

def seed_word(word, morphary):
    word.morphs = [get_latin_root(morphary)]

def transform_word(word, morphary):

    if word.get_origin() == "latin":
        return transform_word_latin(word, morphary)
    else:
        print("Bad origin: " + word.get_origin())

def get_latin_root(morphary):

    bag = [
        ("noun", 1),
        ("adj", 1),
        ("verb", 3)
    ]

    type = helpers.choose_bag(bag)
    key = random.choice(morphary.type_morphs[type])
    morph = Morph(key, morphary)
    return morph
        
def transform_word_latin(word, morphary):

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

        
    # Choose --------------------------
    if not override:
        choice = helpers.choose_bag(bag)
    
    # Transformations --------------------------
    
    # Add Suffix
    if choice == "add_suffix":
        choices = morphary.morphs_from[current_type]
        valid_choices = list(choices)

        if last_morph.morph["key"] in choices:
            valid_choices.remove(last_morph.morph["key"])
        for choice in choices:
            if not check_req(morphary.morph_for_key[choice], { "preceding": last_morph.morph } ):
                valid_choices.remove(choice)
                #print("Refused to join " + last_morph.morph["key"] + " - " + choice)

        choice = random.choice(valid_choices)
        new_morph = Morph(choice, morphary)
        word.add_suffix(new_morph)

    # Add Preposition
    elif choice == "add_prep_prefix":
        choices = morphary.type_morphs["prep"]
        valid_choices = list(choices)

        for choice in choices:
            if helpers.has_tag(morphary.morph_for_key[choice], "no-verb"):
                valid_choices.remove(choice)

        choice = random.choice(valid_choices)
        new_morph = Morph(choice, morphary)
        word.add_prefix(new_morph)
            
    # Add Prefix
    elif choice == "add_prefix":
        new_morph = Morph( random.choice(morphary.type_morphs["prefix"]), morphary)
        word.add_prefix(new_morph)

    # Relational
    elif choice == "relational":
        prep_choices = ["in", "ex", "inter", "trans"]
        if last_morph.has_tag("concrete"):
            prep_choices += ["sub", "super", "infra", "supra"]
        prep_morph = Morph(random.choice(prep_choices), morphary)
        end_morph = Morph( random.choice(["ate", "al", "al", "ary", "ify", "ize"]), morphary )
        word.add_affixes(prep_morph, end_morph)
    
    # Numerical
    elif choice == "numerical":
        num_morph = Morph( random.choice(morphary.type_morphs["number"]), morphary)
        end_morph = Morph("al-number", morphary)
        word.add_affixes(num_morph, end_morph)
