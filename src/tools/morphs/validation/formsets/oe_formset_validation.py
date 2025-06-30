import src.tools.morphs.schemas.dialects as dialects
from src.tools.morphs.validation.type_validation import Any, Dict, One_Or_More, Opt, Schema, String, ValueSet

# TODO: Evaluate different requirement based on part of speech

# Schemata =====================================

schema_head = Any([
		Schema("metaform"),
		Schema("multiform"),
	],
	custom_error="invalid form structure. Expected one-or-list of strings or schema of type 'multiform', 'metaform', or 'paradigm'"
)
schema_multiform = Dict({ "main": One_Or_More(Schema("metaform")), "alt": One_Or_More(Schema("metaform")) })
schema_metaform = Any([
	One_Or_More(Schema("paradigm-oe")),
	Dict({
		"form": One_Or_More(Schema("paradigm-oe")),
		"canon": Opt(One_Or_More(Schema("canonset"))),
		"dialect": Opt(String(ValueSet("old english dialect", dialects.old_english)))
	})
])
schema_paradigm = Any([
		String(),
		Schema("paradigm-oe-base"),
		Schema("paradigm-oe-verb")
	],
	custom_error="invalid 'paradigm' structure. Expected a schema of type 'paradigm-oe-base' or 'paradigm-oe-verb'"
)
schema_paradigm_base = Dict({
	"lemma": String(),
	"oblique": Opt(String())
})
schema_paradigm_verb = Dict({
	"infinitive": String(),
	"past": Opt(One_Or_More(String())),
	"past-participle": Opt(One_Or_More(String()))
})
schema_canonset = Dict({
	"form": One_Or_More(Schema("paradigm-mne")),
	"dialect": Opt(String(ValueSet("middle english dialect", dialects.middle_english)))
})

schemata = {
	"formset": schema_head,
	"multiform": schema_multiform,
	"metaform": schema_metaform,
	"paradigm-oe": schema_paradigm,
	"paradigm-oe-base": schema_paradigm_base,
	"paradigm-oe-verb": schema_paradigm_verb,
	"canonset": schema_canonset
}
