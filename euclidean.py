from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from itertools import chain
from nltk import word_tokenize, pos_tag, defaultdict
from nltk.wsd import lesk
from DisambiquationInterface import DisambiquationInterface
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

class Euclidean(DisambiquationInterface):
    def __init__(self):
        super().__init__()
        self.name = 'Euclidean'
        self.description = ''
        self.sense = None

    def setSentence(self, sentenceList):
        super().setSentence(sentenceList)

    def getSentenceAsList(self):
        return super().getSentenceAsList()

    def setWord(self, word):
        super().setWord(word)

    def getWord(self):
        return super().getWord()

    def mean(self, numberList):
        numberList = [0 if x is None else x for x in numberList]
        return float(sum(numberList)) / max(len(numberList), 1)

    def makeSense(self):
        lemmatizer = WordNetLemmatizer()
        self.sentence = ' '.join([lemmatizer.lemmatize(w) for w in word_tokenize(self.sentence)])
        self.word = ''.join(lemmatizer.lemmatize(self.word))

        words = word_tokenize(self.sentence)
        words = [word for word in words if word not in stopwords.words('english')]
        posWords = pos_tag(words, tagset='universal')

        wordTag = pos_tag(word_tokenize(self.word), tagset='universal')
        sentenceWords = None
        pos = None
        if wordTag[0][1] == "NOUN":
            pos = wn.NOUN
            sentenceWords = [a for (a, b) in posWords if b == "NOUN"]
        elif wordTag[0][1] == "VERB":
            pos = wn.VERB
            sentenceWords = [a for (a, b) in posWords if b == "VERB"]
        if sentenceWords is None:
            return
        result = {}

        wordSynsets = wn.synsets(self.word)

        for synset in wordSynsets:
            midResult = []
            for sentenceWord in sentenceWords:
                t = wn.synsets(sentenceWord, pos=pos)
                if len(t):
                    midResult.append(synset.path_similarity(t[0]))
                #t = [synset.path_similarity(j) for j in wn.synsets(sentenceWord, pos=pos)]
                #t = [0 if x is None else x for x in t]
                #if len(t):
                #    midResult.append(max(t))
            result[synset] = self.mean(midResult)

        result = sorted(result.items(), key=lambda x: x[1])
        if len(result) != 0:
            self.sense = result[-1][0]
            self.definition = result[-1][0].definition()

    def getSenseDict(self):
        return super().getSenseDict()