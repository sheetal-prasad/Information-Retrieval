# -*- coding: utf-8 -*-
"""
Created on Sat May  2 13:50:48 2020

@author: Sheetal
Using parts of code from HW2
"""
import pickle_functions as pk
import math
import preprocessing as pro

#global variables
inverted={}
documents={}
max_freq={}
cosine={}
len_dict={}
q_tf={}
N =0 

def score(pageranks, query):
	prob_query = {}
	ranks = {}
	for word in query:
		prob_query[word] = 1/len(query)
	for doc in pageranks:
		ranks[doc] = sum(prob_query[word]*pageranks[doc][word] if word in pageranks[doc] else 0 for word in query)
	return ranks

def cosine_sim(query,doclen,querylen):
    global cosine
    unique=list(set(query))
    for qtoken in unique:
        try:
            for docno in inverted[qtoken][1]:
                if docno not in cosine:
                    tf=inverted[qtoken][1][docno]/max_freq[docno]
                    idf=math.log((N/inverted[qtoken][0]),2)
                    cosine[docno]=(tf*idf)*(q_tf[qtoken]*idf)
                else:
                    tf=inverted[qtoken][1][docno]/max_freq[docno]
                    idf=math.log((N/inverted[qtoken][0]),2)
                    cosine[docno] +=(tf*idf)*(q_tf[qtoken]*idf)
        except:
            print(qtoken+" is not available in the documents")
#sorting the cosine dictionary based on value and creating a list of keys
    for doc in cosine:
        cosine[doc]=cosine[doc]/(doclen[doc]*querylen)
    ranking=[k for k,v in sorted(cosine.items(), reverse=True, key=lambda k:k[1])]
    return ranking


def qtf_idf(query):
    unique=list(set(query))
    qlen=[]
    global q_tf
    for q in unique:
        if q in query:
            qtf=query.count(q)
            qlen.append(qtf)
            q_tf.update({q:qtf})
    qweight=0
    for ele in qlen:
        qweight+=(ele*ele)
    length=math.sqrt(qweight)
    return length

def tf_idf(doc,text):
    unique=list(set(text))
    doclen=[]
    for word in unique:
        if word in inverted:
            idf=math.log((N/inverted[word][0]),2)
            temp=inverted[word][1]
            tf=temp[doc]/max_freq[doc]
            doclen.append(tf*idf)
    weight=0
    #calculation of length 
    for ele in doclen:
        weight += (ele*ele)
    length= math.sqrt(weight)
    return length

def inverted_index(docno,text):
    global inverted
    for ele in set(text):
        if ele not in inverted:
            inverted[ele]=[1,{docno:text.count(ele)}]
        else:
            present=inverted[ele][1]
            present[docno]=text.count(ele)
            inverted[ele]=[inverted[ele][0]+1,present]
            
def process_query(query):
    cleaned_query= pro.tokenizer_fun(query)
    cleaned_query= pro.remove_stopwords(cleaned_query)
    cleaned_query= pro.stemming(cleaned_query)
    return cleaned_query

def cosine_calc(query):
    cleaned_query=process_query(query)
    len_qdict=qtf_idf(cleaned_query)
    cosine_rank=cosine_sim(cleaned_query,len_dict,len_qdict)
    return cosine_rank
    
def page_rank_calc(query):
    cleaned_query=process_query(query)
    pageranks=pk.open_pickle('qdpr.pkl')
    pr_rank=score(pageranks,cleaned_query)
    qdpr_rank=[k for k,v in sorted(pr_rank.items(), reverse=True, key=lambda k:k[1])]
    #print(len(cosine_rank))
    return qdpr_rank

def main(query,ranker):
    crawler_tuple=pk.open_pickle("crawler_tuple_pages.pkl")
    global inverted
    global documents
    global max_freq
    global cosine
    global N
    global len_dict
    
    for url in crawler_tuple.keys():
        N +=1
        a,b=url, crawler_tuple[url][1]
        documents.update({a:b})
        inverted_index(a,b)
        res = max(set(b), key = b.count)
        max_freq.update({a:(b.count(res))})   
    len_dict={}   
    for docno,file in documents.items():
        val=tf_idf(docno,file)
        len_dict.update({docno:val})
    #print(len_dict)
    if(ranker=='cosine'):
        return cosine_calc(query)
        #print("cosine ranking")
    elif(ranker=='PageRank'):
        return page_rank_calc(query)
        #print('pagerank')

#print(len(main('computer','cosine')))
#print(len(main('computer','PageRank')))