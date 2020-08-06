# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:45:30 2020

@author: Sheetal
"""

import pickle

def open_pickle(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

def save_pickle(filename,obj):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)
        
if __name__ == "__main__":
    crawl=open_pickle("webcrawler.pkl")
    count=open_pickle("word_count.pkl")
    spider=open_pickle("spider.pkl")
    vocab=open_pickle("vocab.pkl")
    #webcrawled=open_pickle("tfidf.pkl")
    
    #print(len(count['uic.edu']))
