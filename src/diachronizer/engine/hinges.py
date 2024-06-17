from random import Random

def often(id, config):
    return hinge(id, 0.75, config) 

def even(id, config):
    return hinge(id, 0.5, config)

def occ(id, config):
    return hinge(id, 0.25, config)

# TODO: consider making this object a member of config
random = None

def hinge(id, odds, config):
    global random

    points = {
        "HL:ng": [True, False],
        "SVC:eːr->ɛːr": [True, False],
        "SVC:eːc->ic": [True, False],
        "SVC:eːo->eː/oː": ["eː", "oː"],
        "SVC:y->i/e/u": ["i", "e", "u"],
        "PCS:rd": [True, False],
        "PCS:rn": [True, False],
        "PCS:ɛː->a": [True, False],
        "OSL:iy": [False, True],
        "OSL:u": [False, True],
        "DThA:dər->ðər": [True, False],
        "DThA:ðər->dər": [False, True],
        "G:-Cg->w/x": ["w", "x"],
        "Orth:aiV->ai/ay": ["ai", "ay"],
        "Orth:ɛ/iu->ew/ue": ["ew", "ue"],
        "Orth:e+r->e/a/ea": ["ea", "e", "a"],
        "Orth:ɛː->ea/eCV": ["ea", "eCV"],
        "Orth:iː#->ie/ye": ["ie", "ye"],
        "Orth:ɔː->oa/oCV": ["oa", "oCV"],
        "Orth:ə->o": [True, False]
    }

    if not random:
        random = Random(config.seed)

    if not id in points:
        print("error: override id '" + str(id) + "' not recognized")

    override = next((pair for pair in config.overrides if pair[0] == id), None)
    if override:
        return override[1]
    
    if config.locked:
        return points[id][0]
    
    if type(odds) == float:
        if random.uniform(0.0, 1.0) < odds:
            return points[id][0]
        else:
            return points[id][1]
    elif type(odds) == list:
        choices = points[id]
        if len(odds) == len(choices):
            print("error: list odds has incorrect length")
        else:
            for i in range(0, len(odds)):
                if random.uniform(0.0, 1.0) < odds[i]:
                    return choices[i]
            
            return choices[-1]
    else:
        print("error: odds type '" + type(odds) + "' not supported")
