import random

from src.diachronizer.engine.phoneme import Phoneme
from src.diachronizer.engine.transform_rig import RigState, Rig
from src.diachronizer.engine.helpers import often, even, occ, hinge

def from_oe_phonemes(oe_phonemes, config):
    phonemes = oe_phonemes

    rig = Rig(phonemes)
    form = ""

    def harden_g(state):
        if (state.current.value == "ɣ" and not state.prev) \
            or (state.current.value == "ɣ" and state.prev and state.prev.value == "n"):
            return [Phoneme("g", template=state.current)]
        elif state.current.value == "ɣɣ":
            return [Phoneme("gg", template=state.current)]

    def homorganic_lengthening(state):
        if state.capture[0].is_vowel() \
            and (state.joined[1:3] in ["ld", "mb", "nd", "rd"] or state.joined[1:3] in ["ng", "rl", "rn"]) \
            and not (len(state.following) > 0 and state.following[0].is_consonant()):
            # and not state.syllable_data.following_syllable_count > 1:
            
            return [state.capture[0].get_lengthened(), state.capture[1], state.capture[2]]

    def stressed_vowel_changes(state):
        if state.current.stressed:
            if state.prev and state.prev.value == "w" \
                and not (len(state.preceding) > 1 and state.preceding[-2].value == "s") \
                and state.next and state.next.value == "r" \
                and state.current.value in ["e", "eo", "o", "y"]:
                return [Phoneme("u", template=state.current)]
            elif state.current.value in ["eː", "eːo"] and state.next and state.next.value == "r" \
                and often("SVC:eːr->ɛːr", config):
                return [Phoneme("ɛː", template=state.current)]
            elif state.current.value in ["eː", "eːo"] and state.next and state.next.value == "k" \
                and occ("SVC:eːc->ic", config):
                return [Phoneme("i", template=state.current)]
            elif state.current.value in ["æ", "ea", "a"]:
                return [Phoneme("a", template=state.current)]
            elif state.current.value in ["æː", "eːa"]:
                return [Phoneme("ɛː", template=state.current)]
            elif state.current.value == "aː":
                return [Phoneme("ɔː", template=state.current)]
            elif state.current.value == "eo":
                return [Phoneme("e", template=state.current)]
            elif state.current.value == "eːo":
                result = often("SVC:eːo->eː/oː", config)
                if result == "eː":
                    return [Phoneme("eː", template=state.current)]
                elif result == "oː":
                    return [Phoneme("oː", template=state.current)]
            elif state.current.value == "y":
                result = hinge("SVC:y->i/e/u", [0.5, 0.3], config)
                if result == "i":
                    # Anglian dialect
                    return [Phoneme("i", template=state.current)]
                elif result == "e":
                    # Kentish dialect
                    return [Phoneme("e", template=state.current)]
                elif result == "u":
                    # West Saxon dialect
                    return [Phoneme("u", template=state.current)]
            elif state.current.value == "yː":
                result = hinge("SVC:y->i/e/u", [0.5, 0.3], config)
                if result == "i":
                    # Anglian dialect
                    return [Phoneme("iː", template=state.current)]
                elif result == "e":
                    # Kentish dialect
                    return [Phoneme("eː", template=state.current)]
                elif result == "u":
                    # West Saxon dialect
                    return [Phoneme("uː", template=state.current)]

    def pre_cluster_shortening(state):
        if state.current.is_vowel() and state.current.is_long() \
            and state.next and state.next.is_consonant() \
            and (state.next.is_geminate() \
                or (len(state.following) > 1 and state.following[1].is_consonant()) \
                or (len(state.following) > 0 and state.following[0].value == "ʃ")): # 'sċ' may count as a cluster (ex. 'flǣsċ')
                next_two_joined = "".join([x.value for x in state.following[:2]])

                # other lengthening clusters: mb, ld
                lengthening_clusters = ["nd", "rl", "rs", "ld"] # rs+vowel?
                if not occ("PCS:rn", config):
                    lengthening_clusters += ["rn"]
                if not occ("PCS:rd", config):
                    lengthening_clusters += ["rd"]
                if next_two_joined in lengthening_clusters \
                    or (next_two_joined == "st" and (len(state.following) == 2 or state.following[2].is_vowel())):
                    return None

                if state.current.value == "ɔː":
                    return [Phoneme("a", template=state.current)]
                elif state.current.value == "ɛː" and often("PCS:ɛː->a", config):
                    return [Phoneme("a", template=state.current)]
                else:
                    return [state.current.get_shortened()]

    # Reduced double consonants to a single consonant
    def reduction_of_double_consonants(state):
        return [state.current.get_geminate_reduced()]

    # Reduce all unstressed vowels to /ə/
    def reduction_of_unstressed_vowels(state):
        if state.current.is_vowel() and not state.current.stressed:
            if state.prev and state.prev.is_vowel() and not state.prev.stressed:
                return []
            else:
                return [Phoneme("ə", template=state.current)]

    def vocalization_of_post_vocalic_g(state):
        if state.current.value == "ɣ" and state.prev and state.prev.is_vowel() and state.next:
            return [Phoneme("u", template=state.current, history=["vocalized-g"])]
        elif state.current.value == "ɣ" and not state.next:
            return [Phoneme("x", template=state.current)]
        elif state.current.value == "w" and state.prev and state.prev.is_vowel():
            return [Phoneme("u", template=state.current)]

    # Formation of diphthongs involving three phonemes
    # For technical reasons, separated from those involving two
    def diphthong_formation_3(state):
        two_joined = "".join([p.value for p in state.capture[:2]])
        vowel_after = state.capture[2].is_vowel()
        
        if two_joined == "eːj" and vowel_after:
            return [Phoneme("iː", template=state.capture[0])]
        elif two_joined == "au" and vowel_after:
            return [Phoneme("au", template=state.capture[0])]
        elif two_joined in ["ɔːu", "ou", "oːu"] and vowel_after:
            return [Phoneme("ɔu", template=state.capture[0])]
        elif two_joined in ["uu", "uːu"] and vowel_after:
            return [Phoneme("uː", template=state.capture[0])]

    # Formation of diphthongs involving two phonemes
    # For technical reasons, separated from those involving three
    def diphthong_formation_2(state):
        vowel_after = state.next and state.next.is_vowel()
        word_end = state.next == None

        if state.joined in ["aj", "aːj", "ɛj", "ɛːj", "ej"] \
            or (state.joined == "eːj" and word_end):
            return [Phoneme("ai", template=state.capture[0])]
        elif (state.capture[0].value == "eːj" and vowel_after) \
            or state.joined in ["ij", "iːj", "yj", "yːj"]:
            return [Phoneme("iː", template=state.capture[0])]
        elif state.joined == "au":
            return [Phoneme("au", template=state.capture[0])]
        elif state.joined in ["ɛːu", "eu", "eou"]:
            return [Phoneme("ɛu", template=state.capture[0])]
        elif state.joined in ["ɔːu", "ou", "oːu"]:
            return [Phoneme("ɔu", template=state.capture[0])]
        elif state.joined in ["eːu", "eːou", "iu", "iːu", "yu", "yːu"]:
            return [Phoneme("iu", template=state.capture[0])]
        elif (state.joined in ["oːx", "oːx", "ux", "uːx"] and not vowel_after) \
            or state.joined in ["ux", "uːx"]:
            return [Phoneme("uː", template=state.capture[0]), Phoneme("x", template=state.capture[0])]
        elif (state.joined in ["ɔːx", "ox"] and not vowel_after) \
            or state.joined in ["ɔːx", "ox"]:
            return [Phoneme("ɔu", template=state.capture[0]), Phoneme("x", template=state.capture[0])]

    # Breaking
    # Inserts /i/ or /u/ between vowels and a following /x/ (or sometimes /g/)
    def breaking(state):
        word_end = state.next == None

        test_string = state.capture[0].value + state.capture[1].get_geminate_reduced().value
        if test_string == "ax" \
            or (test_string == "au" and word_end):
            return [Phoneme("au", template=state.capture[0]), Phoneme("x", template=state.capture[1])]
        elif test_string == "ex":
            return [Phoneme("ɛi", template=state.capture[0]), Phoneme("x", template=state.capture[1])]
        elif test_string in ["eːx", "ix", "iːx", "yx", "yːx"]:
            return [Phoneme("iː", template=state.capture[0]), Phoneme("x", template=state.capture[1])]
        elif test_string in ["aːx", "ox"] \
            or (test_string in ["aːu", "ou"] and word_end):
            return [Phoneme("ɔu", template=state.capture[0]), Phoneme("x", template=state.capture[1])]
        elif test_string in ["ux", "uːx"] \
            or (test_string in ["oːx", "oːu", "uu", "uːu"] and word_end):
            return [Phoneme("ɔu", template=state.capture[0]), Phoneme("x", template=state.capture[1])]

    # ɣ → w / C_V 
    def g_to_w(state):
        if state.current.value == "ɣ" \
            and state.prev and state.prev.is_consonant() \
            and state.next and state.next.is_vowel():
            return [Phoneme("w", template=state.current)]

    # Open syllable lengthening
    def open_syllable_lengthening(state):
        if state.current.is_vowel() and state.syllable_data.is_open \
            and not state.current.value == "ə" and not state.current.is_diphthong() \
            and state.syllable_data.following_syllable_count == 1 \
            and not (state.next and state.next.value == "w"):
            if state.current.value in ["i", "y"]:
                if occ("OSL:iy", config):
                    return [Phoneme("eː", state.current.stressed)]
            elif state.current.value == "u":
                if occ("OSL:u", config):
                    return [Phoneme("oː", state.current.stressed)]
            elif state.current.value in ["e", "eo"]:
                return [Phoneme("ɛː", state.current.stressed)]
            elif state.current.value == "o":
                return [Phoneme("ɔː", state.current.stressed)]
            else:
                return [state.current.get_lengthened()]

    def trisyllabic_laxing(state):
        if state.current.is_vowel() and state.syllable_data.following_syllable_count > 1:
            return [state.current.get_shortened()]

    # m → n / _# when unstressed
    def final_unstressed_m_to_n(state):
        if state.current.value == "m" and state.next == None \
            and not (state.syllable_data.prev_vowel and state.syllable_data.prev_vowel.stressed):
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
        
        # Experimental - remove some other 'ə's

        # ərld
        if state.current.value == "ə" \
            and state.prev and state.prev.value == "r" \
            and len(state.following) >= 2 and "".join([x.value for x in state.following[:2]]) == "ld":
            return []
        
        if state.current.value == "ə" \
            and state.prev and state.prev.value in ["iː"]:
            return []

    def distinguish_voiced_fricatives(state):
        if state.current.is_consonant() and state.current.is_fricative() \
            and (state.prev and (state.prev.is_vowel() or state.prev.is_voiced())) \
            and (state.next and (state.next.is_vowel() or state.next.is_voiced())) \
            and not state.current.value in ["x"]:
            return [state.current.get_voiced()]

    # Insert a schwa between inconvenient final consonant clusters
    # Not referenced in my sources, but added here to handle cases like
    # 'hræfn' -> 'raven', 'fæþm' -> 'fathom', 'swealwe' -> 'swallow', etc.
    #
    # Also handles word-final metathesis in cases like 'blēddre' -> 'bladder'
    def final_consonant_cluster_breaking(state):
            if all(phone.is_consonant() for phone in state.capture) \
                and len(state.following) == 0 \
                and not (state.capture[0].is_nasal() and state.capture[1].is_plosive()) \
                and not (state.capture[0].is_fricative() and state.capture[1].is_plosive()) \
                and not (state.capture[0].is_semivowel() and state.capture[1].is_fricative()) \
                and not (state.capture[0].is_semivowel() and state.capture[1].is_nasal()) \
                and not (state.capture[0].is_semivowel() and state.capture[1].is_plosive()) \
                and not (state.capture[0].is_plosive() and state.capture[1].is_plosive()) \
                and not (state.joined in ["rl"]) \
                and not (state.capture[1].value == "j"):
                return [state.capture[0], Phoneme("ə"), state.capture[1]]
    
    def d_ð_alternation(state):
        if state.joined == "dər" and often("DThA:dər->ðər", config):
            return [Phoneme("ð", state.capture[0]), Phoneme("ə" , state.capture[1]), Phoneme("r" , state.capture[2])]
        elif state.joined == "ðər" and occ("DThA:ðər->dər", config):
            return [Phoneme("d" , state.capture[0]), Phoneme("ə" , state.capture[1]), Phoneme("r" , state.capture[2])]
    
    if config.verbose:
        print("/" + "".join(p.value for p in rig.phonemes) + "/" + config.separator)

    rig.run_capture(harden_g, 1, "Harden g's", config)
    rig.run_capture(homorganic_lengthening, 3, "Homorganic lengthening", config)
    rig.run_capture(stressed_vowel_changes, 1, "Stressed vowel changes", config)
    rig.run_capture(reduction_of_unstressed_vowels, 1, "Reduction of unstressed vowels", config)
    rig.run_capture(final_unstressed_m_to_n, 1, "Final unstressed m to n", config)
    rig.run_capture(drop_inflecional_n, 1, "Drop inflectional n", config)
    rig.run_capture(vocalization_of_post_vocalic_g, 1, "Vocalization of post-vocalic ɣ", config)
    rig.run_capture(g_to_w, 1, "G to w", config)
    rig.run_capture(diphthong_formation_3, 3, "Diphthong formation 1", config)
    rig.run_capture(diphthong_formation_2, 2, "Diphthong formation 2", config)
    rig.run_capture(breaking, 2, "Breaking", config)
    rig.run_capture(open_syllable_lengthening, 1, "Open syllable lengthening", config)
    rig.run_capture(trisyllabic_laxing, 1, "Trisyllabic laxing", config)
    rig.run_capture(pre_cluster_shortening, 1, "Pre-cluster shortening", config)
    rig.run_capture(distinguish_voiced_fricatives, 1, "Distinguish voiced fricatives", config)
    rig.run_capture(reduction_of_double_consonants, 1, "Reduction of double consonants", config)
    rig.run_capture(drop_initial_h, 2, "Drop initial h", config)
    rig.run_capture(loss_of_final_unstressed_vowel, 1, "Loss of final unstressed vowel", config)
    rig.run_capture(final_consonant_cluster_breaking, 2, "Break inconvenient final consonant clusters", config)
    rig.run_capture(d_ð_alternation, 3, "d/ð alternation", config)

    return rig.phonemes
