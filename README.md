# PyDisambiguation

PyDisambiquation is a testing frontend for word sense disambiguation (WSD). System is designed so that adding new algorithms is as easy as possible. 

## Algorithms

If your algorithm implements AbstractPlugin and is placed to right folder, the system automatically includes it to the system. Therefore you can spend more time on developing actual algorithm than working with the surrounding framework.

The package includes some initial algorithms for testing:
- Two euclidean algorithms (with and without morphosemantic translation)
- Lesk algorithm
- 9 PyWSD algorithms

## User interfaces

Package provides two UIs for testing:
- QT GUI
- Automated database tester based on SEMCOR

You can easily add more interfaces by inspecting how the core class works.

## Requirements

System requirements:
- Python3 for running the code
- PyQt5 for GUI
- NLTK toolkit for language processing
- scikit-learn for machine learning
- xlrd for excel (.xsl) file parsing

PyWSD tranlated to Python3 code is provided inside the package.

