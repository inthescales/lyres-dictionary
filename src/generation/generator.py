import random

import src.generation.transforms.transforms as transforms
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
                (0, 1) ,
                (1, 5)
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
    max_failures = 3
    
    successes = 0
    failures = 0
    while (
            successes < transform_count \
            and failures < max_failures \
            and word.size() < maximum_size \
            and not word.last_morph().final()
        ) \
        or not word.last_morph().final_ok():

        result = transforms.transform_word(word, morphothec, transform_count == 1)

        if result.success:
            if not result.free:
                successes += 1
        else:
            Logger.trace("failed to add transform to word with keys: " + str([x.get_key() for x in word.morphs]))
            failures += 1
    
    Logger.trace("generated morph: " + str(word.get_keys()))
    return word

def word_for_keys(keys, morphothec):
    word = Word(morphothec)
    word.set_keys(keys)
    return word
