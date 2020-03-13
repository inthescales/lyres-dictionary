import random
import src.helpers as helpers
from src.models import Morph, Word
from src.morphothec import Morphothec
import src.transforms as transforms

def generate_word(morphothec):
    word = Word(morphothec)
    transforms.seed_word(word, morphothec)
    size = random.randint(2,3)
    while word.size() < size:
        transforms.transform_word(word, morphothec)
    return word

def word_for_keys(keys, morphothec):
    word = Word(morphothec)
    word.set_keys(keys)
    return word