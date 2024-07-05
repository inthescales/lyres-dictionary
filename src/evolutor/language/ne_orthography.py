from random import Random

from src.evolutor.engine.hinges import often, even, occ, hinge

def from_me_phonemes(phonemes, config):
    random = Random(config.seed)
    result = []
    insert_lengthening_e = False
    would_have_inserted_lengthening_e = False

    skip_next = 0

    last_stressed_vowel = None

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

        is_vowel_open = phone.is_vowel() and next1 and next2 and next1.is_consonant() and next2.is_vowel()
        precedes_lengthening_cluster = phone.is_vowel() and next1 and next2 and next1.value + next2.value in ["ld", "mb", "nd", "ng", "rl", "rn"] # Excludes 'rd'

        if insert_lengthening_e and phone.is_vowel():
            insert_lengthening_e = False
            would_have_inserted_lengthening_e = True

        # Diphthongs ----------------------------

        if phone.value == "uː" and "vocalized-g" in phone.history:
            result += random.choice(["ow", "ough"])
        elif next1 and phone.value + next1.value == "aux":
            result += "augh"
            skip_next = True
        elif next1 and phone.value + next1.value == "ɛix":
            result += "aigh"
            skip_next = True
        elif next1 and phone.value + next1.value == "iːx":
            result += "igh"
            skip_next = True
        elif next1 and phone.value + next1.value == "ɔux":
            result += "ough"
            skip_next = True
        elif next1 and phone.value + next1.value == "uːx":
            result += "ough"
            skip_next = True
        elif phone.value == "ai":
            if not next1:
                result += "ay"
            elif next1 and next1.is_vowel():
                choice = even("Orth:aiV->ai/ay", config)
                if choice == "ai":
                    result += "ai"
                    skip_next = True
                elif choice == "ay":
                    result += "ay"
            else:
                result += "ai"
        elif phone.value == "au":
            result += "aw"
        elif phone.value in ["ɛu", "iu"]:
            override = next((x[1] for x in config.overrides if x[0] == "Orth:ɛ/iu->ew/ue"), None)
            if override == "ew":
                result += "ew"
            elif override == "ue":
                result += "ue"
            else:
                choices = ["ue"]
                if next1:
                    choices += ["u"]
                if result[-1] != "c":
                    choices += ["ew"]

                result += random.choice(choices)
            
            if next1 and next1.value == "ə":
                skip_next = True
        elif phone.value == "ɔu":
            if next1 and next1.is_consonant() and next1.value != "n":
                # Added based on pairs such as 'sāwol'->'soul'/'flogen'->'flown'
                result += "ou"
            else:
                result += "ow"
            
            if next1 and next1.value == "ə":
                skip_next = True

        # Monophthongs --------------------------

        elif phone.value == "a":
            result += "a"
        elif phone.value == "aː":
            result += "a"
            if next1 and not (next1.is_geminate() or (next2 and next2.is_consonant()) or next1.value in ["ʃ"]):
                insert_lengthening_e = True
        elif phone.value == "e":
            if next1 and next1.value == "r":
                # These cases seem ambiguous. 
                # "ea" may be more common when descending from "eo" spelling?
                roll = hinge("Orth:e+r->e/a/ea", [0.5, 0.3], config)
                if roll == "ea":
                    result += "ea"
                elif roll == "a":
                    result += "a"
                elif roll == "e":
                    result += "e"
            else:
                result += "e"
        elif phone.value == "ɛ":
            result += "e"
        elif phone.value == "ɛː":
            roll = often("Orth:ɛː->ea/eCV", config)
            if roll == "ea":
                result += "ea"
            elif roll == "eCV":
                result += "e"
                insert_lengthening_e = True
        elif phone.value == "i":
            if next1:
                result += "i"
            else:
                result += "y"
        elif phone.value == "iː" and next1 and next1.is_consonant() and next2 and next2.is_consonant():
            # TODO: Handle the case of 'weird'
            result += "i"
        elif phone.value == "iː":
            if next1:
                result += "i"
                insert_lengthening_e = True
            else:
                if (prev and prev2 and prev.is_consonant() and prev2.is_consonant()) \
                    or (prev and prev.is_consonant() and prev.is_geminate()) \
                    or (not phone.stressed):
                    result += "y"
                else:
                    result += even("Orth:iː#->ie/ye", config)
        elif phone.value == "eː" and next1 and next2 and next1.value + next2.value in ["nd", "ld"]:
            result += "ie"
        elif phone.value == "eː":
            result += "ee"
        elif phone.value == "o":
            result += "o"
        elif phone.value == "ɔ":
            result += "o"
        elif phone.value == "ɔː":
            if precedes_lengthening_cluster:
                # Homorganic lengthening clusters don't take digraphs (usually)
                result += "o"
            elif is_vowel_open:
                # Open syllables don't need a digraph or an inserted vowel (but add one for schwa resolution)
                result += "o"
                insert_lengthening_e = True
            elif next1 != None and next2 == None and next1.is_consonant() and next1.is_voiced() and next1.is_fricative():
                # Words ending in voiced fricatives must have silent e
                result += "o"
                insert_lengthening_e = True
            else:
                roll = often("Orth:ɔː->oa/oCV", config)
                if roll == "oa":
                    result += "oa"
                elif roll == "oCV":
                    result += "o"
                    insert_lengthening_e = True

        elif phone.value == "oː":
            result += "oo"
        elif phone.value == "u" and prev and prev.value == "w" and next1 and next1.value == "r":
            result += "o"
        elif phone.value == "u" and next1 and next1.value == "r":
            result += "u"
        elif phone.value == "u" and next1 and next1.value == "v":
            result += "o"
            insert_lengthening_e = True
        elif phone.value == "u":
            result += "u"
        elif phone.value == "uː":
            if next1:
                if next1.value == "n":
                    # 'town', 'down' 'brown' vs 'roun'
                    # Note that some archaic past participle forms may use 'owe': 'untowen', 'ygrowen', 'thowen'
                    choice = often("Orth:uːn->ow/ou", config)
                    result += choice
                elif next1.value == "r":
                    # 'bower', 'shower' vs 'our', 'sour'
                    choice = even("Orth:uːr->ou/owe", config)
                    result += choice
                else:
                    result += "ou"
            else:
                result += "ow"
        elif phone.value == "ə":
            if not next2:
                if next1.value in ["m", "n", "w"] \
                    and prev and prev.value != "v" \
                    and not would_have_inserted_lengthening_e \
                    and ( \
                        result[-1] == "c" # Never use 'e' following a 'c'
                        or next1.value not in ["n"] # Only 'n' endings are subject to the hinge below
                        or often("Orth:ə->o", config)
                    ):
                    # Words ending in 'm', 'n', or 'w' usually take 'o'
                    result += "o"
                elif next1.value == "k":
                    # As in 'garlic'. But need to consider '-ock' cases as well.
                    result += "i"
                elif next1.value == "l" \
                    and prev and prev.value == "v" \
                    and prev2 and (prev2.value in ["ɛː", "eː"] or prev2.is_consonant()):
                    # Vowel check by analogy with 'evil', 'devil', 'anvil', 'chervil'
                    result += "i"
                else:
                    result += "e"
            else:
                result += "e"

        # Consonants
        elif phone.value == "f":
            if next1 \
                or (prev and prev.is_consonant()) \
                or (prev and prev.is_vowel() and prev.is_long()):
                result += "f"
            else:
                result += "ff"
        elif phone.value == "l":
            if next1 != None \
                or (prev and prev.is_vowel() and prev.is_long()) \
                or (prev and prev.is_consonant()):
                result += "l"
            elif not next1 and prev and prev.value == "ə" \
                and prev2 and prev2.is_consonant() \
                and not prev2.value in ["dʒ", "v", "ð", "z"]:
                result = result[:-1] + ["le"]
            elif prev.is_vowel() and (not prev.stressed or prev.is_diphthong()):
                result += "l"
            else:
                result += "ll"
        elif phone.value == "s":
            if next1:
                if next1.value == "c":
                    result += "sh"
                    skip_next = True
                else:
                    result += "s"
            else:
                if prev and prev.is_vowel() and prev.is_short():
                    result += "ss"
                elif prev and prev.value == "r":
                    result += "se"
                elif prev and prev.value == "iː":
                    result += "c"
                elif prev and prev.is_vowel() and prev.is_long() and not insert_lengthening_e:
                    result += "se"
                else:
                    result += "s"
        elif phone.value == "z":
            if not next1 and prev and prev.value == "r":
                result += "se"
            elif prev and prev.is_vowel() and ((prev.is_long() and not prev.value == "aː") or prev.value == "u"):
                # 'aː' condition added to handle 'hazel' (fits with daze too)
                # 'u' condition added to handle 'busy' / 'dizzy'
                # Need more cases to establish a pattern more clearly
                result += "s"
            elif next1 and next2 and "".join([p.value for p in [next1, next2]]) == "əj":
                # Handles cases like 'dizzy'
                result += "z"
            else:
                result += "s"
        elif phone.value in ["θ", "ð"]:
            if prev and prev.value == "x":
                # Added to handle cases like 'drought', on the belief that no cases of '-oughth' exist
                result += "t"
            else:
                result += "th"
        elif phone.value in ["x", "xx"]:
            if prev == None:
                result += "h"
            else:
                result += "gh"
        elif phone.value == "k":
            if not next1 and prev and prev.is_vowel() and prev.is_short():
                # Doubled form after a short vowel
                result += "ck"
            elif next1 and next1.value == "w":
                # 'qu' when followed by a /w/
                result += "qu"
                skip_next = True
            elif (not prev or prev.is_vowel()) \
                and next1 \
                and next1.value != "n" \
                and not next1.value in ["ɛ", "e", "i", "ɛː", "eː", "iː"] \
                and not insert_lengthening_e:
                # 'c' when not followed by a /e/ or /e/
                result += "c"
            else:
                result += "k"
        elif phone.value == "kw":
            result += "qu"
        elif phone.value == "ks":
            result += "x"
            skip_next = True
        elif phone.value == "ʃ":
            result += "sh"
        elif phone.value == "tʃ":
            if not next1 and prev and prev.is_vowel() and prev.is_short():
                result += "tch"
            else:
                result += "ch"
        elif phone.value == "dʒ":
            if prev == None:
                result += "j"
            else:
                result += "dg"
                if next1 == None:
                    result += "e"
        elif phone.value == "w":
            if prev and prev.value == "x" and not prev2:
                result = "wh" 
            else:
                result += "w"
        elif phone.value == "j":
            if prev and prev.value == "ə":
                result = result[:-1]
            result += "y"
        elif phone.value == "y":
            result += "u"
        else:
            result += phone.value

        # Various word-end adjustments
        if phone.is_consonant() and insert_lengthening_e and (not next1 or not next1.is_vowel()):
            # Insert lengthening 'e'
            result += "e"
            insert_lengthening_e = False
        elif phone.is_consonant() and not phone.is_geminate() \
            and prev and prev.is_vowel() and prev.is_short() \
            and next1 and next1.is_vowel() \
            and phone.value not in ["v", "j", "θ", "ð", "ʃ", "dʒ"]:
            # Double non-final consonant after short vowel
            if phone.value == "k":
                result = result[:-1] + ["ck"]
            elif not (phone.value == "z" and len(result) and result[-1] == "s"):
                result += result[-1]
        elif not next1 and result[-1] != "e" \
            and (phone.value == "v" \
            or (phone.value == "z" and not (prev and prev.is_nasal()))):
            # Certain voiced fricatives ('v', 's' as /z/) shouldn't end a word
            # One exception is nasal + /z/, as in 'alms'
            result += "e"
        
        if phone.is_vowel() and phone.stressed:
            last_stressed_vowel = phone

        would_have_inserted_lengthening_e = False
        
    return "".join(result)
