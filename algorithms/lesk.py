from interfaces.plugin import DisambiquationPlugin
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from itertools import chain

class Lesk(DisambiquationPlugin):
    """Basic lesk implementation for PyDisambiquation"""
    name = "Lesk"
    description = "Basic lesk implementation"
    parent = None
    initializeable = True

    def __init__(self, name=None, description=None, settings=None, parent=None):
        super(Lesk, self).__init__(name, description, settings, parent)

    def run(self):
        pos = None if not "pos" in self.settings else self.settings['pos']
        stem = True if not "stem" in self.settings else self.settings['stem']
        hyperhypo = True if not "hyperhypo" in self.settings else self.settings['hyperhypo']
        if not self.context or not self.word:
            return None
        sset = self.__parse(self.context, self.word, pos, stem, hyperhypo)
        if sset:
            return sset
        return None

    def __parse(self, context_sentence, ambiguous_word, pos=None, stem=True, hyperhypo=True):
        # Heavily based on http://stackoverflow.com/questions/20896278/word-sense-disambiguation-algorithm-in-python
        ps = PorterStemmer()

        max_overlaps = 0; lesk_sense = None
        context_sentence = context_sentence.split()
        for ss in wn.synsets(ambiguous_word):
            # If POS is specified.
            if pos and ss.pos is not pos:
                continue

            lesk_dictionary = []

            # Includes definition.
            lesk_dictionary+= ss.definition().split()
            # Includes lemma_names.
            lesk_dictionary+= ss.lemma_names()

            # Optional: includes lemma_names of hypernyms and hyponyms.
            if hyperhypo == True:
                lesk_dictionary+= list(chain(*[i.lemma_names() for i in ss.hypernyms()+ss.hyponyms()]))

            if stem == True: # Matching exact words causes sparsity, so lets match stems.
                lesk_dictionary = [ps.stem(i) for i in lesk_dictionary]
                context_sentence = [ps.stem(i) for i in context_sentence]

            overlaps = set(lesk_dictionary).intersection(context_sentence)

            if len(overlaps) > max_overlaps:
                lesk_sense = ss
                max_overlaps = len(overlaps)
        return lesk_sense
