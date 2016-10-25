# -*- coding: utf-8 -*-

'''
Created on 24 oct. 2016

@author: Antoine de Chassey
'''

import nltk
from nltk import *

#with open('data.txt', 'r', encoding='utf-8') as myfile:
    #tokens = myfile.read().replace('\n', '').replace('.', '').replace(',', '').split()
   
text = open('data.txt').read()

# Permet de retirer la ponctuation
tokens_sentences = sent_tokenize(text)

with open ("test.cfg", "r", encoding='utf-8') as myfile:
        grammaireText=myfile.read()
    
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

