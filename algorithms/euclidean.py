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
from nltk.stem.porter import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances

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

    def doEuclidean(self, word, context):
        vectorizer = TfidfVectorizer()
        senses = wn.synsets(word)
        sensesDefinitions = [ss.definition() for ss in senses]
        tfIdf = vectorizer.fit_transform([' '.join(context)] + sensesDefinitions)
        result = euclidean_distances(tfIdf[0:1], tfIdf)
        resultList = result.tolist()
        best = 0
        bestI = 0
        for i in range(1,len(resultList[0])):
            if best < resultList[0][i]:
                bestI = i
                best = resultList[0][i]
            elif best == resultList[0][i]:
                bestI = 0
        if bestI == 0:
            return None
        return(senses[bestI-1])

class EuclideanStandard(Euclidean):
    """Euclidean algorithm implementation for PyDisambiquation"""
    name = "Standard Euclidean"
    description = "Standard implementation for euclidean algorithm"

    token_dict = {}
    stemmer = PorterStemmer()

    def stem_tokens(tokens, stemmer):
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed

    def tokenize(text):
        tokens = nltk.word_tokenize(text)
        stems = stem_tokens(tokens, stemmer)
        return stems
    
    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(Euclidean, self).__init__(name, description, settings, parent)
        self.lemmatizer = WordNetLemmatizer()

    def run(self):
        word = self.lemmatizer.lemmatize(self.word)
        context = [self.lemmatizer.lemmatize(w) for w in self.context]
        return(super(EuclideanStandard, self).doEuclidean(word, context))
        

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

        return(super(EuclideanPlus, self).doEuclidean(word, context))