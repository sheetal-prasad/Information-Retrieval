# -*- coding: utf-8 -*-
"""
Created on Sun May  3 12:38:42 2020

@author: Sheetal

User interface program
"""
import os
import tkinter as tk
from PIL import Image,ImageTk


import spellchecker as sp
import final_calc as calc

path=os.getcwd()
window = tk.Tk()
window.title("UIC search Engine")

frame=tk.Frame(window,width=720,height=520,bg="white" )

frame.config(background="white")
window.configure(background="white")
frame.pack()
canvas = tk.Canvas(frame, width = 720, height = 520)  
canvas.pack() 

image=Image.open(path+'\\'+'download.png')
image=image.resize((80,80), Image.ANTIALIAS)
uic_image=ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor=tk.NW, image=uic_image)

lbl1= tk.Label(frame,text="Search Engine using Cosine Simialrity and Query dependent PageRank",
            bg="white", fg='black',padx=2,pady=3,font='Helvetica 14')
lbl1.place(x=100,y=20)

lbl = tk.Label(frame, text="Type your Query here:")
lbl.place(x=10,y=100)

def clicked_cosine():
    
    i=0
    searching_cs=tk.Label(frame, text="Ranking using Cosine Similarity!")
    searching_cs.place(x=250,y=180)
    ipquery=entry.get()
    opquery=sp.main_speller(ipquery)
    query=ipquery
    if(ipquery.lower() != opquery):
        MsgBox=tk.messagebox.askyesno("Question", "Did you mean "+opquery+"?", icon='warning')
        if MsgBox:
            query = opquery
        
    links=calc.main(query,'cosine')
    results = tk.Listbox(frame,width=70,selectmode=tk.BROWSE)
    results.place(x=150,y=220)
    lim=len(links)
    
    while i<10:
        results.insert(i+1,'http://'+links[i])
        i+=1
    def load_more(j):
        global i 
        for x in range(j,j+10):
            ind=j+1
            results.insert(ind,'http://'+links[x])
            ind+=1
        if( j+10<lim):
            j=j+10
    btn3=tk.Button(frame,text="Load more results",command=lambda:load_more(i),bg='blue',fg='white')
    btn3.place(x=380,y=400)
    def clear_fun():
        entry.delete(0,'end')
        results.delete(0,tk.END)
        searching_cs.destroy()
    btn4=tk.Button(frame,text="clear search",command= clear_fun,bg='blue',fg='white')
    btn4.place(x=500,y=400)

def clicked_QDPR():
    
    i=0
    searching_pr=tk.Label(frame, text="Ranking using Query dependent Page Rank!")
    searching_pr.place(x=250,y=180)
    ipquery=entry.get()
    opquery=sp.main_speller(ipquery)  
    query=ipquery
    if(ipquery.lower() != opquery):
        MsgBox=tk.messagebox.askyesno("Question", "Did you mean "+opquery+"?", icon='warning')
        if MsgBox:
            query = opquery
            
    links=calc.main(query,'PageRank')
    results = tk.Listbox(frame,width=70,selectmode=tk.BROWSE)
    results.place(x=150,y=220)
    lim=len(links)
    
    while i<10:
        results.insert(i+1,'http://'+links[i])
        i+=1
    def load_more(j):
        global i 
        for x in range(j,j+10):
            ind=1
            results.insert(ind,'http://'+links[x])
            ind+=1
        if( j+10<lim):
            j=j+10
    btn3=tk.Button(frame,text="Load more results",command=lambda:load_more(i),bg='blue',fg='white')
    btn3.place(x=380,y=400)
    def clear_fun():
        entry.delete(0,'end')
        results.delete(0,tk.END)
        searching_pr.destroy()
    btn4=tk.Button(frame,text="clear search",command= clear_fun,bg='blue',fg='white')
    btn4.place(x=500,y=400)
    #searching_pr.destroy()
    
btn1 = tk.Button(frame, text="Cosine Ranking", command=clicked_cosine,bg='blue', fg='white')
btn1.place(x=250,y=150)

btn2=tk.Button(frame, text="QD-Page Rank", command=clicked_QDPR,bg='blue', fg='white')
btn2.place(x=350,y=150)

entry = tk.Entry(frame,width=70)
entry.place(x=150,y=100)

window.mainloop()