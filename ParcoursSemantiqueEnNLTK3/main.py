  # -*- coding: utf-8 -*-

'''
Created on 24 oct. 2016

@author: Antoine de Chassey
'''

from nltk import *
import nltk

class nltkTextParser():
    
    def __init__(self, grammarFile, textFile):
        self.grammarFile   = grammarFile
        self.sentencesFile = textFile
    
    """
    Read text and process defined grammar
    """
    def readText(self, grammarFile, textFile):
    # with open('data.txt', 'r', encoding='utf-8') as myfile:
        # tokens = myfile.read().replace('\n', '').replace('.', '').replace(',', '').split()
        text = open(textFile).read()
        
        # Permet de retirer la ponctuation
        tokens_sentences = sent_tokenize(text)
        
        with open (grammarFile, "r", encoding='utf-8') as myfile:
                grammaireText = myfile.read()
            
        grammar = grammar.FeatureGrammar.fromstring(grammaireText)
        parser = nltk.ChartParser(grammar)
        parser = parse.FeatureEarleyChartParser(grammar)
            
        for sentence in tokens_sentences:
            tokens_words = RegexpTokenizer(r'\w+').tokenize(sentence)
            print(tokens_words)
            
            trees = parser.parse(tokens_words)
            for tree in trees:
                print(tree)
                nltk.draw.tree.draw_trees(tree)
                print(tree.label()["SEM"])
            
    """
    Build an output file with facts
    """
    def makeFacts(self, outputFile):
        self.factsCount = 0
        with open(outputFile, 'w') as f:
            for sentence in self.sentences:
                sanitizedSentence = self.sanitizeSentence(sentence)
    
                if sentence.startswith('#'):
                    print('Skipping <{0}>'.format(sanitizedSentence))
                    continue
        
                print('Parsing <{0}>'.format(sanitizedSentence))
        
                trees = self.parse(sanitizedSentence)
        
                if len(trees) > 1:
                    self.ambiguous.append(sanitizedSentence)
                elif len(trees) == 0:
                    self.notDefined.append(sanitizedSentence)
        
                for tree in trees:
                    label = tree.label()['SEM']
                    self.writeRule(f, str(label))
                    print(tree)
                    # tree.draw()
                
if __name__ == '__main__':
    nltk = nltkTextParser.readText('grammar.cfg', 'text.txt')
    nltk.makeFacts('facts.clp')
