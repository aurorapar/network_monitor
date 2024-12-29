from abc import ABC, abstractmethod


class DataObject(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def adapt(self):
        pass

    @abstractmethod
    def convert(self):
        pass
