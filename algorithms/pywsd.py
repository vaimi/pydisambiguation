from external.pywsd3.lesk import simple_lesk, adapted_lesk, cosine_lesk

from external.pywsd3.similarity import max_similarity

from interfaces.plugin import DisambiquationPlugin
from interfaces.plugin_group import AlgorithmGroup

import nltk.corpus.reader.wordnet

class PyWSD(DisambiquationPlugin):
    parent = AlgorithmGroup("PyWSD", "Group for PyWsd similarity algorithms")

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSD, self).__init__(name, description, settings, parent)
        self._context = None

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, newContext):
        self._context = ' '.join(newContext)

class PyWSDSimpleLesk(PyWSD):
    name = "Simple Lesk"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDSimpleLesk, self).__init__(name, description, settings, parent)

    def run(self):
        try:
            return simple_lesk(self.context, self.word)
        except TypeError:
            return None

class PyWSDAdaptedLesk(PyWSD):
    name = "Adapted Lesk"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDAdaptedLesk, self).__init__(name, description, settings, parent)

    def run(self):
        try:
            return adapted_lesk(self.context, self.word)
        except TypeError:
            return None

class PyWSDCosineLesk(PyWSD):
    name = "Cosine Lesk"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDCosineLesk, self).__init__(name, description, settings, parent)

    def run(self):
        try:
            return cosine_lesk(self.context, self.word) 
        except TypeError:
            return None

class PyWSDPathSimilarity(PyWSD):
    name = "Path similarity"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDPathSimilarity, self).__init__(name, description, settings, parent)

    def run(self):
        try:
            return max_similarity(self.context, self.word, option="path")
        except:
            return None


class PyWSDLchSimilarity(PyWSD):
    name = "Lch similarity"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDLchSimilarity, self).__init__(name, description, settings, parent)

    def run(self):
        try:
            return max_similarity(self.context, self.word, option="lch")
        except:
            return None

class PyWSDWupSimilarity(PyWSD):
    name = "Wup similarity"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDWupSimilarity, self).__init__(name, description, settings, parent)

    def run(self):
        try:
            return max_similarity(self.context, self.word, pos="n", option="wup")
        except:
            return None

class PyWSDResSimilarity(PyWSD):
    name = "Res similarity"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDResSimilarity, self).__init__(name, description, settings, parent)

    def run(self):
        try:
            return max_similarity(self.context, self.word, option="res")
        except:
            return None

class PyWSDJcnSimilarity(PyWSD):
    name = "Jcn Similarity"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDJcnSimilarity, self).__init__(name, description, settings, parent)

    def run(self):
        try:
            return max_similarity(self.context, self.word, option="jcn")
        except:
            return None

class PyWSDLinSimilarity(PyWSD):
    name = "Lin similarity"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDLinSimilarity, self).__init__(name, description, settings, parent)

    def run(self):
        try:
            return max_similarity(self.context, self.word, option="lin")
        except:
            return None
