from abc import ABCMeta, abstractmethod

class DisambiquationInterface(metaclass=ABCMeta):
    def __init__(self, settings):
        self.name = ""
        self.description = ""
        self.parent = None
        self.settings = {}

    @abstractmethod
    def makeSense(self, context, word):
        pass

    def setSettings(self, settingsDict):
        self.settings = settings

    def hasVariants(self):
        return len(self.variants) > 1

    def getVariantsInfo(self):
        return [variant.getAlgorithmInfo for variant in variants]

    def getSettings(self):
        return self.settings

    def getAlgorithmInfo(self):
        return {'name': self.name, 'description':self.description, 'parent':self.parent}

