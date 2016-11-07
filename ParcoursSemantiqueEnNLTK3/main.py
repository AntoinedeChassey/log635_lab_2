  # -*- coding: utf-8 -*-

'''
Created on 24 oct. 2016

@author: Antoine de Chassey
'''

import re
from nltk import *
import nltk

caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

class nltkTextParser:
    def __init__(self, textFile, grammarFile):
        self.textFile = textFile
        self.grammarFile   = grammarFile

        self.sentences = []
        self.ambiguous = []
        self.notDefined = []
        
        self.loadSentences()
        self.loadGrammar()
    
    """
    Load the text file and create an array of sentences
    """
    def loadSentences(self):
        with open (self.textFile, "r", encoding='utf-8') as myfile:
                text = myfile.read()
                self.sentences = split_into_sentences(text)
        print(self.sentences)
        
    """
    Load the grammar file parse it in NLTK
    """
    def loadGrammar(self):
        with open(self.grammarFile, 'r') as f:
            my_grammar = grammar.FeatureGrammar.fromstring(f.read())
            self.parser = nltk.FeatureEarleyChartParser(my_grammar)
            
    """
    Generate an output file for all the rules
    """
    def makeFacts(self, outputFile):
        with open(outputFile, 'w') as f:
            for sentence in self.sentences:
                sanitizedSentence = self.sanitizeSentence(sentence)
        
                print('Parsing <{}>'.format(sanitizedSentence))
        
                trees = self.parse(sanitizedSentence)
        
                if len(trees) > 1:
                    self.ambiguous.append(sanitizedSentence)
                elif len(trees) == 0:
                    self.notDefined.append(sanitizedSentence)
        
                for tree in trees:
                    self.writeJessRule(f, str(tree.label()['SEM']))
                    print(tree)
                    tree.draw()

    def stats(self):
        print("{} ambiguous sentences".format(len(self.ambiguous)))
        for s in self.ambiguous:
            print("- {}".format(s))
    
        print("{} sentences that the grammar cannot define".format(len(self.notDefined)))
        for s in self.notDefined:
            print("- {}".format(s))
        
        print("{} jess compatible facts generated".format(self.factsCount))

    """
    Returns a list of tokens from sentence
    """
    def sanitizeSentence(self, sentence):
        sanitizedSentence = re.sub(r'(\.|\,|\'|\#)', ' ', sentence).strip('\r\n').strip()
        return sanitizedSentence

    """
    Returns a list of trees generated from the sentence
    RegEx: https://regex101.com/r/nG1gU7/27
    """
    def parse(self, sentence):
#         (?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s
#         tokens = RegexpTokenizer(r'\w+').tokenize(sentence)
#         return list(tokens)
        tokens = sentence.split()
        return list(self.parser.parse(tokens))

    
    """
    Generate the jess rule from the generated sentence label
    """
    def writeJessRule(self, f, label):
        f.write('; {}\n'.format(label))
                    
#         # remove trailling ( )
#         if label.startswith('('):
#             label = label[1:len(label) - 1]
#         
#         # Add unknown subjects? This is sketchy...
#         # this should have been done on the grammar side, but ¯\_(ツ)_/¯
#         i = 0
#         for match in re.findall(r'\\\w\.', label):
#             char = match.strip('\\.')
#         
#             label = label.replace(match, '')
#             label = label.replace(char + ',', 'personne{0},'.format(i))
#             i += 1
#         
#         # Extract & into seperate facts an get the first subject
#         # Usually the first subject is the first argument
#         # This is even more sketchy :/
#         subLabels = label.split('&')
#         if subLabels and len(subLabels) > 1:
#             match = re.search(r'\w+\((\w+\(\w+\))\)?', label)
#             subject = camelCase(re.sub(r'\(|\)', ' ', match.group(1)))
#             for l in subLabels:
#                 self.writeJessRule(f, l, subj = subject)
#         
#         if subj:
#             for match in re.findall(r'\?\w+', label):
#                 label = label.replace(match, subj)
#         
#         # We match stuff like abc(abc,abc) and replace it by AbcAbcAbc == multiple args facts
#         pattern = r'\w+\(\w+(?:,\w+)*\)'
#         matches = re.findall(pattern, label)
#         while matches:
#             for match in matches:
#                 tokens = list(filter(None, re.split(r'\(|,|\)', match)))
#                 fact = ' '.join(tokens)
#                 self.factsCount += 1
#                 f.write('({0})\n'.format(fact))
#         
#                 _camelCase = camelCase(fact)
#                 label = label.replace(match, _camelCase)
#         
#             matches = re.findall(pattern, label)
        
        f.write('\n')

"""
http://stackoverflow.com/questions/8347048/camelcase-every-string-any-standard-library
abc def returns AbcDef
"""
def camelCase(string):
    return ''.join(x for x in string.title() if not x.isspace())
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
    #nltkSolver.readText()
    nltkSolver.makeFacts('facts.clp')
#     makeFacts('facts.clp')
