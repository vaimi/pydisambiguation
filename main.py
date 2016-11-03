#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import logging
from PyQt5.QtWidgets import (QWidget, QFrame, QLabel, QPushButton, QLineEdit,QTextEdit, QGridLayout, QApplication, QHBoxLayout, QRadioButton)
from lesk import Lesk
from euclidean import Euclidean


class DisambiquateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        logging.basicConfig(level=logging.DEBUG)

    def initUI(self):
        self.wordsLabel = QLabel('Word')
        self.sentencesLabel = QLabel('Sentences(s)')
        self.methodLabel = QLabel('Method')
        self.outputLabel = QLabel('Sense')

        self.radioLayout = QHBoxLayout()
        self.euclideanRadioButton = QRadioButton("Euclidean")
        self.euclideanRadioButton.setChecked(True)

        self.leinRadioButton = QRadioButton("Lein")

        self.wordsEdit = QLineEdit()
        self.sentencesEdit = QTextEdit()

        self.buttonLayout = QHBoxLayout()
        self.disambiquateButton = QPushButton("Disambiquate")
        self.disambiquateButton.clicked.connect(self.buttonClicked)

        self.outputEdit = QTextEdit()
        self.outputEdit.setReadOnly(True)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.wordsLabel, 1, 0)
        self.grid.addWidget(self.wordsEdit, 1, 1)

        self.grid.addWidget(self.sentencesLabel, 2, 0)
        self.grid.addWidget(self.sentencesEdit, 2, 1, 2, 1)

        self.grid.addWidget(self.methodLabel, 5, 0)
        self.radioLayout.addWidget(self.euclideanRadioButton)
        self.radioLayout.addWidget(self.leinRadioButton)
        # Push radiobuttons to the left
        self.radioLayout.addStretch(1)
        self.grid.addLayout(self.radioLayout, 5, 1)

        self.buttonLayout.addWidget(self.disambiquateButton)
        self.buttonLayout.addStretch(1)
        self.grid.addLayout(self.buttonLayout, 6, 1)

        self.hLine = QFrame()
        self.hLine.setFrameShape(QFrame.HLine)
        self.hLine.setFrameShadow(QFrame.Sunken)
        self.grid.addWidget(self.hLine, 7, 1)

        self.grid.addWidget(self.outputLabel, 8, 0)
        self.grid.addWidget(self.outputEdit, 8, 1, 2, 1)

        self.setLayout(self.grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('PyDisambiquate')
        self.show()

    def buttonClicked(self):
        if (self.sender() == self.disambiquateButton):
            logging.debug("Disambiquate button pressed")
            self.disambiquateButton.setDisabled(True)
            words = self.__getWord()
            sentences = self.__getSentence()
            logging.debug("Words content: " + str(words))
            logging.debug("Sentences content: " + str(sentences))
            senseMaker = None
            if self.leinRadioButton.isChecked():
                senseMaker = Lesk()
                logging.debug("Using Lesk")
            else:
                senseMaker = Euclidean()
                logging.debug("Using Euclidean")

            senseMaker.setWord(words)
            senseMaker.setSentence(sentences)
            senseMaker.makeSense()
            sense = senseMaker.getSenseTuple()
            outText = "%s: %s" % (sense)
            logging.debug("Made sense: " + outText)
            self.outputEdit.setText(outText)
            self.disambiquateButton.setDisabled(False)

    def __getWord(self):
        return self.wordsEdit.text()

    def __getSentence(self):
        return self.sentencesEdit.toPlainText()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dw = DisambiquateWindow()
    sys.exit(app.exec_())