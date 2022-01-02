class Environment:
    def __init__(self, anteprev, prev, next):
        self.anteprev = anteprev
        self.prev = prev
        self.next = next

    def is_initial(self):
        return self.prev == None

    def is_final(self):
        return self.next == None
