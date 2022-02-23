import random
import src.helpers as helpers
from src.models.word import Word
from src.morphothec import Morphothec
import src.transforms as transforms

def generate_word(morphothec):
    word = Word(morphothec)
    transforms.seed_word(word, morphothec)

    bag = [
        (1, 5),
        (2, 3)
    ]
    transform_count = helpers.choose_bag(bag)
    maximum_size = 3
    
    transforms_done = 0
    while (transforms_done < transform_count and word.size() < maximum_size) \
        or not word.last_morph().final_ok():
        
        transforms.transform_word(word, morphothec)
        transforms_done += 1
            
    return word

def word_for_keys(keys, morphothec):
    word = Word(morphothec)
    word.set_keys(keys)
    return word