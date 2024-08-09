import random

from src.evolutor.engine.phoneme import Phoneme
from src.evolutor.engine.transform_rig import RigState, Rig
from src.evolutor.engine.hinges import often, even, occ, hinge

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

    # The 'ċġ' digraph is represented phonemically as /dʒ/ in this system. However, there are
    # cases where it resolves as /j/ in MnE, as in 'seċġan' -> 'say' and 'leċġan' -> 'lay'.
    # This is an attempt to capture these cases, in distinction against cases like 'edge',
    # 'sedge', 'cudgel'
    #
    # NOTE: OED indicates that this is not properly understood as a phonetic process, but rather a
    # leveling to stem forms in these verbs, where the stem forms had 'ġ' instead of 'ċġ'. See this
    # note from the OED's etymology for 'buy':
    # 
    #   In Old English the form of the present stem bycg- reflects gemination of stem-final West Germanic
    #   g before the inflectional suffix j and the development of that geminated consonant to a voiced
    #   affricate. This stem form originally occurred in the infinitive, 1st singular and plural present
    #   indicative, present subjunctive, present participle, and imperative plural. The stem form without
    #   gemination, Old English byg-, shows regular palatalization of the stem-final consonant, with subsequent
    #   development of a long vowel or a diphthong in Middle English. This stem form originally occurred in the
    #   2nd and 3rd singular present indicative and imperative singular (compare Forms 1b and 1c); levelling
    #   to all other forms of the present tense (already very occasionally attested in Old English; compare
    #   Northumbrian byges, present indicative plural) is reflected in the modern standard pronunciation
    #
    # Despite this, I am going to leave it here in the phonetics for now, since it seems to adequately
    # model modern forms for both nouns and verbs. However, if this produces inaccuracies in the future, it
    # should be changed. 
    def cg_distinction(state):
        if state.current.value == "dʒ" \
            and state.prev and state.prev.is_vowel() and state.prev.value in ["i", "iː", "e", "eː"] \
            and state.next and state.next.is_vowel() \
            and not len(state.preceding) == 1:
            return [Phoneme("j", template=state.current)]

    # Lengthening of vowels followed by certain homorganic consonant clusters
    #
    # Per Kruger(2020):
    # https://benjamins.com/catalog/jhl.18028.kru
    # Also cites Minkova & Stockwell (1992), Minkova (2014)
    # - 'ld' always lengthens after back vowels 'a' and 'o'
    # - 'ld' lengthens after front vowels 'e' and 'i' about 60% of the time
    # - 'ld' lengthens after high back vowel 'u' in exactly one case 'sċuldor' -> 'shoulder' (I've ignored it here)
    # - 'nd' always lengthens after high vowels 'i' and 'u'
    # - 'nd' never lengthens after mid/low vowels 'a', 'e', 'o'
    #
    # My own observations:
    # — 'ng' appears to lengthen frequently after 'a', as in 'long', 'strong', 'monger', but not always, as in 'sang'
    # - 'ng' does not lengthen after other vowels that I've seen so far. Consider 'sing', 'sting', 'ring'
    # - 'o' seems to lengthen into /ɔː/, as in 'board' and 'hoard'
    #
    # TODO: Get better information on the remaining clusters
    def homorganic_lengthening(state):
        vowel = state.capture[0].value
        cluster = "".join([x.value for x in state.capture[1:]])

        if state.capture[0].is_vowel() and not state.capture[0].is_diphthong() \
            and (
                cluster in ["rd", "rl", "rn"]
                or (cluster == "ld" and vowel in ["a", "o"])
                or (cluster == "ld" and vowel in ["e", "i"] and hinge("HL:ld-front", 0.6, config))
                or (cluster == "nd" and vowel in ["i", "u"])
                or (cluster == "mb" and occ("HL:mb", config))
                or (cluster == "ng" and vowel == "a" and often("HL:ng", config))
            ) \
            and not (len(state.following) > 0 and state.following[0].is_consonant()):
    
            if state.capture[0].value == "o":
                lengthened = "ɔː"
            else:
                lengthened = state.capture[0].get_lengthened().value
    
            return [Phoneme(lengthened, template=state.capture[0]), state.capture[1], state.capture[2]]

    def pre_three_cluster_shortening(state):
        if state.current.is_vowel() and state.current.is_long() \
            and len(state.following) >= 3 and all(phoneme.is_consonant() for phoneme in state.following[:3]):

            return [state.current.get_shortened()]

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
                # TODO: Handle 'ġeong'-> 'young'
                return [Phoneme("e", template=state.current)]
            elif state.current.value == "eːo":
                if state.next and state.next.value in ["ɣ", "j"]:
                    # 'ēog' seems to resolve as /iː/, as in 'lēogan' -> 'lie', 'flēogan' -> 'fly'
                    # On a more speculative basis, doing the same for 'ġ
                    return [Phoneme("iː", template=state.current, history=["eːog"])]
                else:
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
        # TODO: don't do this in antepenultimate syllable, as in 'aldormann'
        if state.current.is_vowel() and state.current.is_long() \
            and state.next and state.next.is_consonant() \
            and (state.next.is_geminate() \
                or (len(state.following) > 1 and state.following[1].is_consonant()) \
                or (len(state.following) > 0 and state.following[0].value == "ʃ")): # 'sċ' counts as a cluster (ex. 'flǣsċ')
                next_two_joined = "".join([x.value for x in state.following[:2]])

                # Homorganic lengthing clusters usually exempted
                # Other such clusters: mb, ld
                exempted_clusters = ["ld", "nd", "rl", "rs"] # rs+vowel?
                if not occ("PCS:rn", config):
                    exempted_clusters += ["rn"]
                if not occ("PCS:rd", config):
                    exempted_clusters += ["rd"]
                if next_two_joined in exempted_clusters \
                    or (next_two_joined == "st" and (len(state.following) == 2 or state.following[2].is_vowel())):
                    return None

                if state.current.value == "ɛː" and often("PCS:ɛː->a", config):
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

    def degemination_following_unstressed_vowel(state):
        # OED for 'after': The geminate ‑rr‑ in æfterra, which arises from the fusion of stem-final consonant ‑r 
        # with the comparative ending ‑ra (see ‑er suffix3), is simplified after the reduction of secondary stress 
        # on the medial syllable (æftera)
        # May also explain 'almesse' -> 'alms'
        if state.current.is_geminate() \
            and state.prev and state.prev.value == "ə":
            return [state.current.get_geminate_reduced()]

    def syncope_of_medial_unstressed_vowels(state):
        # Present in cases like 'ċiriċe' -> 'church'
        # OED mentions this happening after liquids, but 'almesse' -> 'alms' makes me think nasals are included

        # TODO: Figure out if we need "medial_ə_syncope" hinge
        # If so, OED suggests it should be often before consant cluster, occasional as medial vowel ('church' vs 'world' entries)

        if state.current.value == "ə" \
            and state.syllable_data.prev_vowel and state.syllable_data.prev_vowel.is_short() \
            and state.prev and (state.prev.is_liquid() or state.prev.is_nasal()) \
            and (
                (len(state.following) >= 2 and all(phone.is_consonant() for phone in state.following[0:2]))
                or (state.next and state.next.is_geminate())
                or state.syllable_data.following_syllable_count > 0
            ):
            return []

    # 'ɣ' and 'w' (both deriving from 'g' phoneme) become 'u' following vowels
    def vocalization_of_post_vocalic_g(state):
        if state.prev and state.prev.is_vowel():
            if state.current.value == "ɣ":
                if state.prev.value == "iː" and "eːog" in state.prev.history:
                    # If we earlier resolved 'ēo' into 'iː', the 'ɣ' melds into that
                    return []
                if state.next:
                    return [Phoneme("u", template=state.current, history=["vocalized-g"])]
                else:
                    return [Phoneme("x", template=state.current)]
            elif state.current.value == "w":
                return [Phoneme("u", template=state.current)]

    # ɣ → w / C_V
    # ɣ → w / C_# (sometimes)
    # ɣ → x / C_# (other times)
    def change_of_post_consonantal_g(state):
        if state.current.value == "ɣ" and state.prev and state.prev.is_consonant():
            if state.next and state.next.is_vowel():
                return [Phoneme("w", template=state.current)]
            else:
                # TODO: Consider using history to allow forms in '-ough'? Rarer I think, but e.g. 'borough'
                value = often("G:-Cg->w/x", config)
                return [Phoneme(value, template=state.current)]

    # Formation of diphthongs involving three phonemes
    # For technical reasons, separated from those involving two
    def diphthong_formation_3(state):
        two_joined = "".join([p.value for p in state.capture[:2]])
        vowel_after = state.capture[2].is_vowel()
        
        if two_joined in ["eːj", "ij"] and vowel_after:
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
        # TODO: See whether verbs should essentially have an extra syllable here
        # Consider cases like 'beckon' vs 'beacon' – basically the same except one is a verb and has extra syllables at the end
        # for inflections etc
        if state.current.is_vowel() and state.syllable_data.following_syllable_count > 1:
            return [state.current.get_shortened()]

    # m → n / _# when unstressed
    # TODO: Look for actual examples of this? I don't think I've seen any
    def final_unstressed_m_to_n(state):
        if state.current.value == "m" and state.next == None \
            and not (state.syllable_data.prev_vowel and state.syllable_data.prev_vowel.stressed):
            return [Phoneme("n", template=state.current)]

    # Drop inflectional endings
    def drop_inflecional_endings(state):
        # Drop final 'n' in verb infinitives
        if state.current.value == "n" and state.next == None and state.current.inflectional:
            return []

        # Drop final vowels in verb endings if preceded by another vowel
        if state.current.is_vowel() and state.prev and state.prev.is_vowel() and state.current.inflectional:
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

    def distinguish_voiced_fricatives(state):
        if state.current.value in ["f", "s", "θ"] \
            and (state.prev and (state.prev.is_vowel() or state.prev.is_voiced())) \
            and (state.next and (state.next.is_vowel() or state.next.is_voiced())) \
            and not state.current.value in ["x"]:
            return [state.current.get_voiced()]

    # Insert a schwa between inconvenient final consonant clusters
    # Not referenced in my sources, but added here to handle cases like
    # 'hræfn' -> 'raven', 'fæþm' -> 'fathom', 'swealwe' -> 'swallow', etc.
    #
    # Also handles word-final metathesis in cases like 'blēddre' -> 'bladder'
    def consonant_cluster_breaking(state):
        if all(phone.is_consonant() for phone in state.capture) \
            and state.syllable_data.prev_vowel != None \
            and not (state.next and state.next.is_consonant()) \
            and not (state.capture[0].is_nasal() and state.capture[1].is_plosive()) \
            and not (state.capture[0].is_nasal() and state.capture[1].is_fricative()) \
            and not (state.capture[0].is_fricative() and state.capture[1].is_plosive()) \
            and not (state.capture[0].is_semivowel() and state.capture[1].is_fricative()) \
            and not (state.capture[0].is_semivowel() and state.capture[1].is_nasal()) \
            and not (state.capture[0].is_semivowel() and state.capture[1].is_plosive()) \
            and not (state.capture[0].is_plosive() and state.capture[1].is_plosive()) \
            and not (state.joined in ["rl", "ks"]) \
            and not (state.capture[1].value == "j"):
            return [state.capture[0], Phoneme("ə"), state.capture[1]]
    
    def d_ð_alternation(state):
        if state.joined == "dər" and often("DThA:dər->ðər", config):
            return [Phoneme("ð", state.capture[0]), state.capture[1], state.capture[2]]
        elif state.joined in ["ðər", "ðən"] and occ("DThA:ðe->de", config):
            return [Phoneme("d" , state.capture[0]), state.capture[1], state.capture[2]]
    
    def shorten_o_before_dðer(state):
        if state.current.value == "oː" \
            and len(state.following) >= 3 \
            and "".join(x.value for x in state.following[:3]) in ["dər", "ðər"]:
            return [Phoneme("o" , state.capture[0])]

    # Forced metathesis between 'r' and neighboring vowels
    # 'r' and a neighboring vowel often switch places within OE: e.g.: 'brid'/'bird', 'fyrht'/'fryht', 'byrht', 'bright'
    # We see at least some cases of both (e.g. 'bird' vs 'bride'). However, in some cases we may want to force the
    # change one way or the other to prevent unfelicitous modern forms, such as *'birght' instead of 'bright'.
    def rV_metathesis(state):
        if len(state.following) > 0 and state.capture[1].is_vowel() and state.capture[2].value == "r" and state.capture[3].value == "x":
            return [state.capture[0], state.capture[2], state.capture[1], state.capture[3]]

    # Miscellaneous assimilation cases
    # These may need to be split up later if there are conflicts in timing
    def misc_assimilation(state):
        if state.joined == "ln":
            # Cases like 'miln' -> 'mill', and the pronunciation of 'kiln'
            return [Phoneme("l", template=state.capture[0])]
        elif state.joined == "ds":
            # Cases like 'god-sibb' -> 'gossip', 'gōdspel' -> 'gospel'
            if state.next and state.next.is_consonant():
                return [Phoneme("s", template=state.capture[0])]
            else:
                return [Phoneme("ss", template=state.capture[0])]
        elif state.joined in ["xθ", "xð"]:
            # Only known case is 'fyrhþ' -> 'fryhþ' -> 'frith''
            # Must occur before 'breaking'
            return [state.capture[1]]

    # Cases of reanalysis
    # TODO: Consider plural reanalysis dropping other final 's's
    # TODO: Add loss of initial 'n' as in 'nadder' -> 'adder', 'napron' -> 'apron'
    def reanalysis(state):
        if state.current.value in ["s", "z"] and state.current.derivational == "els":
            # Words with the 'els' suffix (e.g. 'smyrels', 'rǣdels') are interpreted as plurals and lose their 's'
            return []

    # ===========================================================================================================

    if config.verbose:
        print("/" + "".join(p.value for p in rig.phonemes) + "/" + config.separator)

    # Early consonant distinctions
    rig.run_capture(harden_g, 1, "Harden g's", config)
    rig.run_capture(cg_distinction, 1, "Distinguish cg's", config)

    # Early vowel changes
    rig.run_capture(homorganic_lengthening, 3, "Homorganic lengthening", config)
    rig.run_capture(pre_three_cluster_shortening, 1, "Pre-cluster shortening", config)
    rig.run_capture(stressed_vowel_changes, 1, "Stressed vowel changes", config)
    rig.run_capture(reduction_of_unstressed_vowels, 1, "Reduction of unstressed vowels", config)

    # More particular vowel and vowel-adjacent changes
    rig.run_capture(degemination_following_unstressed_vowel, 1, "Degemination following unstressed vowels", config)
    rig.run_capture(syncope_of_medial_unstressed_vowels, 1, "Syncope of unstressed medial vowels", config)

    # Loss of inflectional endings, et al
    rig.run_capture(final_unstressed_m_to_n, 1, "Final unstressed m to n", config)
    rig.run_capture(drop_inflecional_endings, 1, "Drop inflectional endings", config)

    # 'g' changes 2
    rig.run_capture(vocalization_of_post_vocalic_g, 1, "Vocalization of post-vocalic ɣ", config)
    rig.run_capture(change_of_post_consonantal_g, 1, "Change of post-consonantal ɣ", config)

    # Diphthongs
    rig.run_capture(diphthong_formation_3, 3, "Diphthong formation 1", config)
    rig.run_capture(diphthong_formation_2, 2, "Diphthong formation 2", config)
    rig.run_capture(rV_metathesis, 4, "rV metathesis", config)
    rig.run_capture(misc_assimilation, 2, "Miscellaneous assimilation", config) # Timing is key!
    rig.run_capture(breaking, 2, "Breaking", config)

    # Late vowel changes
    rig.run_capture(trisyllabic_laxing, 1, "Trisyllabic laxing", config)
    rig.run_capture(open_syllable_lengthening, 1, "Open syllable lengthening", config)

    # The timing of these seems to be sensitive, but I don't fully understand it
    rig.run_capture(consonant_cluster_breaking, 2, "Break inconvenient final consonant clusters", config)
    rig.run_capture(pre_cluster_shortening, 1, "Pre-cluster shortening", config)
    
    # Later consonant changes
    rig.run_capture(distinguish_voiced_fricatives, 1, "Distinguish voiced fricatives", config)
    rig.run_capture(reduction_of_double_consonants, 1, "Reduction of double consonants", config)
    rig.run_capture(drop_initial_h, 2, "Drop initial h", config)
    
    # Assorted sound-specific changes
    rig.run_capture(d_ð_alternation, 3, "d/ð alternation", config)
    rig.run_capture(shorten_o_before_dðer, 1, "shorten ō before -[d|ð]er ", config)

    # Loss of final unstressed vowel
    rig.run_capture(loss_of_final_unstressed_vowel, 1, "Loss of final unstressed vowel", config)

    # Later sound changes
    rig.run_capture(reanalysis, 1, "Reanalysis", config)

    return rig.phonemes
