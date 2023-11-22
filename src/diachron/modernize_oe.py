import random

from src.diachron.phoneme import Phoneme
from src.diachron.changerig import RigState, Rig
import src.diachron.syllable as syllable

def modernize(oe_phonemes):
    phonemes = oe_phonemes

    rig = Rig(phonemes)
    form = ""

    # Vː → V[-long] / _C{ː,C} ! _st{#,V} or when preceding a cluster which had
    # triggered a vowel to become long in Old English
    def pre_cluster_shortening(state):
        if state.current.is_vowel() and state.current.is_long() and state.next and state.next.is_consonant():
            if state.next.is_geminate() or len(state.following) > 1 and state.following[1].is_consonant():
                # !
                if len(state.following) >= 2:
                    next_two_joined = "".join([x.value for x in state.following[:2]])
                    if next_two_joined == "st" \
                        and (len(state.following) == 2 or state.following[2].is_vowel()):
                        return None

                    lengthening_clusters = ["ld", "mb", "nd", "ng", "rd", "rl", "rn", "rs"] # rs+vowel?
                    if next_two_joined in lengthening_clusters:
                        return None

                return [state.current.get_shortened()]

    # Reduced double consonants to a single consonant
    def reduction_of_double_consonants(state):
        return [state.current.get_geminate_reduced()]

    # Reduce unstressed vowels to e
    def reduction_of_unstressed_vowels(state):
        if state.current.is_vowel() and not state.current.stressed:
            return [Phoneme("ə", template=state.current)]
        else:
            return None

    # Open syllable lengthening
    def open_syllable_lengthening(state):
        # print("(phoneme: " + str(state.current.value) + ", open:" + str(state.syllable_data.is_open) + ")<br>")
        if state.current.is_vowel() and state.syllable_data.is_open and state.syllable_data.following_syllable_count == 1:
            # print("Lengthening " + str(state.current.value))
            if state.current.value == "i":
                return [Phoneme("iː", state.current.stressed)]
            elif state.current.value == "e":
                return [Phoneme("eː", state.current.stressed)]
            elif state.current.value == "o":
                return [Phoneme("oː", state.current.stressed)]
            elif state.current.value == "u" and occ():
                return [Phoneme("uː", state.current.stressed)]
            else:
                return [state.current.get_lengthened()]
        else:
            return None

    # m → n / _# when unstressed
    def final_unstressed_m_to_n(state):
        if state.current.value in ["m"] and state.next == None \
            and not (state.syllable_data.prev_vowel and not state.syllable_data.prev_vowel.stressed):
            return []

    # Drop final n in inflectional ending
    def drop_inflecional_n(state):
        if state.current.value == "n" and state.next == None and state.current.inflectional:
            return []

    # hn {wl,hl} hr → w l r 
    def drop_initial_h(state):
        if len(state.joined) == 2 and state.joined[0] == "x" and state.joined[1] in ["n", "l", "r"]:
            return [Phoneme(state.joined[1], template=state.capture[-1])]
        elif state.joined == "wl":
            return [Phoneme("l", template=state.capture[-1])]

    # ɣ → ɡ / #_ 
    def initial_g(state):
        if state.current.value == "ɣ" and state.syllable_data.index == 0:
            return [Phoneme("g", template=state.current)]

    # ɣ → w / C_V 
    def g_to_w(state):
        if state.current.value == "ɣ" and state.prev.is_consonant() and state.next.is_vowel():
            return [Phoneme("w", template=state.current)]

    # ə → ∅ / _# 
    def loss_of_final_unstressed_vowel(state):
        if state.current.value == "ə" and state.next == None:
            return []

    print("".join([x.value for x in rig.phonemes]) + "<br>")
    rig.run_capture(open_syllable_lengthening, 1)
    print("".join([x.value for x in rig.phonemes]) + "<br>")
    rig.run_capture(pre_cluster_shortening, 1)
    print("".join([x.value for x in rig.phonemes]) + "<br>")
    rig.run_capture(reduction_of_double_consonants, 1)
    print("".join([x.value for x in rig.phonemes]) + "<br>")
    rig.run_capture(reduction_of_unstressed_vowels, 1)
    print("".join([x.value for x in rig.phonemes]) + "<br>")
    rig.run_capture(final_unstressed_m_to_n, 1)
    print("".join([x.value for x in rig.phonemes]) + "<br>")
    rig.run_capture(drop_inflecional_n, 1)
    print("".join([x.value for x in rig.phonemes]) + "<br>")
    rig.run_capture(drop_initial_h, 2)
    print("".join([x.value for x in rig.phonemes]) + "<br>")
    rig.run_capture(initial_g, 1)
    print("".join([x.value for x in rig.phonemes]) + "<br>")
    rig.run_capture(g_to_w, 1)
    print("".join([x.value for x in rig.phonemes]) + "<br>")
    rig.run_capture(loss_of_final_unstressed_vowel, 1)
    print("".join([x.value for x in rig.phonemes]) + "<br>")

    form = the_big_chart(rig.phonemes)
    return form

def often():
    return False

def occ():
    return False

def the_big_chart(phonemes):
    result = []
    insert_lengthening_e = False
    skip_next = 0

    for i in range(0, len(phonemes)):
        if skip_next > 0:
            skip_next -= 1
            continue

        phone = phonemes[i]
        prev2 = None
        prev = None
        next1 = None
        next2 = None
        next3 = None
        if i > 1:
            prev2 = phonemes[i - 2]
        if i > 0:
            prev = phonemes[i - 1]
        if i < len(phonemes) - 1:
            next1 = phonemes[i + 1]
        if i < len(phonemes) - 2:
            next2 = phonemes[i + 2]
        if i < len(phonemes) - 3:
            next3 = phonemes[i + 3]

        # Diphthongs
        if phone.is_vowel() and next1 and next1.value in ["g", "j", "w", "x"]:
            if (phone.value + next1.value in ["æj", "æːj", "ej"]) \
                or (phone.value + next1.value == "eːj" and not next2):

                if not next2:
                    result += "ay"
                else:
                    result += "ai"
            elif (phone.value + next1.value == "eːj" and next2 and next2.is_vowel()) \
                or (phone.value + next1.value in ["ij", "iːj", "yj", "yːj"]):

                if prev2 and prev2 and prev2.is_consonant() and prev.is_consonant():
                    result += "y"
                else:
                    result += random.choice(["ie", "uy"])
            elif (phone.value + next1.value in ["æw", "aw"]) \
                or (phone.value + next1.value == "ag" and next2 and next2.is_vowel()):

                result += "aw"

            elif phone.value + next1.value in ["æːw", "eːaw", "ew", "eow", "eːw", "eːow", "iw", "iːw", "yw", "yːw"]:
                if next1:
                    result += random.choice(["ew", "ue", "u"])
                else:
                    result += random.choice(["ew", "ue"])

            elif phone.value + next1.value in ["aːw", "ow", "oːw"] \
                 or (phone.value + next1.value in ["aːg", "og", "oːg"] and next2 and next2.is_vowel):

                result += "ow"

            elif phone.value + next1.value in ["ug", "uːg"]: # Modified chart here

                if next1.is_vowel():
                    skip_next += 1

                if next2 and next2.value == "t" or next2.is_vowel() and next3 and next3.value == "t":
                    result += "ough"
                else:
                    result += random.choose("ow", "ough")

            elif phone.value + next1.value in ["æx", "ax"] \
                or (phone.value + next1.value == "ag" and not next2):

                result += "augh"

            elif phone.value + next1.value == "ex":
                result += "ai"

            elif phone.value + next1.value in ["eːx", "ix", "iːx", "yx", "yːx"]:
                result += "igh"

            elif phone.value + next1.value in ["aːx", "ox"] \
                or (phone.value + next1.value in ["aː", "og"] and not next2):
                result += "ough"

            elif phone.value + next1.value in ["aːx", "ox", "oːx"] and next2 and next2.is_consonant:
                result += random.choice(["ough", "augh"])

            elif phone.value + next1.value in ["ux", "uːx"] \
                or (phone.value + next1.value in ["oːx", "oːg", "ug", "uːg"] and not next2):
                result += "ough"
            else:
                # No match found
                continue

            skip_next += 1
            continue

        # Monophthongs
        elif phone.is_vowel():
            if (phone.value in ["ɑ", "æ", "ea"] or (phone.value == "ɑː" and next1 and next1.is_geminate())) \
                or (often() and phone.value in ["æː", "eːa"] and next1 and next1.is_geminate()) \
                or (occ() and phone.value == "eː" and next1 and next1.value.is_geminate()): # WS ǣ+CC
                    
                    if not syllable.is_in_open_syllable(phonemes, i):
                        result += "a"
                    else:
                        result += "a"
                        insert_lengthening_e = True

            elif (phone.value in ["e", "eo"] or (phone.value in ["eː", "eːo"] and next1 and next1.is_geminate())) \
                or (often() and phone.value in ["æː", "eːa"] and next1 and next1.is_geminate()) \
                or (occ() and phone.value == "y") \
                or (occ() and phone.value in ["æː", "eːa"] and next1 and next1.value.is_geminate()): # WS ǣ+CC
                    if next1 and next1.value == "r":
                        result += random.choice(["ar", "er"])
                        skip_next += 1

                    if not syllable.is_in_open_syllable(phonemes, i):
                        result += "e"
                    else:
                        if random.randint(0, 1) == 0:
                            result += "ea"
                        else:
                            result += "e"
                            insert_lengthening_e = True

            elif (phone.value in ["i", "y"] or (phone.value in ["iː", "yː"] and next1 and next1.is_geminate())) \
                or (occ() and phone.value in ["eːo", "eː"] and next1 and next1.value == "c") \
                or (occ() and phone.value in ["iː", "yː"] and next1 and next1.is_consonant() and next2 and next2.is_vowel()):

                    if not syllable.is_in_open_syllable(phonemes, i):
                        result += "i"
                    elif occ():
                        result += "ee"
            elif (phone.value == "o" or (phone.value == "oː" and next1 and next1.is_geminate())):
                if not syllable.is_in_open_syllable(phonemes, i):
                    result += "o"
                else:
                    if random.randint(0, 1) == 0:
                        result += "oa"
                    else:
                        result += "o"
                        insert_lengthening_e = True
            elif (phone.value == "u" or (phone.value == "uː" and next1 and next1.is_geminate())) \
                or (occ() and phone.value == "y"):
                    if occ() and syllable.is_in_open_syllable(phonemes, i):
                        result += "oo"
                    else:
                        result += "u"

                    # TODO: Add exception to catch 'lufian' -> 'love'?
            elif (prev and prev.value == "w" and phone.value in ["e", "eo", "o", "y"] and next1 and next1.value == "r"):
                result += "o"
            elif phone.value == "ɑː" \
                or (phone.value == "ɑ" and next1 and next2 and next1.value + next2.value in ["ld", "mb"]):
                if random.randint(0, 1) == 0:
                    result += "oa"
                else:
                    result += "o"
                    insert_lengthening_e = True
            elif phone.value in ["æː", "eːa"]:
                if random.randint(0, 1) == 0:
                    result += "ea"
                else:
                    result += "e"
                    insert_lengthening_e = True
            elif phone.value in ["eː", "eːo"] \
                or (phone.value == "e" and next1 and next2 and next1.value + next2.value == "ld"):

                if next1 and next2 and next1.value + next2.value in ["nd", "ld"]:
                    result += "ie"
                elif often() and next1 and next1.value == "r":
                    if random.randint(0, 1) == 0:
                        result += "ear"
                    else:
                        result += "er"
                        insert_lengthening_e = True
                elif occ() and next1 and next1.value == "r":
                    result += "eer"
                else:
                    result += "ee"

            elif phone.value in ["iː", "yː"] \
                or (often() and phone.value == "i" and next1 and next2 and next1.value + next2.value in ["ld", "mb", "nd"]) \
                or (often() and phone.value == "y" and next1 and next2 and next1.value + next2.value in ["ld", "mb", "nd"]):

                result += "i"

                if next1 and next1.is_consonant() and not next2:
                    insert_lengthening_e = True

            elif phone.value == "oː" \
                or (occ() and phone.value == "eːo"):

                result += "oo"

            elif phone.value == "uː" \
                or (often() and phone.value == "u" and next1 and next2 and next1.value + next2.wordvalue == "nd"):

                result += "ou"

            elif phone.value == "ə":
                result += "e"

        # Consonants
        else:

            if phone.value == "f":
                if (prev and (prev.is_vowel() or prev.is_voiced())) \
                    and (next1 and (next1.is_vowel() or next1.is_voiced())):
                    result += "v"
                else:
                    if next1 != None:
                        result += "f"
                    else:
                        result += "ff"
            elif phone.value == "l":
                if next1 != None or (prev and prev.is_vowel() and prev.is_long()):
                    result += "l"
                else:
                    result += "ll"
            elif phone.value == "s":
                if next1 != None:
                    result += "s"
                else:
                    result += "ss"
            elif phone.value == "θ":
                result += "th"
            elif phone.value in ["x", "xx"]:
                if prev == None:
                    result += "h"
                else:
                    result += "gh"
            elif phone.value == "k":
                if next1 != None:
                    result += "k"
                else:
                    result += "ck"
            elif phone.value == "tʃ":
                result += "ch"
            elif phone.value == "dʒ":
                if next1 != None:
                    result += "j"
                else:
                    result += "dge"
            else:
                result += phone.value

            if phone.is_consonant and insert_lengthening_e and (not next1 or not next1.is_vowel()):
                result += "e"
                insert_lengthening_e = False


    return "".join(result)