import random

class Config:
    def __init__(self, locked=False, overrides=[], i_mutation=False, verbose=False, separator="\n", seed=None):
        self.locked = locked
        self.overrides = overrides
        self.i_mutation = i_mutation
        self.verbose = verbose
        self.separator = separator
        if seed == None:
            seed = random.randint(0, 999999)
        self.seed = seed
