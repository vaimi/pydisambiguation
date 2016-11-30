from nltk.corpus import semcor
import random

class DbRunner(object):
    def __init__(self, core, outputPath):
        self.core = core
        self.result = []
        self.outputPath = outputPath
        algorithms = self.core.getAlgorithmsInfo()
        self.algorithmscores = {}
        for algorithm in algorithms:
            self.algorithmscores[algorithm['key']] = {'correct':0, 'incorrect':0, 'none':0}



    def runTest(self, algorithmId, word, sentence, rightSense):
        sense = self.core.runAlgorithm(algorithmId, word, sentence)
        if sense['sense']:
            outText = "SENSE: %s: %s" % (sense['sense'], sense['sense'].definition())
        else:
            outText = "SENSE: Unable to make sense"
        testResult = None
        if sense['sense'] is None:
            self.algorithmscores[algorithmId]['none'] += 1
            testResult = 2
        elif rightSense == sense['sense'].name():
            self.algorithmscores[algorithmId]['correct'] += 1
            testResult = 0
        else:
            self.algorithmscores[algorithmId]['incorrect'] += 1
            testResult = 1

        row = "%s, %s, %s, %s, %s, %s\n" % (algorithmId, testResult, word, sentence, sense['sense'], rightSense)
        self.result.append(row)

    def runTester(self, runs):
        files = semcor.fileids()
        random.shuffle(files)

        curRun = 0
        currFile = files.pop()
        currSent = None
        fcList = []
        while len(files) != 0:
            if curRun == runs:
                break
            if len(fcList) == 0:
                currFile = files.pop()
                fc = semcor.tagged_sents(fileids=currFile, tag='both')
                fcList = list(fc)
            sentence = []
            sentPop = fcList.pop()
            for sent in sentPop:
                for word in sent:
                    try:
                        sentence.append(word.leaves())
                    except AttributeError:
                        pass
            if len(sentence) < 20:
                continue
            sentenceString = ' '.join([j for i in sentence for j in i])
            while len(sentPop) != 0:
                word = sentPop.pop()
                if word.label() is not None and not isinstance(word.label(), str) and len(word.leaves()) == 1:
                    wordSynset = word.label().synset().name()
                    wordString = ' '.join(word.leaves())
                    wordTag = pos_tag(word_tokenize(wordString), tagset='universal')
                    if wordTag[0][1] == "NOUN" or wordTag[0][1] == "VERB":
                        break
            message = "Disambiquate \"%s\" using \"%s\"\n" % (wordString, sentenceString)
            print(message)
            print("Running algorithm: ")
            for algorithm in self.core.getAlgorithmsInfo():
                print(str(algorithm['key']))
                self.runTest(algorithm['key'], wordString, sentenceString, wordSynset)
            curRun+=1
        with open(self.outputPath, 'w') as file:
            file.write(str(self.algorithmscores) + "\n")
            for line in self.result:
                file.write(line)
        sys.exit(0) 
