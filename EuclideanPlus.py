from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from itertools import chain
from nltk import word_tokenize, pos_tag, defaultdict
from DisambiquationInterface import DisambiquationInterface
import xlrd
from xlrd.sheet import ctype_text
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords



class EuclideanPlus(DisambiquationInterface):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Euclidean+'
        self.description = ''
        self.translator = self.parseXsl("morphosemantic-links.xls")

    def mean(self, numberList):
        numberList = [0 if x is None else x for x in numberList]
        return float(sum(numberList)) / max(len(numberList), 1)

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
        splitted = context.split(' ')
        context = ' '.join([self.replaceByNoun(verb) for verb in context.split(' ')])
        word = self.replaceByNoun(word)
        words = word_tokenize(context)
        words = [word for word in words if word not in stopwords.words('english')]
        posWords = pos_tag(words, tagset='universal')
        wordTag = pos_tag(word_tokenize(word), tagset='universal')
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

        wordSynsets = wn.synsets(word)

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
            return result[-1][0]
        return None
