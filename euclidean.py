from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from itertools import chain
from DisambiquationInterface import DisambiquationInterface

class Euclidean(DisambiquationInterface):
    def __init__(self):
        super().__init__()

    def setSentence(self, sentenceList):
        super().setSentence(sentenceList)

    def getSentenceAsList(self):
        return super().getSentenceAsList()

    def setWord(self, word):
        super().setWord(word)

    def getWord(self):
        return super().getWord()

    def makeSense(self):
        pass

    def getSenseTuple(self):
        return super().getSenseTuple()