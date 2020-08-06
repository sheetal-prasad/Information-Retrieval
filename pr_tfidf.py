# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 13:50:24 2020

@author: Sheetal
Python program that calculates the tfidf for each term and computes the inlinks
"""
import math
import pickle_functions as pk

if __name__ == "__main__":

    word_count = pk.open_pickle('word_count.pkl')
    vocab = pk.open_pickle('vocab.pkl')
    crawler_tuple = pk.open_pickle('crawler_tuple_pages.pkl')

    tfidf = {}
    N = len(word_count) # N is the total number of webpages scarpped 
    for url in word_count:
        tfidf[url] = {}
        for tokens in word_count[url]:
            tf = word_count[url][tokens] / (max(word for word in word_count[url].values()))

            idf = math.log((N/vocab[tokens]),2)
            
            tfidf[url][tokens] = tf * idf
    #print(tfidf)

    pk.save_pickle('tfidf.pkl',tfidf)
    inlink ={}

    for url in tfidf:
        inlink[url] = []
        for crawlUrl in crawler_tuple:
            if url in crawler_tuple[crawlUrl][2]:
                inlink[url].append(crawler_tuple[crawlUrl][0]) 

    pk.save_pickle("inlink.pkl",inlink)
    #print(inlink)