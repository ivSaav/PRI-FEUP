from numpy import dtype
import pandas as pd
from pathlib import Path
from time import sleep
import json
import csv

def reduce_plot(lst_str):
    
    if (len(lst_str) > 1800):
        return list(str(min(eval(lst_str), key=len)))
    return lst_str


def handle_list_fields(row, fields):
    for field in fields:
        if row[field] == "":
            row[field]= []
        else:
            row[field] = eval(row[field])
    
def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 
        

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            handle_list_fields(row, ['genre', 'country', 'language', 'cast', 'writer', 'plot', 'director', 'composer'])
            jsonArray.append(row)
  
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4, ensure_ascii=False)
        jsonf.write(jsonString)

def data_processing():

    # sleep(1)

    # df = pd.read_csv(Path('./data/imdb_final.csv'), encoding='utf-8')   # imdb data
    
    df = pd.read_pickle(Path('./data/imdb_final.csv'))    

    # removing duplicate entries from dataset
    df = df.drop_duplicates(subset=['title', 'year', 'kind', 'genre', 'rating'])
    print('[-] Removed duplicate entries | New DF size: ', len(df))

    # removing entries that don't have any plots
    df = df[df.astype(str)['plot'] != '[]']
    print('[-] Removed entries with no plots | New DF size: ', len(df))

    # removing rows pertaining to video games
    df = df.loc[(df['kind'] != 'video game') & (df['kind'] != 'tv short')]

    # normalizing movie subtypes
    df.loc[(df['kind'] == 'video movie') | (df['kind'] == 'tv movie'), 'kind'] = 'movie'

    
    df['plot'] = df['plot'].apply(reduce_plot)
        
    df['plot_size'] = df['plot'].apply(len)

    df = df.loc[df['plot_size'] < 1750]
    df.drop('plot_size', axis=1, inplace=True)
    
    
    # removing rows with NaN values
    df = df.dropna(axis=0, subset=['title', 'year', 'kind', 'genre', 'rating'])
    print('[-] Removed NaN values')
    print(f'NaN values: {df.isnull().sum().sum()} | DF size: {len(df)}')
    
    df['year'] = df['year'].apply(int)
    df['vote'] = df['vote'].apply(int)

    df.to_csv(Path('./data/imdb_final.csv'), index=False, index_label='id', encoding='utf-8') # save final version
    # df.to_json(Path('./data/imdb_final.json'), orient='records')
    
    csv_to_json(Path('./data/imdb_final.csv'), Path('./data/imdb_final.json'))


if __name__ == '__main__':
    final = data_processing()
