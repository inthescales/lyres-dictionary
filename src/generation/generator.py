import src.generation.seeding as seeding
import src.generation.transforms.transforms as transforms

from src.models.word import Word
from src.utils.logging import Logger

def generate_word(morphothec):
    word = Word(morphothec)

    root = seeding.seed_root(morphothec)
    word.morphs = [root]

    transform_count = seeding.transform_count(word)

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
