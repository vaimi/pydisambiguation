from nltk.corpus import wordnet as wn
from itertools import chain
from nltk import word_tokenize, pos_tag, defaultdict
from nltk.wsd import lesk

from interfaces.plugin import DisambiquationPlugin
from interfaces.plugin_group import AlgorithmGroup

import xlrd
from xlrd.sheet import ctype_text
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from itertools import chain

class Euclidean(DisambiquationPlugin):
    """Parent for Euclidean plugins. Provides common methods for child algorithms.
    Note that this class doesn't have run method so it's not directly
    initializeable"""
    parent = AlgorithmGroup("Euclidean", "Group for euclidean algorithms")

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(Euclidean, self).__init__(name, description, settings, parent)

    def getMeaningfulWords(self, context, word):
        tokenizedContext = [word for word in context if word not in stopwords.words('english')]

        posContext = pos_tag(tokenizedContext, tagset='universal')
        posWord = pos_tag([word], tagset='universal')
        wordPos = posWord[0][1]

        meaningfulWords = None
        pos = None
        if wordPos in ["NOUN", "VERB"]:
            pos = wn.NOUN if wordPos is "NOUN" else wn.VERB
            meaningfulWords = [a for (a, b) in posContext if b == wordPos]
        if meaningfulWords is None:
            return ([], pos)
        return (meaningfulWords, pos)

    def calculatePathSimilarity(self, sense1, sense2):
        response = sense1.path_similarity(sense2)
        if response:
            return response
        return 0

    def calculateEuclideanSimilarity(self, contextWordsList, word, pos):
        wordSynsets = wn.synsets(word)
        result = {}
        for ss in wordSynsets:
            result[ss] = sum(max([self.calculatePathSimilarity(ss,k) for k in wn.synsets(j)] + [0]) for j in contextWordsList)
        return result

    def getClosestSense(self, scores):
        result = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        if len(result) != 0:
            return result[0][0]
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
        self.lemmatizer = WordNetLemmatizer()

    def run(self):
        word = self.lemmatizer.lemmatize(self.word)
        context = [self.lemmatizer.lemmatize(w) for w in self.context]
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
        self.lemmatizer = WordNetLemmatizer() 

    def parseXsl(self, fname):
        f = xlrd.open_workbook(fname)
        f_sheet = f.sheet_by_index(0)
        translator = {}
        for row in range(0, f_sheet.nrows):
            verb_obj = f_sheet.cell(row, 0)
            noun_obj = f_sheet.cell(row, 3)
            v = verb_obj.value.split('%')
            n = noun_obj.value.split('%')
            if v[0] not in translator:
                translator[v[0]] = []
            translator[v[0]].append(n[0])
        return translator

    def replaceByNoun(self, verb):
        if verb in self.translator:
            return list(set(self.translator[verb]))
        return [verb]

    def run(self):
        context = [self.lemmatizer.lemmatize(w) for w in self.context]
        context = [self.replaceByNoun(verb) for verb in context]
        context = [item for sublist in context for item in sublist]
        word = self.lemmatizer.lemmatize(self.word)
        word = self.replaceByNoun(word)
        word = word[0]

        (meaningfulWords, pos) = super(EuclideanPlus,self).getMeaningfulWords(context, word)
        if not len(meaningfulWords):
            return
        scores = super(EuclideanPlus,self).calculateEuclideanSimilarity(meaningfulWords, word, pos)
        return super(EuclideanPlus,self).getClosestSense(scores)