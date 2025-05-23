import src.generation.composer as composer
import src.generation.generator as generator
import src.generation.metadata as metadata
import src.utils.validator as validator

from src.morphs.morphothec import Morphothec

# Generating operations

def generate_entry():
    # Generate until we have a valid entry
    while True:
        word = generator.generate_word(Morphothec.active)
        entry = composer.entry(word)
        
        if validator.validate(entry):
            meta = metadata.for_word(word)
            return { "content": entry, "meta": meta }

def entry_for_keys(keys):        
    word = generator.word_for_keys(keys, Morphothec.active)
    
    return composer.entry(word)
