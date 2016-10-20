from nltk.wsd import lesk
from nltk.corpus import wordnet as wn

class Lesk(object):	
	def parse(self, sentence, word):
		ss = lesk(sentence.split(), word)
		return(ss.definition())
		
