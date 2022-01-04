import pandas as pd
import re

from imdb import IMDb, IMDbError
from pandas.core.frame import DataFrame
from time import time

import requests

import os

def dimin():
    
    stop = ['of', 'the', 'a']

    original_df = pd.read_csv('./data/imdb_final.csv')
    original_df.rename(columns= {'Unnamed: 0' : 'id'}, inplace=True)

    # print(original_df.head)
    out_f = open("dims_synonyms.txt", "w",encoding='utf-8')

    dims_dict = {}
    for _idx, row in original_df.iterrows():
        title = row['title']
        # print(title)
        if (":" in title):
            title = title[:title.index(":")]
            
        s = title.split(" ")

        if (s[0].lower() in stop):
            s = s[1:]
            print(s)
        if (s[-1].lower() in stop):
            s = s[:-1]
        
        dim = ""
        for word in s:
            dim += word[0].upper()
              
        dim = re.sub("[^a-zA-Z0-9]+", "",dim)
        
        if (len(dim) < 2):
            continue
        dims_dict.setdefault(dim, list())
        dims_dict[dim].append(title)
        
    for (k, v) in dims_dict.items():
        # print(k)
        line = f"{k.lower()} => "
        
        v = [x.lower() for x in v]
        line += ", ".join(v)
        out_f.write(line + "\n")
        
        

    
        
dimin()
        
        
