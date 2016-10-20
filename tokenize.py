import nltk
import nltk.tokenize

class Tokenize(object):
	def parse(self,text):
		tokenized = nltk.word_tokenize(text)
		return(nltk.pos_tag(tokenized))