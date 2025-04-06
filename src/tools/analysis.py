import time

from datetime import datetime
from pathlib import Path

import src.generation.generator as generator
from src.morphs.morphothec import Morphothec

log_dir = "logs"
analysis_dir = "analysis"

def analyze(count):
    print("Analyzing...")

    analyst = Analyst()
    for i in range(0, count):
        word = generator.generate_word(Morphothec.active)
        analyst.register(word)
        print(f"Analyzed: {i}/{count}", end="\r")

    print(f"Analyzed: {count}/{count}")
    print("Analysis complete")
    analyst.print_results(log=True)

class Analyst:
    def __init__(self):
        self.total_words = 0
        self.start_time = time.time()

        self.roots_in_language = {}
        self.types_in_language = {}
        self.construction_in_language = {}

        self.verb_prefix_only = 0
        self.verb_prep_only = 0
        self.verb_both_prefixes = 0

    def register(self, word):
        # Setup

        language = word.get_origin()
        if not language in self.roots_in_language:
            self.roots_in_language[language] = 0
        if not language in self.types_in_language:
            self.types_in_language[language] = {}
        if not language in self.construction_in_language:
            self.construction_in_language[language] = {}

        word_type = word.get_type()
        root_type = None
        for morph in word.morphs:
            if morph.is_root():
                root_type = morph.get_type()

        if root_type == None:
            Logger.error("Word has no root. Keys: " + str(word.get_keys))

        # Type

        if not word_type in self.types_in_language[language]:
            self.types_in_language[language][word_type] = 0

        # Construction

        construction = "std"
        if root_type == "noun" and word.first_morph().get_type() in ["prep", "prefix"]:
            construction = "rel"
        elif root_type == "noun" and word.first_morph().get_type() in ["number"]:
            construction = "num"

        if not construction in self.construction_in_language[language]:
            self.construction_in_language[language][construction] = 0

        # Basic incrementation

        self.total_words += 1
        self.roots_in_language[language] += 1
        self.types_in_language[language][word_type] += 1
        self.construction_in_language[language][construction] += 1

        # Special cases

        # Verbs

        if word_type == "verb":
            has_prefix = False
            has_prep = False
            for morph in word.morphs:
                if morph.get_type() == "prefix":
                    has_prefix = True
                elif morph.get_type() == "prep":
                    has_prep = True

                if has_prep:
                    break

            if has_prefix and not has_prep:
                self.verb_prefix_only += 1
            elif has_prep and not has_prefix:
                self.verb_prep_only += 1
            elif has_prefix and has_prep:
                self.verb_both_prefixes += 1

    def print_results(self, log):
        global log_dir, analysis_dir

        end_time = time.time()
        minutes_elapsed = (end_time - self.start_time) / 60

        results = ""
        results += "\n"
        results += "====== ANALYSIS RESULTS ======\n"
        results += "\n"
        results += "Total words:\t" + str(self.total_words) + "\n"
        results += "Time elapsed:\t" + str(minutes_elapsed) + " min"

        results += "\n"

        results += divider_1()
        results += "Breakdown:\n"
        results += divider_1()
        for lang_key in sorted(self.roots_in_language.keys()):
            results += divider_2()
            results += "  " + lang_key + ":\t" + str(self.roots_in_language[lang_key]) + percent_string(self.roots_in_language[lang_key], self.total_words) + "\n"
            results += divider_2()

            for type_key in sorted(self.types_in_language[lang_key].keys()):
                results += "    " + type_key + ":\t" + str(self.types_in_language[lang_key][type_key]) + percent_string(self.types_in_language[lang_key][type_key], self.roots_in_language[lang_key]) + "\n"

            results += divider_2()
            for const_key in sorted(self.construction_in_language[lang_key].keys()):
                results += "    " + const_key + ":\t" + str(self.construction_in_language[lang_key][const_key]) + percent_string(self.construction_in_language[lang_key][const_key], self.roots_in_language[lang_key]) + "\n"

        results += divider_1()

        results += "\n"

        results += divider_2()
        results += "By language\n"
        results += divider_2()

        for lang_key in sorted(self.roots_in_language.keys()):
            results += "  " + lang_key + ":\t" + str(self.roots_in_language[lang_key]) + percent_string(self.roots_in_language[lang_key], self.total_words) + "\n"

        results += divider_2()
        results += "\n"

        results += divider_2()
        results += "By root type\n"
        results += divider_2()
        type_counts = {}
        for lang_key in self.roots_in_language.keys():
            for type_key in self.types_in_language[lang_key].keys():
                if not type_key in type_counts:
                    type_counts[type_key] = 0

                type_counts[type_key] += self.types_in_language[lang_key][type_key]

        for type_key in sorted(type_counts.keys()):
            results += "  " + type_key + ":  \t" + str(type_counts[type_key]) + percent_string(type_counts[type_key], self.total_words) + "\n"

        results += divider_2()
        results += "\n"

        results += divider_2()
        results += "By construction\n"
        results += divider_2()
        const_counts = {}
        for lang_key in self.roots_in_language.keys():
            for const_key in self.construction_in_language[lang_key].keys():
                if not const_key in const_counts:
                    const_counts[const_key] = 0

                const_counts[const_key] += self.construction_in_language[lang_key][const_key]

        for const_key in sorted(const_counts.keys()):
            results += "  " + const_key + ":  \t" + str(const_counts[const_key]) + percent_string(const_counts[const_key], self.total_words) + "\n"

        results += divider_2()
        results += "\n"

        results += divider_2()
        results += "Verbs\n"
        results += divider_2()

        no_prefixes = type_counts["verb"] - self.verb_prefix_only - self.verb_prep_only - self.verb_both_prefixes
        results += "  total:      \t" + str(type_counts["verb"]) + "\n"
        results += "\n"
        results += "  no prefix:  \t" + str(no_prefixes) + percent_string(no_prefixes, type_counts["verb"]) + "\n"
        results += "  prefix only:\t" + str(self.verb_prefix_only) + percent_string(self.verb_prefix_only, type_counts["verb"]) + "\n"
        results += "  prep only:  \t" + str(self.verb_prep_only) + percent_string(self.verb_prep_only, type_counts["verb"]) + "\n"
        results += "  both:       \t" + str(self.verb_both_prefixes) + percent_string(self.verb_both_prefixes, type_counts["verb"]) + "\n"
        results += "\n"
        results += "  has prefix:\t" + str(self.verb_prefix_only + self.verb_both_prefixes) + percent_string(self.verb_prefix_only + self.verb_both_prefixes, type_counts["verb"]) + "\n"
        results += "  has prep:\t" + str(self.verb_prep_only + self.verb_both_prefixes) + percent_string(self.verb_prep_only + self.verb_both_prefixes, type_counts["verb"]) + "\n"

        results += divider_2()
        results += "\n"

        # Output

        print(results)

        if log:
            filename = str(datetime.now()) + ".txt"
            Path(log_dir).mkdir(exist_ok=True)
            Path(log_dir + "/" + analysis_dir).mkdir(exist_ok=True)
            Path(log_dir + "/" + analysis_dir + "/" + filename).touch()
            file = open(log_dir + "/" + analysis_dir + "/" + filename, "w")
            file.write(results)
            file.close()

# Helpers =============

def divider_1():
    return "=================================\n"

def divider_2():
    return "---------------------------------\n"

def percent_string(numerator, denominator):
     return "\t" + str(round((numerator / denominator) * 100, 2)) + "%"