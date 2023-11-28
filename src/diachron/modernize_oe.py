import random

from src.diachron.phoneme import Phoneme
from src.diachron.changerig import RigState, Rig
import src.diachron.syllable as syllable

def often():
    return True

def even():
    return True

def occ():
    return False

def me_phonemes(oe_phonemes):
    phonemes = oe_phonemes

    rig = Rig(phonemes)
    form = ""

    # ɣ → ɡ / #_ 
    def initial_g(state):
        if state.current.value == "ɣ" and state.syllable_data.index == 0:
            return [Phoneme("g", template=state.current)]

    def homorganic_lengthening(state):
        if state.capture[0].is_vowel() \
            and (state.joined[1:3] in ["ld", "mb", "nd", "rd"] or state.joined[1:3] in ["ng", "rl", "rn"]) \
            and not (len(state.following) > 0 and state.following[0].is_consonant()):
            # and not state.syllable_data.following_syllable_count > 1:
            
            return [state.capture[0].get_lengthened(), state.capture[1], state.capture[2]]

    def stressed_vowel_changess(state):
        if state.current.stressed:
            if state.current.value in ["æ", "ea", "a"]:
                return [Phoneme("a", template=state.current)]
            elif state.current.value in ["æː", "eːa"]:
                return [Phoneme("ɛː", template=state.current)]
            elif state.current.value == "aː":
                return [Phoneme("ɔː", template=state.current)]
            elif state.current.value == "eo":
                return [Phoneme("e", template=state.current)]
            elif state.current.value == "eːo":
                return [Phoneme("eː", template=state.current)]
            elif state.current.value == "y":
                if often():
                    # Anglian dialect
                    return [Phoneme("i", template=state.current)]
                elif often():
                    # Kentish dialect
                    return [Phoneme("e", template=state.current)]
                else:
                    # West Saxon dialect
                    return [Phoneme("u", template=state.current)]
            elif state.current.value == "yː":
                if often():
                    # Anglian dialect
                    return [Phoneme("iː", template=state.current)]
                elif often():
                    # Kentish dialect
                    return [Phoneme("eː", template=state.current)]
                else:
                    # West Saxon dialect
                    return [Phoneme("uː", template=state.current)]

    def pre_cluster_shortening(state):
        if state.current.is_vowel() and state.current.is_long() \
            and state.next and state.next.is_consonant() \
            and (state.next.is_geminate() or len(state.following) > 1 and state.following[1].is_consonant()):
                if state.next.is_geminate():
                    return [state.current.get_shortened()]
                else:
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

    def vocalization_of_post_vocalic_g(state):
        if state.current.value == "ɣ" and state.prev.is_vowel() and state.next.is_vowel():
            return [Phoneme("w", template=state.current)]

    def diphthong_formation_2(state):
        vowel_after = state.next and state.next.is_vowel()
        word_end = state.next == None

        if state.joined in ["aj", "aːj", "ɛj"] \
            or (state.joined == "eːj" and word_end):
            return [Phoneme("ai", template=state.capture[0])]
        elif (state.capture[0].value == "eːj" and vowel_after) \
            or state.joined in ["ij", "iːj", "yj", "yːj"]:
            return [Phoneme("iː", template=state.capture[0])]
        elif state.joined == "au":
            return [Phoneme("au", template=state.capture[0])]
        elif state.joined in ["aːu", "eːau", "eu", "eou"]:
            return [Phoneme("ɛu", template=state.capture[0])]
        elif state.joined in ["eːu", "eːou", "iu", "iːu", "yu", "yːu"]:
            return [Phoneme("iu", template=state.capture[0])]
        elif state.joined in ["aːu", "ou", "oːu"]:
            return [Phoneme("ɔu", template=state.capture[0])]

    def breaking(state):
        word_end = state.next == None

        if state.joined == "ax" \
            or (state.joined == "ag" and word_end):
            return [Phoneme("au", template=state.capture[0]), Phoneme("x", template=state.capture[1])]
        elif state.joined == "ex":
            return [Phoneme("ɛi", template=state.capture[0]), Phoneme("x", template=state.capture[1])]
        elif state.joined in ["eːx", "ix", "iːx", "yx", "yːx"]:
            return [Phoneme("iː", template=state.capture[0]), Phoneme("x", template=state.capture[1])]
        elif state.joined in ["aːx", "ox"] \
            or (state.joined in ["aːg", "og"] and word_end):
            return [Phoneme("ɔu", template=state.capture[0]), Phoneme("x", template=state.capture[1])]
        elif state.joined in ["ux", "uːx"] \
            or (state.joined in ["oːx", "oːg", "ug", "uːg"] and word_end):
            return [Phoneme("ɔu", template=state.capture[0]), Phoneme("x", template=state.capture[1])]

    # ɣ → w / C_V 
    def g_to_w(state):
        if state.current.value == "ɣ" and state.prev.is_consonant() and state.next.is_vowel():
            return [Phoneme("w", template=state.current)]

    # Open syllable lengthening
    def open_syllable_lengthening(state):
        if state.current.is_vowel() and not state.current.is_diphthong() and state.syllable_data.is_open and state.syllable_data.following_syllable_count == 1:
            if state.current.value in ["i", "y"]:
                return [Phoneme("eː", state.current.stressed)]
            elif state.current.value in ["e", "eo"]:
                return [Phoneme("ɛː", state.current.stressed)]
            elif state.current.value == "o":
                return [Phoneme("ɔː", state.current.stressed)]
            elif state.current.value == "u" and occ():
                return [Phoneme("oː", state.current.stressed)]
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

    # ə → ∅ / _# 
    def loss_of_final_unstressed_vowel(state):
        if state.current.value == "ə" and state.next == None:
            return []

    verbose = True
    separator = "<br>"
    if verbose:
        print("".join(p.value for p in rig.phonemes) + separator)

    rig.run_capture(initial_g, 1, "Harden initial g", verbose, separator)
    rig.run_capture(homorganic_lengthening, 3, "Homorganic lengthening", verbose, separator)
    rig.run_capture(stressed_vowel_changess, 1, "Stressed vowel changes", verbose, separator)
    rig.run_capture(reduction_of_unstressed_vowels, 1, "Reduction of unstressed vowels", verbose, separator)
    rig.run_capture(final_unstressed_m_to_n, 1, "Final unstressed m to n", verbose, separator)
    rig.run_capture(drop_inflecional_n, 1, "Drop inflectional n", verbose, separator)
    rig.run_capture(vocalization_of_post_vocalic_g, 1, "Vocalization of post-vocalic ɣ", verbose, separator)
    rig.run_capture(diphthong_formation_2, 2, "Diphthong formation", verbose, separator)
    # rig.run_capture(g_to_w, 1, "G to w", verbose, separator)
    rig.run_capture(breaking, 2, "Breaking", verbose, separator)
    rig.run_capture(open_syllable_lengthening, 1, "Open syllable lengthening", verbose, separator)
    # Trisyllabic laxing (not sure if relevant to spelling)
    rig.run_capture(pre_cluster_shortening, 1, "Pre-cluster shortening", verbose, separator)
    rig.run_capture(reduction_of_double_consonants, 1, "Reduction of double consonants", verbose, separator)
    rig.run_capture(drop_initial_h, 2, "Drop initial h", verbose, separator)
    rig.run_capture(loss_of_final_unstressed_vowel, 1, "Loss of final unstressed vowel", verbose, separator)
    # rig.run_capture(vowel_shifts, 1, "Vowel shifts", verbose, separator)

    return rig.phonemes

    # def vowel_shifts(state):
    #     def value(values):
    #         return state.current.value in values

    #     def vcc(vowels):
    #         if state.current.value in vowels \
    #             and state.next and state.next.is_consonant() \
    #             and len(state.following) > 1 and state.following[1].is_consonant():
    #             return True

    #         return False

    #     def vcv(vowels):
    #         if state.current.value in vowels \
    #             and state.next and state.next.is_consonant() \
    #             and len(state.following) > 1 and state.following[1].is_vowel():
    #             return True

    #         return False


    #     open_syllable = state.current.is_vowel() and state.syllable_data.is_open and state.syllable_data.following_syllable_count == 1
    #     if open_syllable:
    #         # Address only long vowels unaltered by open-syllable lengthening
    #         if state.current.value == "aː":
    #             return [Phoneme("ɔː", template=state.current)]
    #         elif state.current.value in ["eː", "eːo"]:
    #             return [Phoneme("ɛː", template=state.current)]
    #         elif state.current.value in ["æː", "eːa"]:
    #             return [Phoneme("ɛː", template=state.current)]
    #         elif state.current.value in ["iː", "yː"]:
    #             return [Phoneme("iː", template=state.current)]
    #         elif state.current.value == "oː":
    #             return [Phoneme("oː", template=state.current)]
    #         elif state.current.value == "uː":
    #             return [Phoneme("uː", template=state.current)]
    #         return

    #     # vowel = a
    #     if vcc(["a"]):
    #         return [Phoneme("a", template=state.current)]
    #     # elif state.current.value == "a" and open_syllable:
    #     #     return [Phoneme("a", template=state.current)]
    #     elif state.current.value == "a" and len(state.following) > 1 and state.following[0].value + state.following[1].value in ["ld", "mb"]:
    #         return [Phoneme("ɔː", template=state.current)]
    #     elif state.current.value == "a":
    #         return [Phoneme("a", template=state.current)]
    #     elif state.current.value == "aː":
    #         return [Phoneme("ɔː", template=state.current)]
        
    #     # vowel = æ
    #     # elif state.current.value == "æ" and open_syllable:
    #     #     return [Phoneme("aː", template=state.current)]
    #     elif state.current.value == "æ":
    #         return [Phoneme("a", template=state.current)]
    #     elif vcc(["æː"]):
    #         if often():
    #             return [Phoneme("a", template=state.current)]
    #         else:
    #             return [Phoneme("e", template=state.current)]
    #     elif state.current.value == "æː":
    #         return [Phoneme("ɛː", template=state.current)]
        
    #     # vowel = e
    #     # elif state.current.value == "e" and open_syllable:
    #     #     return [Phoneme("ɛː", template=state.current)]
    #     elif often() and state.current.value == "e" and len(state.following) > 1 and state.following[0].value + state.following[1].value == "ld":
    #         return [Phoneme("ɛː", template=state.current)]
    #     elif state.current.value == "e" and len(state.preceding) > 0 and len(state.following) > 0 and state.preceding[0].value == "w" and state.following[0].value == "r":
    #         return [Phoneme("u", template=state.current)]
    #     elif state.current.value == "e":
    #         return [Phoneme("e", template=state.current)]
        
    #     # vowel = ea
    #     elif state.current.value == "ea":
    #         return [Phoneme("a", template=state.current)]

    #     # vowel = eo
    #     elif state.current.value == "eo" and len(state.preceding) > 0 and len(state.following) > 0 and state.preceding[0].value == "w" and state.following[0].value == "r":
    #         return [Phoneme("u", template=state.current)]
    #     elif state.current.value == "eo":
    #         return [Phoneme("e", template=state.current)]

    #     # vowel = ē
    #     elif often() and state.current.value == "eː" and len(state.following) > 0 and state.following[0].value == "c":
    #             return [Phoneme("i", template=state.current)]
    #     elif vcc(["eː"]):
    #         if often():
    #             return [Phoneme("e", template=state.current)]
    #         else:
    #             return [Phoneme("a", template=state.current)]
    #     elif often() and state.current.value == "eː" and len(state.following) > 0 and state.following[0].value == "r":
    #         return [Phoneme("ɛː", template=state.current)]
    #     elif state.current.value == "eː":
    #         return [Phoneme("eː", template=state.current)]

    #     # vowel = ēa
    #     elif vcc(["eːa"]):
    #         if often():
    #             return [Phoneme("a", template=state.current)]
    #         else:
    #             return [Phoneme("e", template=state.current)]
    #     elif state.current.value == "eːa":
    #         return [Phoneme("ɛː", template=state.current)]

    #     # vowel = ēo
    #     elif state.current.value == "eːo" and len(state.following) > 1 and state.following[0].value + state.following[1].value == "nd":
    #         # Special case added for "friend". No counterexamples yet
    #         return [Phoneme("eː", template=state.current)]
    #     elif vcc(["eːo"]):
    #         return [Phoneme("e", template=state.current)]
    #     elif state.current.value == "eːo" and len(state.following) > 0 and state.following[0].value == "c":
    #         if often():
    #             return [Phoneme("i", template=state.current)]
    #     elif state.current.value == "eːo" and len(state.following) > 0 and state.following[0].value == "r":
    #         if often():
    #             return [Phoneme("ɛː", template=state.current)]
    #         else:
    #             return [Phoneme("eː", template=state.current)]
    #     elif state.current.value == "eːo":
    #         if often():
    #             return [Phoneme("eː", template=state.current)]
    #         else:
    #             return [Phoneme("oː", template=state.current)]

    #     # vowel = y
    #     elif often() and state.current.value == "y" and len(state.following) > 1 and state.following[0] + state.following[1] in ["ld", "mb", "nd"]:
    #         return [Phoneme("i", template=state.current)]
    #     elif state.current.value == "y" and len(state.preceding) > 0 and len(state.following) > 0 and state.preceding[0].value == "w" and state.following[0].value == "r":
    #         return [Phoneme("e", template=state.current)]
    #     elif state.current.value == "y":
    #         if often():
    #             # Anglian dialect
    #             return [Phoneme("i", template=state.current)]
    #         elif often():
    #             # Kentish dialect
    #             return [Phoneme("e", template=state.current)]
    #         else:
    #             # West Saxon dialect
    #             return [Phoneme("u", template=state.current)]

    #     # vowel = ȳp
    #     elif vcc(["yː"]):
    #         return [Phoneme("i", template=state.current)]
    #     elif state.current.value == "yː":
    #         return [Phoneme("iː", template=state.current)]
    #     elif state.current.value == "i" and len(state.following) > 1 and state.following[0].value + state.following[1].value in ["ld", "mb", "nd"]:
    #         return [Phoneme("iː", template=state.current)]
    #     elif state.current.value == "i":
    #         return [Phoneme("i", template=state.current)]
    #     elif vcc(["iː"]):
    #         return [Phoneme("i", template=state.current)]
    #     elif occ() and vcv(["iː"]):
    #         return [Phoneme("i", template=state.current)]
    #     elif state.current.value == "iː":
    #         return [Phoneme("iː", template=state.current)]
    #     elif vcc(["oː"]):
    #         return [Phoneme("o", template=state.current)]
    #     elif state.current.value == "oː":
    #         return [Phoneme("oː", template=state.current)]
    #     elif state.current.value == "o" and len(state.preceding) > 0 and len(state.following) > 0 and state.preceding[0].value == "w" and state.following[0].value == "r":
    #         return [Phoneme("u", template=state.current)]
    #     elif state.current.value == "o":
    #         return [Phoneme("o", template=state.current)]
    #     elif state.current.value == "u":
    #         return [Phoneme("u", template=state.current)]
    #     elif vcc(["uː"]):
    #         return [Phoneme("u", template=state.current)]
    #     elif state.current.value == "uː":
    #         return [Phoneme("uː", template=state.current)]
    #     else:
    #         return None

# def the_big_chart(phonemes):
#     result = []
#     insert_lengthening_e = False
#     skip_next = 0

#     for i in range(0, len(phonemes)):
#         if skip_next > 0:
#             skip_next -= 1
#             continue

#         phone = phonemes[i]
#         prev2 = None
#         prev = None
#         next1 = None
#         next2 = None
#         next3 = None
#         if i > 1:
#             prev2 = phonemes[i - 2]
#         if i > 0:
#             prev = phonemes[i - 1]
#         if i < len(phonemes) - 1:
#             next1 = phonemes[i + 1]
#         if i < len(phonemes) - 2:
#             next2 = phonemes[i + 2]
#         if i < len(phonemes) - 3:
#             next3 = phonemes[i + 3]

#         # Diphthongs
#         if phone.is_vowel() and next1 and next1.value in ["g", "j", "w", "x"]:
#             if (phone.value + next1.value in ["æj", "æːj", "ej"]) \
#                 or (phone.value + next1.value == "eːj" and not next2):

#                 if not next2:
#                     result += "ay"
#                 else:
#                     result += "ai"
#             elif (phone.value + next1.value == "eːj" and next2 and next2.is_vowel()) \
#                 or (phone.value + next1.value in ["ij", "iːj", "yj", "yːj"]):

#                 if prev2 and prev2 and prev2.is_consonant() and prev.is_consonant():
#                     result += "y"
#                 else:
#                     result += random.choice(["ie", "uy"])
#             elif (phone.value + next1.value in ["æw", "aw"]) \
#                 or (phone.value + next1.value == "ag" and next2 and next2.is_vowel()):

#                 result += "aw"

#             elif phone.value + next1.value in ["æːw", "eːaw", "ew", "eow", "eːw", "eːow", "iw", "iːw", "yw", "yːw"]:
#                 if next1:
#                     result += random.choice(["ew", "ue", "u"])
#                 else:
#                     result += random.choice(["ew", "ue"])

#             elif phone.value + next1.value in ["aːw", "ow", "oːw"] \
#                  or (phone.value + next1.value in ["aːg", "og", "oːg"] and next2 and next2.is_vowel):

#                 result += "ow"

#             elif phone.value + next1.value in ["ug", "uːg"]: # Modified chart here

#                 if next1.is_vowel():
#                     skip_next += 1

#                 if next2 and next2.value == "t" or next2.is_vowel() and next3 and next3.value == "t":
#                     result += "ough"
#                 else:
#                     result += random.choose("ow", "ough")

#             elif phone.value + next1.value in ["æx", "ax"] \
#                 or (phone.value + next1.value == "ag" and not next2):

#                 result += "augh"

#             elif phone.value + next1.value == "ex":
#                 result += "ai"

#             elif phone.value + next1.value in ["eːx", "ix", "iːx", "yx", "yːx"]:
#                 result += "igh"

#             elif phone.value + next1.value in ["aːx", "ox"] \
#                 or (phone.value + next1.value in ["aː", "og"] and not next2):
#                 result += "ough"

#             elif phone.value + next1.value in ["aːx", "ox", "oːx"] and next2 and next2.is_consonant:
#                 result += random.choice(["ough", "augh"])

#             elif phone.value + next1.value in ["ux", "uːx"] \
#                 or (phone.value + next1.value in ["oːx", "oːg", "ug", "uːg"] and not next2):
#                 result += "ough"
#             else:
#                 # No match found
#                 continue

#             skip_next += 1
#             continue

#         # Monophthongs
#         elif phone.is_vowel():
#             if (phone.value in ["a", "æ", "ea"] or (phone.value == "aː" and next1 and next1.is_geminate())) \
#                 or (often() and phone.value in ["æː", "eːa"] and next1 and next1.is_geminate()) \
#                 or (occ() and phone.value == "eː" and next1 and next1.value.is_geminate()): # WS ǣ+CC
                    
#                     if not syllable.is_in_open_syllable(phonemes, i):
#                         result += "a"
#                     else:
#                         result += "a"
#                         insert_lengthening_e = True

#             elif (phone.value in ["e", "eo"] or (phone.value in ["eː", "eːo"] and next1 and next1.is_geminate())) \
#                 or (often() and phone.value in ["æː", "eːa"] and next1 and next1.is_geminate()) \
#                 or (occ() and phone.value == "y") \
#                 or (occ() and phone.value in ["æː", "eːa"] and next1 and next1.value.is_geminate()): # WS ǣ+CC
#                     if next1 and next1.value == "r":
#                         result += random.choice(["ar", "er"])
#                         skip_next += 1

#                     if not syllable.is_in_open_syllable(phonemes, i):
#                         result += "e"
#                     else:
#                         if random.randint(0, 1) == 0:
#                             result += "ea"
#                         else:
#                             result += "e"
#                             insert_lengthening_e = True

#             elif (phone.value in ["i", "y"] or (phone.value in ["iː", "yː"] and next1 and next1.is_geminate())) \
#                 or (occ() and phone.value in ["eːo", "eː"] and next1 and next1.value == "c") \
#                 or (occ() and phone.value in ["iː", "yː"] and next1 and next1.is_consonant() and next2 and next2.is_vowel()):

#                     if not syllable.is_in_open_syllable(phonemes, i):
#                         result += "i"
#                     elif occ():
#                         result += "ee"
#             elif (phone.value == "o" or (phone.value == "oː" and next1 and next1.is_geminate())):
#                 if not syllable.is_in_open_syllable(phonemes, i):
#                     result += "o"
#                 else:
#                     if random.randint(0, 1) == 0:
#                         result += "oa"
#                     else:
#                         result += "o"
#                         insert_lengthening_e = True
#             elif (phone.value == "u" or (phone.value == "uː" and next1 and next1.is_geminate())) \
#                 or (occ() and phone.value == "y"):
#                     if occ() and syllable.is_in_open_syllable(phonemes, i):
#                         result += "oo"
#                     else:
#                         result += "u"

#                     # TODO: Add exception to catch 'lufian' -> 'love'?
#             elif (prev and prev.value == "w" and phone.value in ["e", "eo", "o", "y"] and next1 and next1.value == "r"):
#                 result += "o"
#             elif phone.value == "aː" \
#                 or (phone.value == "a" and next1 and next2 and next1.value + next2.value in ["ld", "mb"]):
#                 if random.randint(0, 1) == 0:
#                     result += "oa"
#                 else:
#                     result += "o"
#                     insert_lengthening_e = True
#             elif phone.value in ["æː", "eːa"]:
#                 if random.randint(0, 1) == 0:
#                     result += "ea"
#                 else:
#                     result += "e"
#                     insert_lengthening_e = True
#             elif phone.value in ["eː", "eːo"] \
#                 or (phone.value == "e" and next1 and next2 and next1.value + next2.value == "ld"):

#                 if next1 and next2 and next1.value + next2.value in ["nd", "ld"]:
#                     result += "ie"
#                 elif often() and next1 and next1.value == "r":
#                     if random.randint(0, 1) == 0:
#                         result += "ear"
#                     else:
#                         result += "er"
#                         insert_lengthening_e = True
#                 elif occ() and next1 and next1.value == "r":
#                     result += "eer"
#                 else:
#                     result += "ee"

#             elif phone.value in ["iː", "yː"] \
#                 or (often() and phone.value == "i" and next1 and next2 and next1.value + next2.value in ["ld", "mb", "nd"]) \
#                 or (often() and phone.value == "y" and next1 and next2 and next1.value + next2.value in ["ld", "mb", "nd"]):

#                 result += "i"

#                 if next1 and next1.is_consonant() and not next2:
#                     insert_lengthening_e = True

#             elif phone.value == "oː" \
#                 or (occ() and phone.value == "eːo"):

#                 result += "oo"

#             elif phone.value == "uː" \
#                 or (often() and phone.value == "u" and next1 and next2 and next1.value + next2.wordvalue == "nd"):

#                 result += "ou"

#             elif phone.value == "ə":
#                 result += "e"

#         # Consonants
#         else:

#             if phone.value == "f":
#                 if (prev and (prev.is_vowel() or prev.is_voiced())) \
#                     and (next1 and (next1.is_vowel() or next1.is_voiced())):
#                     result += "v"
#                 else:
#                     if next1 != None:
#                         result += "f"
#                     else:
#                         result += "ff"
#             elif phone.value == "l":
#                 if next1 != None or (prev and prev.is_vowel() and prev.is_long()):
#                     result += "l"
#                 else:
#                     result += "ll"
#             elif phone.value == "s":
#                 if next1 != None:
#                     result += "s"
#                 else:
#                     result += "ss"
#             elif phone.value == "θ":
#                 result += "th"
#             elif phone.value in ["x", "xx"]:
#                 if prev == None:
#                     result += "h"
#                 else:
#                     result += "gh"
#             elif phone.value == "k":
#                 if next1 != None:
#                     result += "k"
#                 else:
#                     result += "ck"
#             elif phone.value == "tʃ":
#                 result += "ch"
#             elif phone.value == "dʒ":
#                 if next1 != None:
#                     result += "j"
#                 else:
#                     result += "dge"
#             else:
#                 result += phone.value

#             if phone.is_consonant and insert_lengthening_e and (not next1 or not next1.is_vowel()):
#                 result += "e"
#                 insert_lengthening_e = False


#     return "".join(result)

def orthography(phonemes):
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

        if insert_lengthening_e and phone.is_vowel():
            insert_lengthening_e = False

        # Monophthongs
        if phone.value == "a":
            result += "a"
        elif phone.value == "aː":
            result += "a"
            insert_lengthening_e = True
        elif phone.value == "e" and next1 and next1.value == "r":
            # These cases seem ambiguous. 
            # "ea" may be more common when descending from "eo" spelling?
            if often():
                result += "ea"
            elif often():
                result += "a"
            else:
                result += "e"
        elif phone.value == "ɛː":
            if often():
                result += "ea"
            else:
                result += "e"
                insert_lengthening_e = True
        elif phone.value == "i":
            result += "i"
        elif phone.value == "iː" and next1 and next1.is_consonant() and next2 and next2.is_consonant():
            result += "i"
        elif phone.value == "iː":
            result += "i"
            insert_lengthening_e = True
        elif phone.value == "eː" and next1 and next2 and next1.value + next2.value in ["nd", "ld"]:
            result += "ie"
        elif phone.value == "eː":
            result += "ee"
        elif phone.value == "o":
            result += "o"
        elif phone.value == "ɔː":
            if often():
                result += "oa"
            else:
                result += "o"
                insert_lengthening_e = True
        elif phone.value == "oː":
            result += "oo"
        elif phone.value == "u" and next1 and next1.value == "r":
            result += "o"
        elif phone.value == "u":
            result += "u"
        elif phone.value == "uː":
            result += "ou"
        elif phone.value == "ə":
            result += "e"

        # Consonants
        elif phone.value == "f":
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

        if phone.is_consonant() and insert_lengthening_e and (not next1 or not next1.is_vowel()):
            result += "e"
            insert_lengthening_e = False


    return "".join(result)