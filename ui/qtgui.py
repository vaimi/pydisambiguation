from PyQt5.QtWidgets import (QWidget, QFrame, QLabel, QPushButton, QComboBox, QLineEdit,QTextEdit, QGridLayout, QApplication, QHBoxLayout, QRadioButton)
import logging

class AlgorithmRadioButton(QRadioButton):
    def __init__(self, text, id=None, group=None):
        super().__init__(text)
        self.algorithmId = id
        self.group = group

class DisambiquateApp(QApplication):
    def __init__(self, sysargs, core):
        super(DisambiquateApp, self).__init__(sysargs)
        self.dw = DisambiquateWindow(core)

class DisambiquateWindow(QFrame):
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

        groups = list(set([algorithm['parent'] for algorithm in self.core.getAlgorithmsInfo() if algorithm['parent'] is not None]))
        self.algorithmsRadioButtons = []
        for group in groups:
            self.algorithmsRadioButtons += [self.__makeRadioButton(group.name + ' (+)', None, group)]
        self.algorithmsRadioButtons += [self.__makeRadioButton(algorithm['name'], algorithm['key']) for algorithm in self.core.getAlgorithmsInfo() if algorithm['parent'] is None]

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
                    [self.variantComboBox.addItem(algorithm['name'], algorithm['key']) for algorithm in self.core.getAlgorithmsInfo() if algorithm['parent'] is button.group]
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
                    sense = self.core.runAlgorithm(button.algorithmId, words, sentences)
                    break
                else:
                    sense = self.core.runAlgorithm(self.variantComboBox.itemData(self.variantComboBox.currentIndex()), words, sentences)
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
