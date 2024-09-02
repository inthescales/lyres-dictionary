import random

import src.generation.transforms as transforms
import src.utils.helpers as helpers

from src.models.word import Word
from src.morphs.morphothec import Morphothec
from src.utils.logging import Logger

def generate_word(morphothec):
    word = Word(morphothec)
    transforms.seed_word(word, morphothec)

    bag = [(1, 1)]
    if word.get_origin() == "old-english":
        if word.root_morph().has_tag("speculative"):
            bag = [
                (0, 3) ,
                (1, 1)
            ]
        elif word.root_morph().has_tag("obscure"):
            bag = [
                (0, 2) ,
                (1, 2)
            ]
        else:
            bag = [
                (1, 1)
            ]
    else:
        bag = [
            (1, 5),
            (2, 3)
        ]
    transform_count = helpers.choose_bag(bag)
    maximum_size = 3
    
    transforms_done = 0
    while (
            transforms_done < transform_count \
            and word.size() < maximum_size \
            and not word.last_morph().final()
        ) \
        or not word.last_morph().final_ok():
        success = transforms.transform_word(word, morphothec, transform_count == 1)
        # HACK: In OE I used the convention that returning False should give you another try,
        # but that isn't the case in Latin and Greek where you can legitimately have no
        # valid transforms, and need to exit.
        #
        # TODO: come up with a better convention for 'free' transforms
        if success or word.get_origin() != "old-english":
            transforms_done += 1
    
    Logger.trace("generated morph: " + str(word.get_keys()))
    return word

def word_for_keys(keys, morphothec):
    word = Word(morphothec)
    word.set_keys(keys)
    return word