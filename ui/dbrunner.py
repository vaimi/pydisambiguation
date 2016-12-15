from nltk.corpus import semcor
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from nltk.tree import Tree
import random
import sys
import datetime

class classproperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)

class DbRunner(object):

    @classproperty
    def databasesAsStr(self):
        return [db.__name__ for db in self.databases]

    @classproperty
    def databases(self):
        return [semcor]

    def __init__(self, core, iterations=100, databaseStr="semcor", outputPath="report.txt", debugOutputPath=None):
        self.core = core
        self.iterations = iterations
        self.half = iterations/2
        class_ = getattr(sys.modules[__name__], databaseStr)
        self.dbStr = databaseStr
        self.db = class_
        self.outputPath = outputPath
        self.debugOutputPath = debugOutputPath
        
        self.result = []
        algorithms = self.core.getAlgorithmsInfo()
        self.algorithmscores = {}
        for algorithm in algorithms:
            self.algorithmscores[algorithm['key']] = {'n.correct':0, 'n.incorrect':0, 'v.correct':0, 'v.incorrect':0, 'v.none':0, 'n.none':0, 'runtime':0}

    def setupFormatter(self):
        i = datetime.datetime.now()
        response = "Run ended: %s\n" % i.isoformat()
        response += "Database: %s\n" % self.dbStr
        response += "Iterations: %s\n\n" % self.iterations
        return response




    def algorithmResultFormatter(self, algorithmId, algorithmScore):
        info = self.core.getAlgorithmInfo(algorithmId)
        nall = algorithmScore['n.incorrect']+algorithmScore['n.correct']+algorithmScore['n.none']
        vall = (algorithmScore['v.incorrect']+algorithmScore['v.correct']+algorithmScore['v.none'])
        naccuracy = 1 if algorithmScore['n.incorrect'] == 0 else algorithmScore['n.correct']/(nall - algorithmScore['n.none'])
        nrecall = 0 if nall == 0 else algorithmScore['n.correct']/nall
        vaccuracy = 1 if algorithmScore['v.incorrect'] == 0 else algorithmScore['v.correct']/(vall - algorithmScore['v.none'])
        vrecall = 0 if vall == 0 else algorithmScore['v.correct']/vall
        response = "Algorithm ID: %s\n" % algorithmId
        response += "Algorithm name: %s\n" % info['name']
        response += "Noun precision: %.2f\n" % naccuracy
        response += "Noun recall: %.2f\n" % nrecall
        response += "Verb precision: %.2f\n" % vaccuracy
        response += "Verb recall: %.2f\n" % vrecall
        response += "Average runtime: %.4f\n" % (algorithmScore['runtime']/self.iterations)
        response += "Raw: %s\n\n" % algorithmScore
        return response


    def writeResults(self):
        if self.outputPath:
            setup = self.setupFormatter()
            algorithmResults = [self.algorithmResultFormatter(algorithmKey, self.algorithmscores[algorithmKey]) for algorithmKey in self.algorithmscores]
            with open(self.outputPath, 'w') as file:
                file.write("--SETUP--\n")
                [file.write(line) for line in setup]
                file.write("--RESULTS--\n")
                [file.write(line) for line in algorithmResults]

                
        if self.debugOutputPath:
            with open(self.debugOutputPath, 'w') as file:
                for line in self.result:
                    file.write(line)

    def runTest(self, algorithmId, word, sentence, rightSense, wordTag):
        t1 = datetime.datetime.now()
        sense = self.core.runAlgorithm(algorithmId, word, sentence, {'pos':wordTag})
        t2 = datetime.datetime.now()
        delta = t2-t1
        self.algorithmscores[algorithmId]['runtime'] += delta.total_seconds()
        if sense['sense']:
            outText = "SENSE: %s: %s" % (sense['sense'], sense['sense'].definition())
        else:
            outText = "SENSE: Unable to make sense"
        testResult = None
        if sense['sense'] is None:
            if wordTag == 'NN':
                self.algorithmscores[algorithmId]['n.none'] += 1
            elif wordTag == 'VB':
                self.algorithmscores[algorithmId]['v.none'] += 1
            testResult = 2
        elif rightSense == sense['sense'].name():
            if wordTag == 'NN':
                self.algorithmscores[algorithmId]['n.correct'] += 1
            elif wordTag == 'VB':
                self.algorithmscores[algorithmId]['v.correct'] += 1
            testResult = 0
        else:
            if wordTag == 'NN':
                self.algorithmscores[algorithmId]['n.incorrect'] += 1
            elif wordTag == 'VB':
                self.algorithmscores[algorithmId]['v.incorrect'] += 1
            testResult = 1

        row = "%s, %s, %s, %s, %s, %s\n" % (algorithmId, testResult, word, sentence, sense['sense'], rightSense)
        self.result.append(row)

    def run(self):
        files = self.db.fileids()
        random.seed()
        random.shuffle(files)

        curRun = 0
        currFile = files.pop()
        currSent = None
        fcList = []
        ncount = 0
        vcount = 0
        while len(files) != 0:
            if curRun == self.iterations:
                break
            if len(fcList) == 0:
                currFile = files.pop()
                fc = self.db.tagged_sents(fileids=currFile, tag='both')
                fcList = list(fc)
            sentence = []

            sentPop = fcList.pop()
            for sent in sentPop:
                for word in sent:
                    if type(word) is Tree:
                        sentence.append(word.leaves())
                    else:
                        sentence.append([word])
            if len(sentence) < 5 or len(sentence) > 20:
                continue
            sentenceString = ' '.join([j for i in sentence for j in i])
            while len(sentPop) != 0:
                word = sentPop.pop()
                if word.label() is not None and not isinstance(word.label(), str) and len(word.leaves()) == 1:
                    wordSynset = word.label().synset().name()
                    wordString = ' '.join(word.leaves())
                    if wordString in stopwords.words('english'):
                        continue
                    pos = word.pos()
                    if pos[0][1] == 'NN':
                        if ncount < self.half:
                            ncount += 1
                            break
                    elif pos[0][1] == 'VB':
                        if vcount < self.half:
                            vcount += 1
                            break
            if not sentPop:
                continue

            message = "Disambiquate %s \"%s\" using \"%s\"\n" % (pos[0][1], wordString, sentenceString)
            print(message)
            #print("Running algorithm: ")
            for algorithm in self.core.getAlgorithmsInfo():
                print(str(algorithm['key']))
                self.runTest(algorithm['key'], wordString, sentenceString, wordSynset, pos[0][1])
            curRun+=1
        self.writeResults()

    def exampleRun(self):

        examples = [
            ("bass", "freshwater_bass.n.01", '"Though still a far cry from the lake’s record 52-pound bass of a decade ago, “you could fillet these fish again, and that made people very, very happy.” Mr. Paulson says'),
            ("bass", "bass.n.07", 'An electric guitar and bass player stand off to one side, not really part of the scene, just as a sort of nod to gringo expectations again.'),
            ("cold", "cold.n.03", "She shivered from the cold"),
            ("cold", "cold.n.01", "I am taking aspirin for my cold")
        ]

        for example in examples:
            for algorithm in self.core.getAlgorithmsInfo():
                self.runTest(algorithm['key'], example[0], example[2], example[1])
        self.writeResults()
