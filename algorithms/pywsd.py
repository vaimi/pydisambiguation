from external.pywsd3.lesk import simple_lesk, adapted_lesk, cosine_lesk

from external.pywsd3.similarity import max_similarity

from interfaces.plugin import DisambiquationPlugin
from interfaces.plugin_group import AlgorithmGroup

class PyWSD(DisambiquationPlugin):
    parent = AlgorithmGroup("PyWSD", "Group for PyWsd similarity algorithms")

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSD, self).__init__(name, description, settings, parent)

class PyWSDSimpleLesk(PyWSD):
    name = "Simple Lesk"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDSimpleLesk, self).__init__(name, description, settings, parent)

    def run(self):
        return simple_lesk(self.context, self.word)

class PyWSDAdaptedLesk(PyWSD):
    name = "Adapted Lesk"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDAdaptedLesk, self).__init__(name, description, settings, parent)

    def run(self):
        return adapted_lesk(self.context, self.word)

class PyWSDCosineLesk(PyWSD):
    name = "Cosine Lesk"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDCosineLesk, self).__init__(name, description, settings, parent)

    def run(self):
        return cosine_lesk(self.context, self.word) 

class PyWSDPathSimilarity(PyWSD):
    name = "Path similarity"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDPathSimilarity, self).__init__(name, description, settings, parent)

    def run(self):
        return max_similarity(self.context, self.word, "path")

class PyWSDLchSimilarity(PyWSD):
    name = "Lch similarity"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDLchSimilarity, self).__init__(name, description, settings, parent)

    def run(self):
        return max_similarity(self.context, self.word, "lch")

class PyWSDWupSimilarity(PyWSD):
    name = "Wup similarity"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDWupSimilarity, self).__init__(name, description, settings, parent)

    def run(self):
        return max_similarity(self.context, self.word, "wup")

class PyWSDResSimilarity(PyWSD):
    name = "Res similarity"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDResSimilarity, self).__init__(name, description, settings, parent)

    def run(self):
        return max_similarity(self.context, self.word, "res")

class PyWSDJcnSimilarity(PyWSD):
    name = "Jcn Similarity"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDJcnSimilarity, self).__init__(name, description, settings, parent)

    def run(self):
        return max_similarity(self.context, self.word, "jcn")

class PyWSDLinSimilarity(PyWSD):
    name = "Lin similarity"

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(PyWSDLinSimilarity, self).__init__(name, description, settings, parent)

    def run(self):
        return max_similarity(self.context, self.word, "lin")