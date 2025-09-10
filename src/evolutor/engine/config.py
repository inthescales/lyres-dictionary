import copy
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

    # Helpers ==========================

    # Inserts the new override in the list. 'overwrite' determines whether to overwrite
    # an existing override for the same hinge, or to return without adding if there is one.
    def add_override(self, new_over, overwrite=False):
        # Get index of any existing override for this hinge
        index = None
        for i in range(0, len(self.overrides)):
            if self.overrides[i][0] == new_over[0]:
                index = i

        if index == None:
            self.overrides.append(new_over)
        else:
            if overwrite:
                del self.overrides[index]
                self.overrides.append(new_over)
            else:
                return

    # Add multiple overrides
    def add_overrides(self, new_overrides, overwrite=False):
        for over in new_overrides:
            self.add_override(over, overwrite=overwrite)

    # Creates and returns a copy of the config object with the added overrides.
    def copy_with_overrides(self, new_overrides, overwrite=False):
        new_config = copy.deepcopy(self)
        new_config.add_overrides(new_overrides)
        return new_config
