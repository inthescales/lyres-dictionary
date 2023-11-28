from src.diachron.syllable import SyllableData

import sys

class RigState:
    def __init__(self, phonemes, index):
        self.prev = None
        self.next = None
        self.prev_value = None
        self.next_value = None

        if type(index) == int:
            self.current = phonemes[index]

            if index > 0:
                self.prev = phonemes[index-1]
                self.prev_value = self.prev.value

            if index + 1 < len(phonemes):
                self.next = phonemes[index+1]
                self.next_value = self.next.value

            self.preceding = phonemes[:index]
            self.following = phonemes[index:]

            self.syllable_data = SyllableData(phonemes, index)

        elif type(index) == tuple:
            self.capture = phonemes[index[0]:index[1]]
            self.joined = "".join([x.value for x in self.capture])
            if len(self.capture) == 1:
                self.current = phonemes[index[0]]

            if index[0] > 0:
                self.prev = phonemes[index[0]-1]
                self.prev_value = self.prev.value

            if index[1] < len(phonemes):
                self.next = phonemes[index[1]]
                self.next_value = self.next.value

            self.preceding = phonemes[:index[0]]
            self.following = phonemes[index[1]:]

            self.syllable_data = SyllableData(phonemes, index[0])

        self.is_first = (self.prev == None)
        self.is_last = (self.next == None)



    # Returns true if the phoneme at the given index in the word is in an open syllable.
    # Assumes the given index points to a vowel.
    def is_in_open_syllable(phonemes, index):
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

        return False

class Rig:
    def __init__(self, phonemes):
        self.phonemes = phonemes

    def run_change(self, change, name=None, verbose=False, separator="\n"):
        new_phonemes = []
        for i in range(0, len(self.phonemes)):
            state = RigState(self.phonemes, i)
            added_phonemes = change(state)
            if added_phonemes:
                new_phonemes.append(added_phonemes)

        if name and verbose:
            print(name + ": " + "".join([p.value for p in new_phonemes]) + separator)

        self.phonemes = new_phonemes

    def run_capture(self, change, capture_size, name=None, verbose=False, separator="\n"):
        if capture_size > len(self.phonemes):
            return

        new_phonemes = []
        treated = 0

        for i in range(0, len(self.phonemes) - capture_size + 1):
            if i < treated:
                continue

            state = RigState(self.phonemes, (i, i + capture_size))
            added_phonemes = change(state)
            if added_phonemes != None:
                new_phonemes += added_phonemes
                treated += capture_size
            else:
                new_phonemes.append(self.phonemes[i])
                treated += 1

        if treated < len(self.phonemes):
            new_phonemes += self.phonemes[treated:]

        if name and verbose and new_phonemes != self.phonemes:
            print("".join([p.value for p in new_phonemes]) + " — " + name + separator)

        self.phonemes = new_phonemes



