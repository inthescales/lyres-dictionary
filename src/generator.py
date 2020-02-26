import random
import src.helpers as helpers
from src.models import Morph, Word
from src.morphary import Morphary
import src.transforms as transforms

def generate_word(morphary):
    word = Word(morphary)
    transforms.seed_word(word, morphary)
    while word.size() < 2:
        transforms.transform_word(word, morphary)
    return word

def word_for_keys(keys, morphary):
    word = Word(morphary)
    word.set_keys(keys)
    return word