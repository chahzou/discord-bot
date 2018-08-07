from abc import ABC, abstractmethod
from .util.util import Utility

class Module(ABC):

    def __init__(self, bot):
        self.bot = bot

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def return_help(self):
        pass