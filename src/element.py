from abc import ABC

from env import AbstractElement, Env

class Element(AbstractElement, ABC):
    def __init__(self, env: Env):
        self.env = env
