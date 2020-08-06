# -*- coding: utf-8 -*-
"""
Created on Fri May  1 15:59:17 2020

@author: Sheetal
"""
import pickle_functions as pk
import os

def inlinkFunc(tfidf,crawled):
    inlink ={}

    for url in tfidf:
        inlink[url] = []
        for crawlUrl in crawled:
            if url in crawled[crawlUrl][2]:
                inlink[url].append(crawled[crawlUrl][0]) 

    return inlink

def pqitoj(term, i, j, tfidf):
    s = 0
    for doc in crawler_tuple[i][2]:
        if doc in tfidf and term in tfidf[doc]:
            s += tfidf[doc][term]

    return (tfidf[j][term] if term in tfidf[j] else 0)/s

def qdpr(tfidf, crawled, inlink):
    df = 0.85 #damping factor
    qdpr_dict = {}

    for url in tfidf:
        qdpr_dict[url] = {}
        for token in tfidf[url]:
            qdpr_dict[url][token] = 1/len(tfidf[url])
    
    count = 0

    while( count < 10) :        
        for url in tfidf:            
            for token in tfidf[url]:               
                s = 0
                for i in inlink[url]:
                    s += (qdpr_dict[i][token] if token in qdpr_dict[i] else 0) * pqitoj(token, i, url, tfidf)
                prQuery = tfidf[url][token]/ sum(tfidf[i][token] if token in tfidf[i] else 0 for i in tfidf)  
                qdpr_dict[url][token] = (1 - df) * prQuery + (df * s)
        count += 1
    return qdpr_dict

if __name__ == "__main__":

    crawler_tuple = pk.open_pickle("crawler_tuple_pages.pkl")
    tfidf = pk.open_pickle("tfidf.pkl")
    
    if os.path.exists('inlink.pkl'):
        inlink = pk.open_pickle("inlink.pkl")
    
    else:
        inlink = inlinkFunc(tfidf,crawler_tuple)
        pk.save_pickle("inlink.pkl",inlink)

    qdpr_fin = qdpr(tfidf, crawler_tuple, inlink)
    print(qdpr_fin)
    pk.save_pickle("qdpr.pkl",qdpr_fin)   
    qr = pk.open_pickle('qdpr.pkl')