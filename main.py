#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import logging
from PyQt5.QtWidgets import (QWidget, QFrame, QLabel, QPushButton, QComboBox, QLineEdit,QTextEdit, QGridLayout, QApplication, QHBoxLayout, QRadioButton)
import os
import inspect
import imp
import importlib

from DisambiquationInterface import DisambiquationInterface

from nltk.corpus import semcor
import random
from nltk import word_tokenize, pos_tag, defaultdict
from nltk.corpus import semcor

class DisambiquateCore(object):
    def __init__(self):
        self.algorithms = {}

    def findAlgorithms(self):
        #https://chriscoughlin.com/2012/04/writing-a-python-plugin-framework/
        algorithms_folder = "./algorithms"
        algorithms = []
        if not algorithms_folder in sys.path:
            sys.path.append(algorithms_folder)
        for root, dirs, files in os.walk(algorithms_folder):
            for module_file in files:
                module_name, module_extension = os.path.splitext(module_file)
                if module_extension == os.extsep + "py":
                    plugin_module = importlib.import_module(module_name)
                    plugin_classes = inspect.getmembers(plugin_module, inspect.isclass)
                    for plugin_class in plugin_classes:
                        if issubclass(plugin_class[1], DisambiquationInterface):
                            if plugin_class[1].__module__ == module_name:
                                #plugin = plugin_class[1]()
                                algorithms.append(plugin_class)
        return algorithms

    def getAlgorithmInstance(self, plugin_name, algorithms = None):
        """Given the name of a plugin, returns the plugin's class and an instance of the plugin,
        or (None, None) if the plugin isn't listed in the available plugins."""
        plugin_instance = None
        available_plugins = self.findAlgorithms() if algorithms is None else algorithms 
        plugin_names = [plugin[0] for plugin in available_plugins]
        plugin_classes = [plugin[1] for plugin in available_plugins]
        if plugin_name in plugin_names:
            plugin_class = plugin_classes[plugin_names.index(plugin_name)]
            plugin_instance = plugin_class(None)
            #plugin_instance.data = self.data
        return plugin_instance

    def registerAlgorithm(self, algorithm, key=None):
        key = len(self.algorithms)+1 if key is None else key
        if key not in self.algorithms and isinstance(key, int):
            if key >= 1:
                self.algorithms[key] = algorithm
                return key
        return False

    def unregisterAlgorithm(self, algorithm):
        if self.algorithms.pop(key, None):
            return True
        return False

    def getAlgorithmInfo(self, key):
        if key in self.algorithms:
            info = self.algorithms[key].getAlgorithmInfo()
            return {'key': key, 'name': info['name'], 'description': info['description'], 'parent':info['parent']}
        return {}

    def getAlgorithmsInfo(self):
        return map(self.getAlgorithmInfo, self.algorithms)

    def runAlgorithm(self, key, word, sentence):
        algorithm = self.algorithms[key]
        result = algorithm.makeSense(sentence, word)
        return {'algorithm':key, 'sense':result}

class AlgorithmRadioButton(QRadioButton):
    def __init__(self, text, id=None, group=None):
        super().__init__(text)
        self.algorithmId = id
        self.group = group

class DisambiquateWindow(QWidget):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.initUI()

    def __makeLabel(self, text, tooltip):
        label = QLabel(text)
        label.setToolTip(tooltip)
        return QLabel(text)

    def __makeEditBox(self):
        return QLineEdit()

    def __makeRadioButton(self, text, key=None, group=None):
        radiobutton = AlgorithmRadioButton(text, key, group)
        radiobutton.clicked.connect(self.selectionChanged)
        return radiobutton

    def __makeComboBox(self, items):
        comboBox = QComboBox()
        [comboBox.addItem(algorithm['name'], algorithm['key']) for algorithm in items]
        return comboBox


    def __makeHorizontalLine(self):
        hLine = QFrame()
        hLine.setFrameShape(QFrame.HLine)
        hLine.setFrameShadow(QFrame.Sunken)
        return hLine

    def __initElements(self):
        self.gridLayout = QGridLayout()
        self.radioLayout = QHBoxLayout()
        self.variantLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()

        # First row
        self.wordsLabel = self.__makeLabel('Word', '')
        self.wordsEdit = self.__makeEditBox()

        # Second row
        self.sentencesLabel = self.__makeLabel('Sentence(s)', '')
        self.sentencesEdit = QTextEdit()

        # Third row
        self.methodLabel = self.__makeLabel('Method', '')

        groups = list(set([algorithm['parent'] for algorithm in core.getAlgorithmsInfo() if algorithm['parent'] is not None]))
        self.algorithmsRadioButtons = []
        for group in groups:
            info = group.getCollectionInfo()
            self.algorithmsRadioButtons += [self.__makeRadioButton(info['name'] + ' (+)', None, group)]
        self.algorithmsRadioButtons += [self.__makeRadioButton(algorithm['name'], algorithm['key']) for algorithm in core.getAlgorithmsInfo() if algorithm['parent'] is None]

        #
        self.variantLabel = self.__makeLabel('Variant', '')
        self.variantComboBox = QComboBox()


        # Fourth row
        self.disambiquateButton = QPushButton("Disambiquate")

        # Fifth row
        self.hLine = self.__makeHorizontalLine()

        # Sixth row
        self.outputLabel = self.__makeLabel('Sense', '')
        self.outputEdit = QTextEdit()

    def __setElementSettings(self):
        self.outputEdit.setReadOnly(True)
        self.algorithmsRadioButtons[0].setChecked(True)
        self.selectionChanged()
        self.disambiquateButton.clicked.connect(self.disambiquateButtonClicked)
        self.gridLayout.setSpacing(10)

    def __setLayout(self):
        row = 1
        labelColumn = 0
        contentColumn = 1
        self.setLayout(self.gridLayout)

        self.gridLayout.addWidget(self.wordsLabel, row, labelColumn)
        self.gridLayout.addWidget(self.wordsEdit, row, contentColumn)

        row += 1
        self.gridLayout.addWidget(self.sentencesLabel, row, labelColumn)
        self.gridLayout.addWidget(self.sentencesEdit, row, contentColumn, 2, 1)

        row += 2
        self.gridLayout.addWidget(self.methodLabel, row, labelColumn)
        self.gridLayout.addLayout(self.radioLayout, row, contentColumn)
        [self.radioLayout.addWidget(button) for button in self.algorithmsRadioButtons]
        self.radioLayout.addStretch(1)

        row += 1
        self.gridLayout.addWidget(self.variantLabel, row, labelColumn)
        self.gridLayout.addLayout(self.variantLayout, row, contentColumn)
        self.variantLayout.addWidget(self.variantComboBox)
        #self.variantLayout.addStretch(1)

        row += 1
        self.gridLayout.addLayout(self.buttonLayout, row, contentColumn)
        self.buttonLayout.addWidget(self.disambiquateButton)
        self.buttonLayout.addStretch(1)

        row += 1
        self.gridLayout.addWidget(self.hLine, row, contentColumn)

        row += 1
        self.gridLayout.addWidget(self.outputLabel, row, labelColumn)
        self.gridLayout.addWidget(self.outputEdit, row, contentColumn, 2, 1)

    def initUI(self):
        self.__initElements()
        self.__setElementSettings()
        self.__setLayout()

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('PyDisambiquate')
        self.show()

    def selectionChanged(self):
        self.variantComboBox.clear()
        for button in self.algorithmsRadioButtons:
            if button.isChecked():
                if button.algorithmId == None:
                    self.variantComboBox.setEnabled(True)
                    [self.variantComboBox.addItem(algorithm['name'], algorithm['key']) for algorithm in core.getAlgorithmsInfo() if algorithm['parent'] is button.group]
                else:
                    self.variantComboBox.setDisabled(True)

    def disambiquateButtonClicked(self):
        logging.debug("Disambiquate button pressed")
        self.disambiquateButton.setDisabled(True)
        words = self.__getWord().strip()
        sentences = self.__getSentence().strip()
        if not words or not sentences:
            self.disambiquateButton.setEnabled(True)

            pass
        logging.debug("Words content: " + str(words))
        logging.debug("Sentences content: " + str(sentences))

        sense = False
        for button in self.algorithmsRadioButtons:
            if button.isChecked():
                if button.group is None:
                    sense = core.runAlgorithm(button.algorithmId, words, sentences)
                    break
                else:
                    sense = core.runAlgorithm(self.variantComboBox.itemData(self.variantComboBox.currentIndex()), words, sentences)
                    break
        if sense['sense']:
            outText = "%s: %s" % (sense['sense'], sense['sense'].definition())
        else:
            outText = "Unable to make sense"
        logging.debug("Made sense: " + outText)
        self.outputEdit.setText(outText)
        self.disambiquateButton.setEnabled(True)

    def __getWord(self):
        return self.wordsEdit.text()

    def __getSentence(self):
        return self.sentencesEdit.toPlainText()


class CSVRunner(object):
    def __init__(self, inputPath, outputPath):
        self.inputPath = inputPath
        self.outputPath = outputPath

    def parseInput(self):
        pass

    def writeOut(self, id, method, word, sense):
        pass

class dbTestRunner(object):
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

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    core = DisambiquateCore()
    settings = {}

    algorithms = core.findAlgorithms()
    [core.registerAlgorithm(core.getAlgorithmInstance(algorithm[0], algorithms)) for algorithm in algorithms]
    #core.registerAlgorithm(Lesk(settings), 1)
    #core.registerAlgorithm(EuclideanStandard(settings), 2)
    #core.registerAlgorithm(EuclideanPlus(settings), 3)
    dw = DisambiquateWindow(core)
    #tester = dbTestRunner(core, "result.csv")
    #tester.runTester(1000)

    sys.exit(app.exec_())
