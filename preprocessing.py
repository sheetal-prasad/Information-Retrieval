# -*- coding: utf-8 -*-
"""
Created on Sat May  2 14:32:06 2020

@author: Sheetal
"""
import nltk, string, re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

def tokenizer_fun(strng):
    tokenizer =str.maketrans(dict.fromkeys(string.punctuation))
    cleaned_data=strng.translate(tokenizer)
    a=re.sub('[0-9]+','',cleaned_data)
    op=word_tokenize(a)
    op1 = [ele.lower() for ele in op]
    no_integers = [x for x in op1 if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]
    return no_integers

#Function to remove stopwords from the list of tokens . Stopwords are imported from nltk.corpus
def remove_stopwords(tokens):
    filteredwords = tokens[:]
    for word in tokens:
        if word in stopwords.words('english'):
            filteredwords.remove(word)
    return filteredwords

#Function to stem the tokens using porter stemmer 
def stemming(tokens):
    ps = PorterStemmer()
    StemmedWords= [ps.stem(words) for words in tokens]
    return StemmedWords

def length2(tokens):
    filter_len = []
    for words in tokens:
        if len(words) >2 :
            filter_len.append(words)
    return filter_len
