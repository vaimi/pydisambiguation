#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import sys
from ui.qtgui import DisambiquateApp
from ui.dbrunner import DbRunner
from core import DisambiquateCore

from nltk import word_tokenize, pos_tag, defaultdict




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    core = DisambiquateCore()
    settings = {}

    algorithms = core.findAlgorithms()
    [core.registerAlgorithm(core.getAlgorithmInstance(algorithm[0], algorithms)) for algorithm in algorithms]
    #core.registerAlgorithm(Lesk(settings), 1)
    #core.registerAlgorithm(EuclideanStandard(settings), 2)
    #core.registerAlgorithm(EuclideanPlus(settings), 3)
    #app = QApplication(sys.argv)
    app = DisambiquateApp(sys.argv, core)
    #tester = dbTestRunner(core, "result.csv")
    #tester.runTester(1000)
    app.exec_()
    #sys.exit(app.exec_())
