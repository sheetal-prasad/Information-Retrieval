# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 22:01:39 2020
Spell checker for search engine

@author: Sheetal
"""
import re
from collections import Counter

def simple_edit(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    split=[]
    delete=[]
    transpose=[]
    replace=[]
    insert=[]
    for i in range(len(word)+1):
        split.append((word[:i],word[i:]))
    for L,R in split:
        if R:
            delete.append(L+R[1:])
        if len(R)>1:
            transpose.append(L + R[1] + R[0] + R[2:])
        for c in letters:
            if R:
                replace.append(L + c + R[1:])
            insert.append(L+c+R)  
    return set(delete + transpose + replace + insert)

def words(text): 
    return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('dictionary.txt').read()))

def Prob(word, N=sum(WORDS.values())): 
    return WORDS[word] / N

def spell_check(word): 
    return max(candidates(word), key=Prob)

def candidates(word): 
    return (known([word]) or known(simple_edit(word)) or known(two_edits(word)) or [word])

def known(words): 
    return set(w for w in words if w in WORDS)

def two_edits(word): 
    return (e2 for e1 in simple_edit(word) for e2 in simple_edit(e1))

def main_speller(query):
    string= query.split()
    corrected=[]
    for word in string:
        corrected.append( spell_check(word))

    corrected= ' '.join(corrected)
    return corrected

