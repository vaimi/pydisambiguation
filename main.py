#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import sys
from ui.qtgui import DisambiquateApp
from ui.dbrunner import DbRunner
from core import DisambiquateCore
import argparse

def dbrunnerLimit(x):
    x = int(x)
    if x < 1:
        raise argparse.ArgumentTypeError("Minimum test amount is 1")
    return x

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='WSD framework.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    mainSettings = parser.add_argument_group('Main settings')
    qtSettings = parser.add_argument_group('QT gui settings')
    dbSettings = parser.add_argument_group('DbRunner settings')

    mainSettings.add_argument('--ui', choices=['qt', 'dbrunner'], default="qt", help="UI to be used")
    mainSettings.add_argument('--include', nargs="*", help="Include these algorithms (classes and subclasses). Disables autoload of rest.")
    mainSettings.add_argument('--exclude', nargs="*", help="Exclude these algorithms (classes and subclasses).")

    dbSettings.add_argument("-i", "--iterations", default=100, type=dbrunnerLimit, help="Amount of iterations per algorithm")
    dbSettings.add_argument("-db", "--database", default="semcor", type=str, help="Database to be used", choices=DbRunner.databasesAsStr)
    dbSettings.add_argument("-r", "--report", default="report.txt", type=str, help="Report path")
    dbSettings.add_argument("-dr", "--debugreport", type=str, help="Optional debug dump path (csv)")

    args = parser.parse_args()
    print(args)
    
    core = DisambiquateCore()
    args.include = [] if args.include is None else args.include
    args.exclude = [] if args.exclude is None else args.exclude
    algorithms = core.findAlgorithms(args.include, args.exclude)
    [core.registerAlgorithm(core.getAlgorithmInstance(algorithm[0], algorithms)) for algorithm in algorithms]
    #core.registerAlgorithm(Lesk(settings), 1)
    #core.registerAlgorithm(EuclideanStandard(settings), 2)
    #core.registerAlgorithm(EuclideanPlus(settings), 3)
    #app = QApplication(sys.argv)
    if args.ui == "qt":
        app = DisambiquateApp(sys.argv, core)
        sys.exit(app.exec_())
    elif args.ui == "dbrunner":
        tester = DbRunner(core, args.iterations, args.database, args.report, args.debugreport)
        tester.run()

