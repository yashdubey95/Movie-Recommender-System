# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 20:59:14 2020

@author: yashd
"""

import os
import requests
import re
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

url="https://www.imdb.com/chart/top?ref_=nv_mv_250"
os.environ['NO_PROXY'] = 'imdb.com'
req = requests.get(url)
page = req.text

soup = BeautifulSoup(page, 'html.parser')

links=[]
for a in soup.find_all('a'): #, href=True):
    links.append(a.get('href'))
links=['https://www.imdb.com'+a.strip() for a in links if a is not None and a.startswith('/title/tt') ]

#---------------------------Remove duplicates in links
top_250_links=[]
for c in links:
    if c not in top_250_links:
        top_250_links.append(c)

print(len(top_250_links))

column_list=['Rank','Movie_name' ,'URL' ,'Release_Year' ,'IMDB_Rating' ,
'Reviewer_count' ,'Censor_Board_Rating' ,'Movie_Length', 'Release_Date' ,'Genre','Story_Summary' ,
'Director' , 'Writers', 'Stars','Plot_Keywords' ,'Budget' ,
'Gross_USA' ,'Cum_Worldwide_Gross' ,'Production_Company' 
]
df = pd.DataFrame(columns=column_list)

for x in np.arange(0, 250):
    #---------------------------Load html page for 1st movie in top 250 movies

    url=top_250_links[x]
    req = requests.get(url)
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    
    #---------------------------Retrieve Movie details from html page
    Movie_name=(soup.find("div",{"class":"title_wrapper"}).get_text(strip=True).split('|')[0]).split('(')[0]
        
    year_released=((soup.find("div",{"class":"title_wrapper"}).get_text(strip=True).split('|')[0]).split('(')[1]).split(')')[0]
        
    imdb_rating=soup.find("span",{"itemprop":"ratingValue"}).text
    
    reviewer_count=int(soup.find("span",{"itemprop":"ratingCount"}).text.replace(',', ''))
    
    
    subtext= soup.find("div",{"class":"subtext"}).get_text(strip=True).split('|') #Censor_rating
    if len(subtext)<4:
        censor_rating='Not Rated'
        movie_len=subtext[0]
        genre_list=subtext[1].split(',')
        release_date=subtext[2]
    else:
        censor_rating=subtext[0]
        movie_len=subtext[1]
        genre_list=subtext[2].split(',')
        release_date=subtext[3]
        
    story_summary=soup.find("div",{"class":"summary_text"}).get_text(strip=True).strip()
    
    #---------------------------Director,Writer and Actor details
    b=[]
    for a in soup.find_all("div",{"class":"credit_summary_item"}):
        c=re.split(',|:|\|',a.get_text(strip=True))         #print("c - ",c)
        b.append(c)                                         #print(''.join(a.get_text(strip=True)))
    stars=b.pop()
    writers=b.pop()
    directors=b.pop()
    if 'See full cast & crew»' in stars: stars.remove('See full cast & crew»')
    if '1 more credit»' in writers: writers.remove('1 more credit»') 
    if '1 more credit»' in directors: directors.remove('1 more credit»')
    stars=stars[1:]
    writers=writers[1:]
    directors=directors[1:]
    
    director=directors[0]
    
    #---------------------------Plot Keywords
    b=[]
    plot_keywords = []
    for a in soup.find_all("span",{"class":"itemprop"}):     b.append(a.get_text(strip=True))  
    
    plot_keywords = b
    print(b)
    #---------------------------Commercial details and Prod Company
    
    
    b=[]                    #---------------------------Remove unwanted entries
    d={'Budget':'', 'Opening Weekend USA':'','Gross USA':'','Cumulative Worldwide Gross':'','Production Co':''}
    for a in soup.find_all("div",{"class":"txt-block"}):
        c=a.get_text(strip=True).split(':')
        if c[0] in d:
            b.append(c)

    for i in b:             #---------------------------Update default values if entries are found
            if i[0] in d: 
                d.update({i[0]:i[1]})                

    production_company=d['Production Co'].split('See more')[0]
    cum_world_gross=d['Cumulative Worldwide Gross'].split(' ')[0]
    gross_usa=d['Gross USA'].split(' ')[0]
    budget=d['Budget']
    
    #---------------------------Dictionary to holds all details
    movie_dict={
        'Rank':x+1,
        'Movie_name' : Movie_name,
        'URL' : url,
        'Release_Year' : year_released,
        'IMDB_Rating' : imdb_rating,
        'Reviewer_count' : reviewer_count,
        'Censor_Board_Rating' : censor_rating,
        'Movie_Length' : movie_len,
        'Release_Date' : release_date,
        'Genre' : genre_list,
        'Story_Summary' : story_summary,
        'Director' : director,
        'Writers' : writers,
        'Stars' : stars,
        'Plot_Keywords' : plot_keywords,
        'Budget' : budget,
        'Gross_USA' : gross_usa,
        'Cum_Worldwide_Gross' : cum_world_gross,
        'Production_Company' : production_company
        }
    
    #---------------------------Append rows to dataframes using dictionary
    df = df.append(pd.DataFrame.from_records([movie_dict],columns=movie_dict.keys() ) )
    print(x)
    
df.to_csv('dataset.csv', encoding='utf-8', index=False)    