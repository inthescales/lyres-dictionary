class Environment:
    def __init__(self, anteprev, prev, next, postnext, object_specified=False):
        self.anteprev = anteprev
        self.prev = prev
        self.next = next
        self.postnext = postnext
        
        self.object_specified = object_specified

    def is_initial(self):
        return self.prev == None

    def is_final(self):
        return self.next == None

    def prev_env(self, morph):
        return Environment(None, self.anteprev, morph, None)

    def next_env(self, morph):
        return Environment(None, morph, self.postnext, None )
