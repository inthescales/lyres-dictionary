from random import Random

def always(id, config):
    return hinge(id, 1.00, config)

def often(id, config):
    return hinge(id, 0.75, config) 

def even(id, config):
    return hinge(id, 0.5, config)

def occ(id, config):
    return hinge(id, 0.25, config)

def never(id, config):
    return hinge(id, 0.00, config)

# TODO: consider making this object a member of config
random = None

def hinge(id, odds, config):
    global random

    # Format: [[options], default]
    # First option should represent a change occurring, when applicable
    points = {
        "HL:ld-front": [[True, False], True],
        "HL:mb": [[True, False], False],
        "HL:ng": [[True, False], True],
        "SVC:eːr->ɛːr": [[True, False], True],
        "SVC:eːc->ic": [[True, False], True],
        "SVC:eːo->eː/oː": [["eː", "oː"], "eː"],
        "SVC:y->i/e/u": [["i", "e", "u"], "i"],
        "PCS:rd": [[True, False], True],
        "PCS:rn": [[True, False], True],
        "PCS:ɛː->a": [[True, False], True],
        "OSL:iy": [[True, False], False],
        "OSL:u": [[True, False], False],
        "DThA:dər->ðər": [[True, False], True],
        "DThA:ðe->de": [[True, False], False],
        "G:-Cg->w/x": [["w", "x"], "w"],
        "medial_ə_syncope": [[True, False], True],
        "Orth:aiV->ai/ay": [["ai", "ay"], "ai"],
        "Orth:ɛ/iu->ew/ue": [["ew", "ue"], "ew"],
        "Orth:e+r->e/a/ea": [["ea", "e", "a"], "ea"],
        "Orth:ɛː->ea/eCV": [["ea", "eCV"], "ea"],
        "Orth:iː#->ie/ye": [["ie", "ye"], "ie"],
        "Orth:ɔː->oa/oCV": [["oa", "oCV"], "oa"],
        "Orth:uːn->ow/ou": [["ow", "ou"], "ow"],
        "Orth:uːr->ou/owe": [["ou", "owe"], "ou"],
        "PPart:use-strong": [[True, False], True],
        "PPart:use-class-3-suffix": [[True, False], False],
        "PPart:contract-weak": [[True, False], True],
        "PPart:verners-law": [[True, False], False]
    }

    if not random:
        random = Random(config.seed)

    if not id in points:
        print("error: override id '" + str(id) + "' not recognized")

    override = next((pair for pair in config.overrides if pair[0] == id), None)
    if override:
        return override[1]
    
    options = points[id][0]
    default = points[id][1]

    if config.locked:
        return default
    
    if type(odds) == float:
        if random.uniform(0.0, 1.0) < odds:
            return options[0]
        else:
            return options[1]
    elif type(odds) == list:
        if len(odds) == len(options):
            print("error: list odds has incorrect length")
        else:
            for i in range(0, len(odds)):
                if random.uniform(0.0, 1.0) < odds[i]:
                    return options[i]
            
            return options[-1]
    else:
        print("error: odds type '" + type(odds) + "' not supported")
