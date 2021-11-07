import pandas as pd
from pathlib import Path

import matplotlib.pyplot as plt

def data_processing():

    data = pd.read_csv(Path('./data/imdb.csv'))   # imdb data
    # renaming first column
    data.rename(columns= {'Unnamed: 0' : 'id'}, inplace=True)
    print(f'NaN values: {data.isnull().sum().sum()} | DF size: {len(data)}')

    plts = pd.read_csv(Path('./data/imdb_plots.csv')) # read imdb plots
    # adding plots to the original data
    df = pd.merge(data, plts, on=['id', 'title'] )

    # removing rows pertaining to video games
    df = df.loc[df['kind'] != 'video game']
    
    # removing rows with NaN values
    df = df.dropna(axis=0, subset=['title', 'year', 'kind', 'genre', 'rating'])
    print('[-] Removed NaN values')
    print(f'NaN values: {df.isnull().sum().sum()} | DF size: {len(df)}')

    out_path = Path('./data/imdb_final.csv')
    df.to_csv(out_path, index=False, index_label='id') # save final version


if __name__ == '__main__':
    final = data_processing()
