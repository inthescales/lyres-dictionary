class Environment:
    def __init__(self, anteprev, prev, next, postnext):
        self.anteprev = anteprev
        self.prev = prev
        self.next = next
        self.postnext = postnext

    def is_initial(self):
        return self.prev == None

    def is_final(self):
        return self.next == None

    def prev_env(self, morph):
        return Environment(None, self.anteprev, morph, None)

    def next_env(self, morph):
        return Environment(None, morph, self.postnext, None )
