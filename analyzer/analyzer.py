from abc import *


class Analyzer(metaclass=ABCMeta):

    @abstractmethod
    def analyze_data(self, data):
        pass
