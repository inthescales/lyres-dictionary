from src.diachron.phoneme import Phoneme
from src.diachron.changerig import RigState, Rig

def phonemes_from_oe(oe_phonemes):
    phonemes = oe_phonemes

    # Skipping homorganic lengthening for now

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

    # Vocalization of [ɣ]
    new_phonemes = []
    for i in range(0, len(phonemes)):
        phoneme = phonemes[i]
        if i > 0 and phonemes[-1].is_vowel() and phoneme.value == "ɣ":
            new_phonemes.append(Phoneme("u"))
        else:
            new_phonemes.append(phoneme)
    phonemes = new_phonemes

    # TO DO: Add new diphthongs

    # Breaking
    # new_phonemes = []
    # for i in range(0, len(phonemes)):
    #     phoneme = phonemes[i]
    #     next_phoneme = None
    #     if i < len(phonemes) - 1:
    #         next_phoneme = phonemes[i+1]

    #     new_phonemes.append(phoneme)

    #     if next_phoneme and next_phoneme.value == "x":
    #         if phoneme.is_front_vowel() and phoneme.value != "ɑ":
    #             new_phonemes.append(Phoneme("i"))
    #         if phoneme.is_back_vowel() or phoneme.value == "ɑ":
    #             new_phonemes.append(Phoneme("u"))

    # phonemes = new_phonemes

    # Not sure if I did breaking correctly. Need to find an example

    # Open-syllable lengthening
    new_phonemes = []
    for i in range(0, len(phonemes)):
        phoneme = phonemes[i]
        if phoneme.is_consonant():
            new_phonemes.append(phoneme)
        elif is_in_open_syllable(phonemes, i) and following_syllable_count(phonemes, i) == 1:
            joined = "".join([p.value for p in phonemes])
            if phoneme.value == "e":
                new_phonemes.append(Phoneme("ɛː", phoneme.stressed))
            elif phoneme.value == "o":
                new_phonemes.append(Phoneme("ɔː", phoneme.stressed))
            # Only occasionally applied to these high vowels
            # elif phoneme.value == "u":
            #     new_phonemes.append(Phoneme("oː", phoneme.stressed))
            # elif phoneme.value == "i":
            #     new_phonemes.append(Phoneme("eː", phoneme.stressed))
            else:
                new_phonemes.append(phoneme.get_lengthened())
        else:
            new_phonemes.append(phoneme)

    phonemes = new_phonemes

    # Trisyllabic laxing
    new_phonemes = []
    for i in range(0, len(phonemes)):
        phoneme = phonemes[i]
        if phoneme.is_consonant():
            new_phonemes.append(phoneme)
        elif following_syllable_count(phonemes, i) >= 2 \
            and i + 2 < len(phonemes) \
            and phonemes[i+1].is_consonant() \
            and phonemes[i+2].is_consonant():

            new_phonemes.append(phoneme.get_shortened())
        else:
            new_phonemes.append(phoneme)

    phonemes = new_phonemes

    # Come back to interactions between open-syllable lengthening and trisyllabic laxing
    #   The effects of open-syllable lengthening and trisyllabic laxing often led to differences
    #   in the stem vowel between singular and plural/genitive. Generally these differences
    #   were regularized by analogy in one direction or another, but not in a consistent way...

    # Pre-cluster shortening
    new_phonemes = []
    for i in range(0, len(phonemes)):
        phoneme = phonemes[i]
        if phoneme.is_consonant():
            new_phonemes.append(phoneme)
        elif i + 3 < len(phonemes) \
        and phonemes[i+1].is_consonant() \
        and phonemes[i+2].is_consonant() \
        and phonemes[i+3].is_consonant():
            new_phonemes.append(phoneme.get_shortened())
        else:
            new_phonemes.append(phoneme)
    phonemes = new_phonemes

    # Come back to:
    #   Later in Middle English, vowels were shortened before clusters of two consonants,
    #   except before /st/ and in some cases where homorganic lengthening applied.

    # Reduction of double consonants
    new_phonemes = []
    for i in range(0, len(phonemes)):
        phoneme = phonemes[i]
        length = len(phoneme.value)
        if phoneme.is_consonant():
            new_phonemes.append(phoneme.get_geminate_reduced())
        else:
            new_phonemes.append(phoneme)
    phonemes = new_phonemes

    # Homebrew ------------------

    # Remove initial H before consonants
    new_phonemes = []
    for i in range(0, len(phonemes)):
        phoneme = phonemes[i]
        if i + 1 < len(phonemes):
            next_phoneme = phonemes[i+1]
            if i == 0 and phoneme.value == "x" and next_phoneme.is_consonant():
                continue
            else:
                new_phonemes.append(phoneme)
        else:
            new_phonemes.append(phoneme)
    phonemes = new_phonemes

    # Template
    # new_phonemes = []
    # for i in range(0, len(phonemes)):
        # ...
    # phonemes = new_phonemes

    return phonemes

# ==============================================
# ==============================================

def phonemes_from_oe_3(oe_phonemes):
    phonemes = oe_phonemes

    rig = Rig(phonemes)

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

    def e_diphthong_replacement(state):
        if state.current.value == "eɑ":
            return Phoneme("ɑ", template=state.current)
        elif state.current.value == "eːɑ":
            return Phoneme("ɛː", template=state.current)
        elif state.current.value == "eo":
            return Phoneme("e", template=state.current)
        elif state.current.value == "eːo":
            return Phoneme("eː", template=state.current)
        else:
            return state.current

    # æj → aj → ej
    # {æːj,e(ː)j} → ej 
    def æj_to_ej(state):
        if state.next_value == "j" and state.current.value in ["æ", "æː", "e", "eː"]:
            # At an intermediate stage this would be "a" instead"
            return Phoneme("e", template=state.current)
        else:
            return state.current

    # ɑɣ → ɑw 
    def a_breaking(state):
        if state.prev_value and state.prev_value + state.current.value == "ɑɣ":
            return Phoneme("w", template=state.current)
        else:
            return state.current

    # {eɑh,eɑç,eɑx,eɑʝ,eɑɣ} → ɑw
    def diphthong_breaking(state):
        if state.joined[-1] in ["x", "ɣ"] and state.joined[:-1] in ["æɑ", "æːɑ"]:
            return [Phoneme("ɑ", template=state.capture[0]), Phoneme("w", template=state.capture[-1])]

    # eːɑw iːw → ew ju
    def ew_ju(state):
        if state.joined == "eːɑw":
            return [Phoneme("e", template=state.capture[0]), Phoneme("w", template=state.capture[-1])]
        elif state.joined == "iːw":
            return [Phoneme("j", template=state.capture[0]), Phoneme("u", template=state.capture[-1])]

    # {ɑːw,ɑːɣ,oːw} → ɔːw 
    def owww(state):
        if state.joined in ["ɑːw", "ɑːɣ", "oːw"]:
            return [Phoneme("ɔː", template=state.capture[0]), Phoneme("w", template=state.capture[-1])]

    # oɣ → ɔːw / _V 
    def ogow(state):
        if state.joined == "oɣ" and state.next_phoneme.is_vowel():
            return [Phoneme("ɔː", template=state.capture[0]), Phoneme("w", template=state.capture[-1])]

    # {ɑːht,o(ː)ht} → ow 
    def htow(state):
        if state.joined in ["ɑːht", "oht", "oːht"]:
            return [Phoneme("o", template=state.capture[0]), Phoneme("w", template=state.capture[-1])]

    # ɑː y(ː) → ɔː i(ː)
    def ay_vowel_changes(state):
        if state.current.value == "ɑː":
            return [Phoneme("ɔː", template=state.current)]
        elif state.current.value == "y":
            return [Phoneme("i", template=state.current)]
        elif state.current.value == "yː":
            return [Phoneme("iː", template=state.current)]

    # ɑ e o → ɑː ɛː oː / in U[+open] ! in #U with the following U containing /iː/ or ending
    # in one of /m n r l/ 
    def back_mid_lengthening(state):
        if state.current.value in ["ɑ", "e", "o"] and state.syllable_data.is_open \
            and not (state.syllable_data.next_other_syllable_vowel.value == "iː" or state.syllable_data.next_consonant.value in ["m", "n", "r", "l"]):
            return [state.current.get_lengthened()]

    # Vː → V[-long] / in #U before a U with /iː/ 
    def shorten_in_syllable_before_long_i(state):
        next_other = state.syllable_data.next_other_syllable_vowel
        if state.current.is_vowel() and state.current.is_long() \
            and next_other and next_other.value == "iː":
            return state.current.get_shortened()

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
        if len(state.joined) == 2 and state.joined[0] == "h" and state.joined[1] in ["n", "l", "r"]:
            return [Phoneme(state.joined[0], template=state.capture[-1])]
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

    # {e,ɑ,o} → ə → ∅ / _# 
    def reduce_final_vowel(state):
        if state.current.value in ["e", "ɑ" ,"o"] and state.next == None:
            # return [Phoneme("ə", template=state.current)]
            return []

    rig.run_capture(pre_cluster_shortening, 1)
    rig.run_change(e_diphthong_replacement)
    rig.run_change(æj_to_ej)
    rig.run_change(a_breaking)
    rig.run_capture(diphthong_breaking, 2)
    rig.run_capture(ew_ju, 2)
    rig.run_capture(owww, 2)
    rig.run_capture(ogow, 2)
    rig.run_capture(htow, 3)
    rig.run_capture(ay_vowel_changes, 1)
    rig.run_capture(back_mid_lengthening, 1)
    rig.run_capture(shorten_in_syllable_before_long_i, 1)
    rig.run_capture(final_unstressed_m_to_n, 1)
    rig.run_capture(drop_inflecional_n, 1)
    rig.run_capture(drop_initial_h, 1)
    rig.run_capture(initial_g, 1)
    rig.run_capture(g_to_w, 1)
    rig.run_capture(reduce_final_vowel, 1)

    return rig.phonemes
