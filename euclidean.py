from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from itertools import chain
from nltk import word_tokenize, pos_tag, defaultdict
from nltk.wsd import lesk
from DisambiquationInterface import DisambiquationInterface
from AlgorithmCollection import AlgorithmCollection
import xlrd
from xlrd.sheet import ctype_text
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

class Euclidean(AlgorithmCollection):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Euclidean'
        self.description = ''

        self.variants = [EuclideanStandard, EuclideanPlus]

    @classmethod
    def getMeaningfulWords(self, context, word):
        tokenizedContext = [word for word in word_tokenize(context) if word not in stopwords.words('english')]

        posContext = pos_tag(tokenizedContext, tagset='universal')
        posWord = pos_tag(word_tokenize(word), tagset='universal')
        wordPos = posWord[0][1]

        meaningfulWords = None
        pos = None
        if wordPos in ["NOUN", "VERB"]:
            pos = wn.NOUN if wordPos is "NOUN" else wn.VERB
            meaningfulWords = [a for (a, b) in posContext if b == wordPos]
        if meaningfulWords is None:
            return ([], pos)
        return (meaningfulWords, pos)

    @classmethod
    def calculateEuclideanSimilarity(self, contextWordsList, word, pos):
        wordSynsets = wn.synsets(word)
        result = {}
        for synset in wordSynsets:
            midResult = []
            for sentenceWord in contextWordsList:
                t = wn.synsets(sentenceWord, pos=pos)
                if len(t):
                    midResult.append(synset.path_similarity(t[0]))
                #t = [synset.path_similarity(j) for j in wn.synsets(sentenceWord, pos=pos)]
                #t = [0 if x is None else x for x in t]
                #if len(t):
                #    midResult.append(max(t))
            result[synset] = self.mean(midResult)
        return result

    @classmethod
    def getClosestSense(self, scores):
        result = sorted(scores.items(), key=lambda x: x[1])
        if len(result) != 0:
            return result[-1][0]
        return

    @classmethod
    def mean(self, numberList):
        numberList = [0 if x is None else x for x in numberList]
        return float(sum(numberList)) / max(len(numberList), 1)




class EuclideanStandard(DisambiquationInterface):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Standard Euclidean'
        self.description = ''
        self.parent = Euclidean

    def makeSense(self, context, word):
        lemmatizer = WordNetLemmatizer()
        context = ' '.join([lemmatizer.lemmatize(w) for w in word_tokenize(context)])
        word = ''.join(lemmatizer.lemmatize(word))
        (meaningfulWords, pos) = Euclidean.getMeaningfulWords(context, word)
        if not len(meaningfulWords):
            return
        scores = Euclidean.calculateEuclideanSimilarity(meaningfulWords, word, pos)
        return Euclidean.getClosestSense(scores)

class EuclideanPlus(DisambiquationInterface):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Euclidean+'
        self.description = ''
        self.translator = self.parseXsl("morphosemantic-links.xls")

    def parseXsl(self, fname):
        f = xlrd.open_workbook(fname)
        f_sheet = f.sheet_by_index(0)
        translator = {}
        for row in range(0, f_sheet.nrows):
            verb_obj = f_sheet.cell(row, 0)
            noun_obj = f_sheet.cell(row, 3)
            v = verb_obj.value.split('%')
            n = noun_obj.value.split('%')
            translator[v[0]] = n[0]
        return translator

    def replaceByNoun(self, verb):
        if verb in self.translator:
            return self.translator[verb]
        return verb

    def makeSense(self, context, word):
        lemmatizer = WordNetLemmatizer()
        context = ' '.join([lemmatizer.lemmatize(w) for w in word_tokenize(context)])
        word = ''.join(lemmatizer.lemmatize(word))

        context = ' '.join([self.replaceByNoun(verb) for verb in context.split(' ')])
        word = self.replaceByNoun(word)

        (meaningfulWords, pos) = Euclidean.getMeaningfulWords(context, word)
        if not len(meaningfulWords):
            return
        scores = Euclidean.calculateEuclideanSimilarity(meaningfulWords, word, pos)
        return Euclidean.getClosestSense(scores)



