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

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances, cosine_distances

from itertools import chain

class Euclidean(DisambiquationPlugin):
    """Parent for Euclidean plugins. Provides common methods for child algorithms.
    Note that this class doesn't have run method so it's not directly
    initializeable"""
    parent = AlgorithmGroup("Euclidean", "Group for euclidean algorithms")

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(Euclidean, self).__init__(name, description, settings, parent)

    def getMeaningfulWords(self, context, word, pos=None, both=None):
        tokenizedContext = [word for word in context if word not in stopwords.words('english')]
        posContext = pos_tag(tokenizedContext, tagset='universal')
        posWord = ""
        if not pos:
            posWord = pos_tag([word], tagset='universal')
            posWord = posWord[0][1]
        else:
            posWord='NOUN' if pos == 'NN' else 'VERB'
        meaningfulWords = None
        pos = None
        print(posWord)
        if posWord in ["VERB", "NOUN"]:
            if both:
                meaningfulWords = [a for (a, b) in posContext if b in ["VERB", "NOUN"]]
            else:
                meaningfulWords = [a for (a, b) in posContext if b == posWord]
        if meaningfulWords is None:
            return ([], pos)
        return (meaningfulWords, posWord)

    def doEuclidean(self, word, context):
        vectorizer = CountVectorizer()
        senses = wn.synsets(word)
        sensesDefinitions = [ss.definition()+' '.join(ss.lemma_names()) for ss in senses]
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
            return None, None
        return(senses[bestI-1], best)

class EuclideanStandard(Euclidean):
    """Euclidean algorithm implementation for PyDisambiquation"""
    name = "Standard Euclidean"
    description = "Standard implementation for euclidean algorithm"

    token_dict = {}
    stemmer = PorterStemmer()
    
    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(Euclidean, self).__init__(name, description, settings, parent)
        self.lemmatizer = WordNetLemmatizer()

    def run(self):
        word = self.lemmatizer.lemmatize(self.word)
        context = [self.lemmatizer.lemmatize(w) for w in self.context]
        response, best_score = super(EuclideanStandard, self).doEuclidean(word, context)
        return(response)
        

class EuclideanPlus(Euclidean):
    name = "Euclidian + morphosemantic"
    description = "Euclidean with morphosemantic translator"
    
    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(Euclidean, self).__init__(name, description, settings, parent)
        self.translator = self.parseXsl("external/morphosemantic-links.xls")
        self.backtranslator = {v: k for k, v in self.translator.items()}
        self.lemmatizer = WordNetLemmatizer() 

    def parseXsl(self, fname):
        f = xlrd.open_workbook(fname)
        f_sheet = f.sheet_by_index(0)
        translator = {}
        for row in range(1, f_sheet.nrows):
            verb_obj = f_sheet.cell(row, 0)
            noun_obj = f_sheet.cell(row, 3)
            v = verb_obj.value
            n = noun_obj.value
            translator[wn.lemma_from_key(v).synset()] = wn.lemma_from_key(n).synset()
        return translator

    def replaceByNoun(self, verb):
        response = []
        posWord = pos_tag(verb, tagset='universal')
        if posWord[0][1] == 'NOUN':
            return [verb]
        synsets = wn.synsets(verb)
        for synset in synsets:
            if synset in self.translator:
                response.append(synset.name().split('.')[0])
        if response:
            return list(set(response))
        return [verb]

    def replaceByVerbSynset(self, nounSynset):
        if nounSynset in self.backtranslator:
            return self.backtranslator[nounSynset]
        return None

    def run(self):
        pos = self.settings['pos']
        context = [self.lemmatizer.lemmatize(w) for w in self.context]
        context, pos = super(EuclideanPlus, self).getMeaningfulWords(context, self.word, pos=pos, both=True)
        context = [self.replaceByNoun(verb) for verb in context]
        context = [item for sublist in context for item in sublist]
        if not context:
            return None
        words = self.lemmatizer.lemmatize(self.word)
        if pos == 'VERB':
            words = self.replaceByNoun(words)
        else:
            words = [words]
        scores = {}

        for word in words:
            response, score = super(EuclideanPlus, self).doEuclidean(word, context)
            if response is not None:
                scores[score] = response
        if scores:
            best = max(scores.keys())
            if pos == 'VERB':
                return(self.replaceByVerbSynset(scores[best]))
            else:
                return(scores[best])
        return None