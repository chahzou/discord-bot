from abc import ABC, abstractmethod

from .util.util import Utility


class Module(ABC):

    def __init__(self, bot):
        self.bot = bot
    

    @property
    def cmd_arg(self):
        raise NotImplementedError
    

    @abstractmethod
    def run(self, args, message=None):
        raise NotImplementedError

    @abstractmethod
    def return_help(self, args):
        raise NotImplementedError