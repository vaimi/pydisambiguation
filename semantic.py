from tokenize import Tokenize

class SemanticSimilarity(object):
	def __init__(self):
		tokenizer = Tokenize()

	def parse(self, sentence, word):
		posTagged = tokenizer.parse(sentence)
		
	