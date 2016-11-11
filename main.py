#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import logging
from PyQt5.QtWidgets import (QWidget, QFrame, QLabel, QPushButton, QLineEdit,QTextEdit, QGridLayout, QApplication, QHBoxLayout, QRadioButton)
from lesk import Lesk
from euclidean import Euclidean

class DisambiquateCore(object):
    def __init__(self):
        self.algorithms = {}

    def registerAlgorithm(self, algorithm, key):
        if key not in self.algorithms and isinstance(key, int):
            if key >= 1:
                self.algorithms[key] = algorithm
                return key
        return False

    def unregisterAlgorithm(self, algorithm, key):
        if self.algorithms.pop(key, None):
            return True
        return False

    def getAlgorithmInfo(self, key):
        if key in self.algorithms:
            info = self.algorithms[key].getAlgorithmInfo()
            return {'key': key, 'name': info['name'], 'description': info['description']}
        return {}

    def getAlgorithmsInfo(self):
        return map(self.getAlgorithmInfo, self.algorithms)

    def runAlgorithm(self, key, word, sentence):
        algorithm = self.algorithms[key]
        algorithm.setWord(word)
        algorithm.setSentence(sentence)
        algorithm.makeSense()
        result = algorithm.getSenseDict()
        if result:
            return {'algorithm':key, 'sense':result['sense'], 'description': result['description']}
        return {}

class AlgorithmRadioButton(QRadioButton):
    def __init__(self, text, id):
        super().__init__(text)
        self.algorithmId = id

class DisambiquateWindow(QWidget):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.initUI()

        logging.basicConfig(level=logging.DEBUG)

    def __makeLabel(self, text, tooltip):
        label = QLabel(text)
        label.setToolTip(tooltip)
        return QLabel(text)

    def __makeEditBox(self):
        return QLineEdit()

    def __makeRadioButton(self, text, key):
        return AlgorithmRadioButton(text, key)

    def __makeHorizontalLine(self):
        hLine = QFrame()
        hLine.setFrameShape(QFrame.HLine)
        hLine.setFrameShadow(QFrame.Sunken)
        return hLine

    def __initElements(self):
        self.gridLayout = QGridLayout()
        self.radioLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()

        # First row
        self.wordsLabel = self.__makeLabel('Word', '')
        self.wordsEdit = self.__makeEditBox()

        # Second row
        self.sentencesLabel = self.__makeLabel('Sentence(s)', '')
        self.sentencesEdit = QTextEdit()

        # Third row
        self.methodLabel = self.__makeLabel('Method', '')
        algorithms = core.getAlgorithmsInfo()
        self.algorithmsRadioButtons = [self.__makeRadioButton(algorithm['name'], algorithm['key']) for algorithm in algorithms]

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
                sense = core.runAlgorithm(button.algorithmId, words, sentences)
                break

        if sense:
            outText = "%s: %s" % (sense['sense'], sense['description'])
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    core = DisambiquateCore()
    core.registerAlgorithm(Lesk(), 1)
    core.registerAlgorithm(Euclidean(), 2)
    dw = DisambiquateWindow(core)
    sys.exit(app.exec_())
