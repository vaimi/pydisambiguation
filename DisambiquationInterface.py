from abc import ABCMeta, abstractmethod

class DisambiquationInterface(metaclass=ABCMeta):
    def __init__(self):
        self.sentence = []
        self.word = ""
        self.sense = None
        self.definition = ""

    @abstractmethod
    def setSentence(self, sentenceList):
        self.sentence = sentenceList

    @abstractmethod
    def getSentenceAsList(self):
        return self.sentence

    @abstractmethod
    def setWord(self, word):
        self.word = word

    @abstractmethod
    def getWord(self):
        return self.word

    @abstractmethod
    def makeSense(self):
        pass

    @abstractmethod
    def getSenseTuple(self):
        return (self.sense.name(), self.definition)