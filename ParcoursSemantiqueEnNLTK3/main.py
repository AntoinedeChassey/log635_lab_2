  # -*- coding: utf-8 -*-

'''
Created on 24 oct. 2016

@author: Antoine de Chassey, Victor Mabille, Louis Congard
'''

import re
from nltk import *
import nltk

caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Il\s|Elle\s|Ce\s|Ils\s|Leur\s|Notre\s|Nous\s|Mais\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|fr|net|org|io|gov)"

class nltkTextParser:
    def __init__(self, textFile, grammarFile):
        self.textFile = textFile
        self.grammarFile   = grammarFile
        
        self.loadSentences()
        self.loadGrammar()
    
    """
    Load the text file and create an array of sentences
    """
    def loadSentences(self):
        with open (self.textFile, "r", encoding='utf-8') as myfile:
                text = myfile.read()
                self.sentences = split_into_sentences(text.lower())
        print(self.sentences)
        
    """
    Load the grammar file parse it in NLTK
    """
    def loadGrammar(self):
        with open(self.grammarFile, "r", encoding='utf-8') as f:
            my_grammar = grammar.FeatureGrammar.fromstring(f.read())
            self.parser = nltk.FeatureEarleyChartParser(my_grammar)
            
    """
    Generate an output file for all the rules
    """
    def makeFacts(self, outputFile):
        with open(outputFile, 'w', encoding='utf-8') as f:
            for sentence in self.sentences:
                comprehensiveSentence = self.getSentence(sentence)
        
                print('Processing [{}]'.format(comprehensiveSentence))
                
                # tokenize the comprehensiveSentence
                tokens = comprehensiveSentence.split()
                trees = list(self.parser.parse(tokens))
                                
                for tree in trees:
                    self.writeJessRule(f, str(tree.label()['SEM']))
#                     print(tree)
#                     tree.draw()

    """
    Returns a list of tokens from sentence
    """
    def getSentence(self, sentence):
        comprehensiveSentence = re.sub(r'(\.|\#|\,|\')', ' ', sentence).strip('\r\n').strip()
        return comprehensiveSentence
    
    """
    Generate the jess rule from the tree label
    """
    def writeJessRule(self, f, label):
        print(label)
        f.write('(assert ({}))'.format(label))
        f.write('\n')
        
"""
http://stackoverflow.com/questions/4576077/python-split-text-on-sentences
"""
def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

if __name__ == '__main__':
    nltkSolver = nltkTextParser('text.txt', 'grammar.cfg')
    nltkSolver.makeFacts('facts.clp')