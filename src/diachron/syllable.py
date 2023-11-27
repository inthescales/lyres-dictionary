class SyllableData:
    def __init__(self, phonemes, index):
        self.index = get_syllable_index(phonemes, index)
        self.is_open = is_in_open_syllable(phonemes, index)
        self.following_syllable_count = following_syllable_count(phonemes, index)
        self.next_other_syllable_vowel = get_next_other_syllable_vowel(phonemes, index)
        self.next_consonant = get_next_consonant(phonemes, index)
        self.prev_vowel = get_prev_vowel(phonemes, index)

# Returns the syllable that the phoneme at the given index is in, 0-indexed.
# Assumes that the phoneme at the given index is a vowel
def get_syllable_index(phonemes, index):
    count = 0
    state = 0

    for i in range(index, 0, -1):
        if phonemes[i].is_consonant():
            state = 1
        if phonemes[i].is_vowel() and state == 1:
            count += 1

    return count

# Returns true if the phoneme at the given index in the word is in an open syllable.
# Assumes the given index points to a vowel.
def is_in_open_syllable(phonemes, index):
    if not phonemes[index].is_vowel():
        return

    state = 0
    for i in range(index + 1, len(phonemes)):
        phoneme = phonemes[i]

        if phoneme.is_consonant():
            if state == 0:
                state = 1
            else:
                return False
        elif phoneme.is_vowel:
            if state == 1:
                return True

    return state == 1

# Returns the number of syllables after the given index.
def following_syllable_count(phonemes, index):
    polarity = phonemes[index].is_vowel()
    count = 0

    for i in range(index + 1, len(phonemes)):
        new_polarity = phonemes[i].is_vowel()

        if new_polarity != polarity:
            if new_polarity == True:
                count += 1
            polarity = new_polarity

    return count

# Returns the next vowel that is not in the syllable at the given index, if any
# Assumes that the phoneme at the given index is a vowel
def get_next_other_syllable_vowel(phonemes, index):
    state = 0

    for i in range(index, len(phonemes)):
        if phonemes[i].is_consonant():
            state = 1
        elif phonemes[i].is_vowel() and state == 1:
            return phonemes[i]

    return None

# Returns the next consonant phoneme after the given index, if any.
# Assumes that the phoneme at the given index is a vowel.
def get_next_consonant(phonemes, index):
    for i in range(index, len(phonemes)):
        if phonemes[i].is_consonant():
            return phonemes[i]

    return None

# Returns the previous vowel phoneme before the given index, if any.
def get_prev_vowel(phonemes, index):
    for i in range(index, 0):
        if phonemes[i].is_vowel():
            return phonemes[i]

    return None