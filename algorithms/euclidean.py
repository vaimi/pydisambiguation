from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from itertools import chain
from nltk import word_tokenize, pos_tag, defaultdict
from nltk.wsd import lesk

from interfaces.plugin import DisambiquationPlugin
from interfaces.plugin_group import AlgorithmGroup

import xlrd
from xlrd.sheet import ctype_text
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

class Euclidean(DisambiquationPlugin):
    """Parent for Euclidean plugins. Provides common methods for child algorithms.
    Note that this class doesn't have run method so it's not directly
    initializeable"""
    parent = AlgorithmGroup("Euclidean", "Group for euclidean algorithms")

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(Euclidean, self).__init__(name, description, settings, parent)

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

    def getClosestSense(self, scores):
        result = sorted(scores.items(), key=lambda x: x[1])
        if len(result) != 0:
            return result[-1][0]
        return

    def mean(self, numberList):
        numberList = [0 if x is None else x for x in numberList]
        return float(sum(numberList)) / max(len(numberList), 1)


class EuclideanStandard(Euclidean):
    """Euclidean algorithm implementation for PyDisambiquation"""
    name = "Standard Euclidean"
    description = "Standard implementation for euclidean algorithm"
    
    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(Euclidean, self).__init__(name, description, settings, parent)

    def run(self):
        lemmatizer = WordNetLemmatizer()
        context = ' '.join([lemmatizer.lemmatize(w) for w in word_tokenize(self.context)])
        word = ''.join(lemmatizer.lemmatize(self.word))
        (meaningfulWords, pos) = super(EuclideanStandard,self).getMeaningfulWords(context, word)
        if not len(meaningfulWords):
            return
        scores = super(EuclideanStandard,self).calculateEuclideanSimilarity(meaningfulWords, word, pos)
        return super(EuclideanStandard,self).getClosestSense(scores)

class EuclideanPlus(Euclidean):
    name = "Euclidian + morphosemantic"
    description = "Euclidean with morphosemantic translator"
    
    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(Euclidean, self).__init__(name, description, settings, parent)
        self.translator = self.parseXsl("external/morphosemantic-links.xls")    

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

    def run(self):
        lemmatizer = WordNetLemmatizer()
        context = ' '.join([lemmatizer.lemmatize(w) for w in word_tokenize(self.context)])
        word = ''.join(lemmatizer.lemmatize(self.word))

        context = ' '.join([self.replaceByNoun(verb) for verb in context.split(' ')])
        word = self.replaceByNoun(word)

        (meaningfulWords, pos) = super(EuclideanPlus,self).getMeaningfulWords(context, word)
        if not len(meaningfulWords):
            return
        scores = super(EuclideanPlus,self).calculateEuclideanSimilarity(meaningfulWords, word, pos)
        return super(EuclideanPlus,self).getClosestSense(scores)