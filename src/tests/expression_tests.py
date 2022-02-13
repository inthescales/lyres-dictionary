import unittest

from src.expressions import evaluate_expression

test_morphs = {
    "nuntiare": { "key": "nuntiare", "link-present": "nuntia", "link-perfect": "nunciat", "final": "nounce", "type": "verb", "conjugation": 1, "gloss": "report", "tags": ["transitive"], "origin": "latin", "form": "nuntiat", "final": False },
    "audire": { "key": "audire", "link-present": "audi", "link-perfect": "audit", "final": "audit", "type": "verb", "conjugation": 4, "gloss": "hear", "tags": ["transitive"], "origin": "latin", "form": "audit", "final": False },
    "cancer": { "key": "cancer", "link": "cancr", "type": "noun", "declension": 2, "gloss": "crab", "tags": ["count", "concrete", "living", "animal"], "origin": "latin", "form": "cancr", "final": False },
    "lumen": { "key": "lumen", "link": "lumin", "type": "noun", "declension": 3, "gloss": "lamp", "tags": ["count", "concrete", "tool"], "origin": "latin", "form": "lumin", "Final": False },
    "stella": { "key": "stella", "link": "stell", "type": "noun", "declension": 1, "gloss": "star", "tags": ["count", "concrete"], "origin": "latin", "form": "stell", "final": False },
    "volumen": { "key": "volumen", "link": "volumin", "type": "noun", "declension": 3, "gloss": "volume", "tags": ["mass", "abstract"], "origin": "latin", "form": "volumin", "final" : False},
    "columna": { "key": "columna", "link": "column", "type": "noun", "declension": 1, "gloss": "column", "tags": ["count", "concrete"], "origin": "latin", "form": "column", "final": False },

    "arktos": { "key": "arktos", "link": "arct", "type": "noun", "gloss": "bear", "tags": ["count", "concrete", "living", "animal"], "origin": "greek", "form": "arct", "final": False },
    "enigma": { "key": "enigma", "link": "enigmat", "type": "noun", "gloss": "riddle", "tags": ["count", "abstract"], "origin": "greek", "form": "enigmat", "final": False },
    "ic":     { "key": "ic", "final": "ic", "link": "ic", "type": "derive", "derive-from": "noun", "derive-to": "adj", "suffixes": [], "gloss": "pertaining to %pl", "tags": ["final"], "origin": "greek", "form": "ic", "final": True }
}


class ExpressionTests(unittest.TestCase):
    
    def testProperties(self):

        # Simple properties
        self.assertTrue(evaluate_expression({'has-key': 'enigma'}, test_morphs["enigma"]))
        self.assertFalse(evaluate_expression({'has-key': 'arktos'}, test_morphs["enigma"]))
        self.assertTrue(evaluate_expression({'has-key': ['enigma', 'arktos']}, test_morphs["enigma"]))

        self.assertTrue(evaluate_expression({'has-type': 'noun'}, test_morphs["arktos"]))
        self.assertFalse(evaluate_expression({'has-type': 'verb'}, test_morphs["arktos"]))
        self.assertTrue(evaluate_expression({'has-type': ['noun', 'verb']}, test_morphs["arktos"]))
        self.assertTrue(evaluate_expression({'has-type': 'adj'}, test_morphs["ic"]))
        self.assertFalse(evaluate_expression({'has-type': 'noun'}, test_morphs["ic"]))
        self.assertFalse(evaluate_expression({'has-type': 'derive'}, test_morphs["ic"]))
        self.assertTrue(evaluate_expression({'has-type': ['adj', 'noun', 'derive']}, test_morphs["ic"]))

        self.assertTrue(evaluate_expression({'has-tag': 'count'}, test_morphs["enigma"]))
        self.assertFalse(evaluate_expression({'has-tag': 'non-final'}, test_morphs["enigma"]))

        self.assertTrue(evaluate_expression({'has-conjugation': 1}, test_morphs["nuntiare"]))
        self.assertFalse(evaluate_expression({'has-conjugation': 3}, test_morphs["nuntiare"]))
        self.assertTrue(evaluate_expression({'has-conjugation': 4}, test_morphs["audire"]))
        self.assertFalse(evaluate_expression({'has-conjugation': 1}, test_morphs["audire"]))
        self.assertTrue(evaluate_expression({'has-conjugation': [1, 4]}, test_morphs["audire"]))
        self.assertFalse(evaluate_expression({'has-conjugation': [2, 3]}, test_morphs["audire"]))

        self.assertTrue(evaluate_expression({'has-declension': 2}, test_morphs["cancer"]))
        self.assertFalse(evaluate_expression({'has-declension': 3}, test_morphs["cancer"]))
        self.assertTrue(evaluate_expression({'has-declension': 3}, test_morphs["lumen"]))
        self.assertFalse(evaluate_expression({'has-declension': [1, 4]}, test_morphs["lumen"]))
        self.assertTrue(evaluate_expression({'has-declension': [2, 3]}, test_morphs["cancer"]))

        self.assertTrue(evaluate_expression({'is-root': True}, test_morphs["cancer"]))
        self.assertFalse(evaluate_expression({'is-root': False}, test_morphs["cancer"]))
        self.assertTrue(evaluate_expression({'is-root': True}, test_morphs["audire"]))
        self.assertFalse(evaluate_expression({'is-root': False}, test_morphs["audire"]))
        self.assertTrue(evaluate_expression({'is-root': False}, test_morphs["ic"]))
        self.assertFalse(evaluate_expression({'is-root': True}, test_morphs["ic"]))

        # Compound properties
        self.assertTrue(evaluate_expression({'has-all-tags': ["count"]}, test_morphs["arktos"]))
        self.assertTrue(evaluate_expression({'has-all-tags': ["count", "concrete", "living"]}, test_morphs["arktos"]))
        self.assertFalse(evaluate_expression({'has-all-tags': ["count", "concrete", "living", "plant"]}, test_morphs["arktos"]))
        self.assertFalse(evaluate_expression({'has-all-tags': ["mass", "abstract"]}, test_morphs["arktos"]))

        self.assertTrue(evaluate_expression({'has-any-tags': ["count"]}, test_morphs["arktos"]))
        self.assertTrue(evaluate_expression({'has-any-tags': ["count", "concrete"]}, test_morphs["arktos"]))
        self.assertTrue(evaluate_expression({'has-any-tags': ["animal", "plant"]}, test_morphs["arktos"]))
        self.assertFalse(evaluate_expression({'has-any-tags': ["plant"]}, test_morphs["arktos"]))
        self.assertFalse(evaluate_expression({'has-any-tags': ["plant", "terrain"]}, test_morphs["arktos"]))

        # Form properties
        self.assertTrue(evaluate_expression({'has-prefix': "i"}, test_morphs["ic"]))
        self.assertFalse(evaluate_expression({'has-prefix': "o"}, test_morphs["ic"]))
        self.assertTrue(evaluate_expression({'has-prefix': ["i", "o"]}, test_morphs["ic"]))
        self.assertTrue(evaluate_expression({'has-prefix': "ic"}, test_morphs["ic"]))

        self.assertTrue(evaluate_expression({'has-suffix': "c"}, test_morphs["ic"]))
        self.assertFalse(evaluate_expression({'has-suffix': "y"}, test_morphs["ic"]))
        self.assertTrue(evaluate_expression({'has-suffix': ["c", "y"]}, test_morphs["ic"]))
        self.assertTrue(evaluate_expression({'has-suffix': "ic"}, test_morphs["ic"]))

        self.assertTrue(evaluate_expression({'even-syllables': True }, test_morphs["lumen"]))
        self.assertFalse(evaluate_expression({'even-syllables': False }, test_morphs["lumen"]))
        self.assertTrue(evaluate_expression({'odd-syllables': True }, test_morphs["arktos"]))
        self.assertFalse(evaluate_expression({'odd-syllables': False }, test_morphs["arktos"]))
        self.assertTrue(evaluate_expression({'odd-syllables': True }, test_morphs["enigma"]))
        self.assertFalse(evaluate_expression({'odd-syllables': False }, test_morphs["enigma"]))

        self.assertTrue(evaluate_expression({'final-or-semifinal-l': True }, test_morphs["stella"]))
        self.assertTrue(evaluate_expression({'final-or-semifinal-l': True }, test_morphs["columna"]))
        self.assertTrue(evaluate_expression({'final-or-semifinal-l': False }, test_morphs["cancer"]))
        self.assertTrue(evaluate_expression({'final-or-semifinal-l': False }, test_morphs["volumen"]))

        # Contextual properties
        self.assertTrue(evaluate_expression({'is-final': False}, test_morphs["arktos"]))
        self.assertFalse(evaluate_expression({'is-final': True}, test_morphs["arktos"]))
        self.assertTrue(evaluate_expression({'is-final': True}, test_morphs["ic"]))
        self.assertFalse(evaluate_expression({'is-final': False}, test_morphs["ic"]))

    def testOperators(self):

        self.assertTrue(evaluate_expression({'and': [{'has-key': 'enigma'}, {'is-root': True }]}, test_morphs["enigma"]))
        self.assertFalse(evaluate_expression({'and': [{'has-key': 'enigma'}, {'is-root': False }]}, test_morphs["enigma"]))
        self.assertFalse(evaluate_expression({'and': [{'has-key': 'cancer'}, {'is-root': True }]}, test_morphs["enigma"]))
        self.assertFalse(evaluate_expression({'and': [{'has-key': 'cancer'}, {'is-root': False }]}, test_morphs["enigma"]))
        self.assertTrue(evaluate_expression({'and': [{'has-key': 'enigma'}, {'is-root': True }, {'has-tag': "count"}]}, test_morphs["enigma"]))
        self.assertFalse(evaluate_expression({'and': [{'has-key': 'enigma'}, {'is-root': True }, {'has-tag': "living"}]}, test_morphs["enigma"]))

        self.assertTrue(evaluate_expression({'or': [{'has-key': 'enigma'}, {'is-root': True }]}, test_morphs["enigma"]))
        self.assertTrue(evaluate_expression({'or': [{'has-key': 'enigma'}, {'is-root': False }]}, test_morphs["enigma"]))
        self.assertTrue(evaluate_expression({'or': [{'has-key': 'cancer'}, {'is-root': True }]}, test_morphs["enigma"]))
        self.assertFalse(evaluate_expression({'or': [{'has-key': 'cancer'}, {'is-root': False }]}, test_morphs["enigma"]))
        self.assertTrue(evaluate_expression({'and': [{'has-key': 'enigma'}, {'is-root': True }, {'has-tag': "count"}]}, test_morphs["enigma"]))
        self.assertFalse(evaluate_expression({'and': [{'has-key': 'cancer'}, {'is-root': False }, {'has-tag': "living"}]}, test_morphs["enigma"]))

        self.assertFalse(evaluate_expression({'not': {'has-key': 'enigma'}}, test_morphs["enigma"]))
        self.assertTrue(evaluate_expression({'not': {'has-tag': 'living'}}, test_morphs["enigma"]))
        self.assertTrue(evaluate_expression({'not': {'not': {'has-tag': 'count'}}}, test_morphs["enigma"]))

if __name__ == '__main__':    
    unittest.main()