from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from itertools import chain
from nltk import word_tokenize, pos_tag, defaultdict
from DisambiquationInterface import DisambiquationInterface

class Euclidean(DisambiquationInterface):
    def __init__(self):
        super().__init__()
        self.name = 'Euclidean'
        self.description = ''

    def setSentence(self, sentenceList):
        super().setSentence(sentenceList)

    def getSentenceAsList(self):
        return super().getSentenceAsList()

    def setWord(self, word):
        super().setWord(word)

    def getWord(self):
        return super().getWord()

    def makeSense(self):
        words = word_tokenize(self.sentence)
        posWords = pos_tag(words, tagset='universal')

        wordTag = pos_tag(word_tokenize(self.word), tagset='universal')
        if wordTag[0][1] == "NOUN":
            nouns = [a for (a, b) in posWords if b == "NOUN"]
        elif wordTag[0][1] == "VERB":
            verbs = [a for (a, b) in posWords if b == "VERB"]

    def getSenseDict(self):
        return super().getSenseDict()