from DisambiquationInterface import DisambiquationInterface
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from itertools import chain

class Lesk(DisambiquationInterface):
    def __init__(self, settings):
        super().__init__(settings)
        self.name = 'Lesk'
        self.description = ''

    def makeSense(self, context, word):
        sset = self.__parse(context, word)
        if sset:
            return sset
        return None

    def __parse(self, context_sentence, ambiguous_word, pos=None, stem=True, hyperhypo=True):
        # Based on http://stackoverflow.com/questions/20896278/word-sense-disambiguation-algorithm-in-python
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
