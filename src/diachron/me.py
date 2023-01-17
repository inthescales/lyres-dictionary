from src.diachron.phoneme import Phoneme

def phonemes_from_oe(oe_phonemes):
    phonemes = oe_phonemes

    # Skipping homorganic lengthening

    # Stressed vowel changes
    new_phonemes = []
    for phoneme in phonemes:
        if phoneme.value == "æɑ":
            new_phonemes.append(Phoneme("æ", phoneme.stressed))
        elif phoneme.value == "æːɑ":
            new_phonemes.append(Phoneme("æː", phoneme.stressed))
        elif phoneme.value == "eo":
            new_phonemes.append(Phoneme("e", phoneme.stressed))
        elif phoneme.value == "eːo":
            new_phonemes.append(Phoneme("eː", phoneme.stressed))
        elif phoneme.value == "y":
            new_phonemes.append(Phoneme("i", phoneme.stressed))
        elif phoneme.value == "yː":
            new_phonemes.append(Phoneme("iː", phoneme.stressed))
        else:
            new_phonemes.append(phoneme)
    phonemes = new_phonemes

    # Reduction and loss of unstressed vowels
    new_phonemes = []
    for phoneme in phonemes:
        if phoneme.is_vowel() and not phoneme.stressed:
            new_phonemes.append(Phoneme("ə", False))
        else:
            new_phonemes.append(phoneme)
    phonemes = new_phonemes

    return phonemes
