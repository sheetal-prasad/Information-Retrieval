# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 10:45:18 2020

@author: Sheetal
UIN: 677918305

Python Program to Crawl the web and scrape the web pages 
"""
from urllib.parse import urlparse,urljoin
from urllib.request import urlopen
import requests,os,re

from bs4 import BeautifulSoup

import pickle_functions as pk
import preprocessing as process


page_num = 0

def scrape (visited,vocab) :
    i=0
    for url in visited:
        try:
            response = urlopen("http://"+url)
            print("scraping",i)
            i+=1
        except:
            continue
        base = [urlparse(u).netloc for u in url]    
        bs = BeautifulSoup(response,'html.parser')
        try:
            title = bs.find('title').text
        except :
            continue
        tags=['p','span','h1','h2','h3','h4','h5','h6','div']
        if(title):
            content=title
        else:
            content=''
        for tag in tags:
            text_tag=bs.find_all(tag)
            textContent=[x.text for x in text_tag]
            content +=' '.join(textContent)
        
        page_content[url] = {'data':content} 
        content = re.sub('\n',' ',content)

        tokens = process.tokenizer_fun(content)
        cleaned = process.remove_stopwords(tokens)
        stemmed = process.stemming(cleaned)
        cleaned2 = process.remove_stopwords(stemmed)
        cleaned_text = process.length2(cleaned2)

        word_count[url] = {}
        v_flag = True
        for token in cleaned_text:
            
            if token not in vocab:
                vocab[token] = 1
            elif v_flag:
                vocab[token] += 1
                v_flag = False
                
            if token in word_count[url].keys():
                word_count[url][token] += 1
            else:
                word_count[url][token] = 1
                
        links = [urljoin(url, l.get('href')) for l in bs.findAll('a')]
        links = [l.rstrip("/") for l in links if urlparse(l).netloc in base]
        finalData = (url,cleaned_text,list(set(links)))
        if finalData != (-1) :
            crawler_tuple[url] = finalData

    return crawler_tuple


if __name__ == "__main__":

    page_content = {} #key: url and value:contents of web page
    starting_url = "https://www.cs.uic.edu/"
    search_limit =3000 # number of web pages to be collected 
    uic_domain = "uic.edu"
    url_queue = []
    skip_exten=['.jpeg','.jpg','.png','.gif','.JPG','.pdf','.doc', '.mp4','.ico','favicon','mailto:','.svg','.css', '.js']
    page_num = 0
    links_dict = {} #key: pageno, value: url
    word_count = {}
    vocab = {}
    crawler_tuple = {}
    visited = set()    
    
    path = os.getcwd()
    if not (os.path.isfile('crawler_tuple_pages.pkl') and os.path.isfile('word_count.pkl') and os.path.isfile('vocab.pkl')):

        url_component = urlparse(starting_url)
        url_queue.append((url_component.netloc).lstrip("www."))
        #BFS algorithm is implementted using visited and Url_queue
        while(url_queue):
            url = url_queue.pop(0)
            if url not in visited:
                visited.add(url)
                try:
                    response = requests.get("http://"+url)
                    if(response.status_code == 200):                    
                        links_dict[page_num] = url
                        page_num += 1
                        bs = BeautifulSoup(response.text, 'html.parser')
                        a_tags = bs.find_all('a')
                        for a in a_tags:
                            try:
                                if(re.search('.+?uic.edu',a["href"]) != None):
                                    if not any(ext in a["href"] for ext in skip_exten):
                                        parse = urlparse(a["href"])
                                        temp_href = ((parse.netloc+parse.path).lstrip("www.").rstrip("/"))
                                        if(uic_domain in a["href"] and temp_href not in links_dict.values() and temp_href not in visited):
                                            url_queue.append(temp_href)
                                                
                            except:
                                continue
                        
                        print(page_num)
                        if(page_num>search_limit):
                            break
                except:
                    print("Connection failed for ", url)
                    continue
        web_crawler = scrape(visited,vocab) 
        pk.save_pickle('crawler_tuple_pages.pkl',web_crawler)
        pk.save_pickle('word_count.pkl',word_count)
        pk.save_pickle('vocab.pkl',vocab)  
        pk.save_pickle('page_content.pkl',page_content)

    else:
        web_crawler = pk.open_pickle('crawler_tuple_pages.pkl')
        word_count = pk.open_pickle('word_count.pkl')
        vocab = pk.open_pickle('vocab.pkl')
        page_content = pk.open_pickle('page_content.pkl')
