from abc import ABCMeta, abstractmethod

class DisambiquationInterface(metaclass=ABCMeta):
    def __init__(self):
        self.sentence = []
        self.word = ""
        self.sense = None
        self.definition = ""
        self.name = ""
        self.description = ""

    @abstractmethod
    def setSentence(self, sentenceList):
        self.sentence = sentenceList
        self.sense = None
        self.definition = None

    @abstractmethod
    def getSentenceAsList(self):
        return self.sentence

    @abstractmethod
    def setWord(self, word):
        self.word = word
        self.sense = None
        self.definition = None

    @abstractmethod
    def getWord(self):
        return self.word

    @abstractmethod
    def makeSense(self):
        pass

    def getAlgorithmInfo(self):
        return {'name': self.name, 'description':self.description}

    @abstractmethod
    def getSenseDict(self):
        if self.sense is not None:
            return {'sense':self.sense.name(), 'description': self.definition}
        else:
            return {'sense':None, 'description': None}