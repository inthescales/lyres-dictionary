import random
import src.helpers as helpers
from src.models import Morph, Word
from src.morphothec import Morphothec
import src.transforms as transforms

def generate_word(morphothec):
    word = Word(morphothec)
    transforms.seed_word(word, morphothec)
    transform_count = random.randint(1,2)
    maximum_size = 3
    
    for i in range(0, transform_count):
        transforms.transform_word(word, morphothec)
        
        if word.size() >= maximum_size:
            break
            
    return word

def word_for_keys(keys, morphothec):
    word = Word(morphothec)
    word.set_keys(keys)
    return word