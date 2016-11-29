from external.pywsd3.lesk import simple_lesk
from external.pywsd3.lesk import adapted_lesk
from external.pywsd3.similarity import max_similarity
from DisambiquationInterface import DisambiquationInterface
from AlgorithmCollection import AlgorithmCollection

class PyWSD(AlgorithmCollection):
    def __init__(self, settings):
        super().__init__(settings)

    @classmethod
    def getCollectionInfo(self):
        return {'name': 'PyWSD', 'description':''}

class PyWSDSimpleLesk(DisambiquationInterface):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Simple Lesk'
        self.description = ''
        self.parent = PyWSD

    def makeSense(self, context, word):
    	return simple_lesk(context,word)

class PyWSDAdaptedLesk(DisambiquationInterface):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Adapted Lesk'
        self.description = ''
        self.parent = PyWSD

    def makeSense(self, context, word):
    	return adapted_lesk(context,word)

class PyWSDCosineLesk(DisambiquationInterface):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Cosine Lesk'
        self.description = ''
        self.parent = PyWSD

    def makeSense(self, context, word):
    	return cosine_lesk(context,word)

class PyWSDPathSimilarity(DisambiquationInterface):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Path similarity'
        self.description = ''
        self.parent = PyWSD

    def makeSense(self, context, word):
    	return max_similarity(context, word, "path")

class PyWSDLchSimilarity(DisambiquationInterface):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Path similarity'
        self.description = ''
        self.parent = PyWSD

    def makeSense(self, context, word):
    	return max_similarity(context, word, "lch")

class PyWSDWupSimilarity(DisambiquationInterface):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Path similarity'
        self.description = ''
        self.parent = PyWSD

    def makeSense(self, context, word):
    	return max_similarity(context, word, "wup")

class PyWSDResSimilarity(DisambiquationInterface):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Path similarity'
        self.description = ''
        self.parent = PyWSD

    def makeSense(self, context, word):
    	return max_similarity(context, word, "res")

class PyWSDJcnSimilarity(DisambiquationInterface):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Path similarity'
        self.description = ''
        self.parent = PyWSD

    def makeSense(self, context, word):
    	return max_similarity(context, word, "jcn")

class PyWSDLinSimilarity(DisambiquationInterface):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Path similarity'
        self.description = ''
        self.parent = PyWSD

    def makeSense(self, context, word):
    	return max_similarity(context, word, "lin")






