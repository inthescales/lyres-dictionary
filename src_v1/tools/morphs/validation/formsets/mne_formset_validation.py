from src.tools.morphs.validation.type_validation import Any, Dict, One_Or_More, Opt, Schema, String

schema_paradigm = Any(
    [
        One_Or_More(String()),
        Schema("paradigm-mne-noun"),
        Schema("paradigm-mne-adj"),
        Schema("paradigm-mne-verb"),
    ],
    custom_error="invalid 'paradigm-mne' structure. Expected a schema of type 'paradigm-mne-noun', 'paradigm-mne-adj', or 'paradigm-mne-verb'"
)
schema_paradigm_noun = Dict({
    "lemma": String(),
    "plural": Opt(String())
})
schema_paradigm_adj = Dict({
    "lemma": String(),
    "comparative": Opt(String()),
    "superlative": Opt(String())
})
schema_paradigm_verb = Dict({
    "lemma": String(),
    "past": Opt(One_Or_More(String())),
    "past-participle": Opt(One_Or_More(String()))
})

schemata = {
    "paradigm-mne": schema_paradigm,
    "paradigm-mne-noun": schema_paradigm_noun,
    "paradigm-mne-adj": schema_paradigm_adj,
    "paradigm-mne-verb": schema_paradigm_verb
}
