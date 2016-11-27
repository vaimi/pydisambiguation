from abc import ABCMeta, abstractmethod

class AlgorithmCollection(metaclass=ABCMeta):
    def __init__(self, settings):
        self.name = ""
        self.description = ""
        self.variants = []

    def getVariantsInfo(self):
        return [variant.getAlgorithmInfo for variant in variants]