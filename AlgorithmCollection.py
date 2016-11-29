from abc import ABCMeta, abstractmethod

class AlgorithmCollection(metaclass=ABCMeta):
    def __init__(self, settings):
        super().__init__()

    @abstractmethod
    def getCollectionInfo(self):
        pass
        

    def getVariantsInfo(self):
        return [variant.getAlgorithmInfo for variant in variants]