class Config:
    def __init__(self, locked=False, overrides=[], verbose=False, separator="\n"):
        self.locked = locked
        self.overrides = overrides
        self.verbose = verbose
        self.separator = separator
