import random

class Config:
    def __init__(self, locked=False, overrides=[], verbose=False, separator="\n", seed=None):
        self.locked = locked
        self.overrides = overrides
        self.verbose = verbose
        self.separator = separator
        if seed == None:
            seed = random.randint(0, 999999)
        self.seed = seed
