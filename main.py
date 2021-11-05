import pandas as pd
from pathlib import Path

def data_processing():

    # TODO: merge plots with imdb data

    in_path = Path('./data/imdb.csv')
    df = pd.read_csv(in_path)

    # renaming first column
    df.rename(columns= {'Unnamed: 0' : 'id'}, inplace=True)
    print(f'NaN values: {df.isnull().sum().sum()} | DF size: {len(df)}')

    # removing rows pertaining to video games
    df = df.loc[df['kind'] != 'video game']
    
    # removing rows with NaN values
    df = df.dropna(axis=0, subset=['title', 'year', 'kind', 'genre', 'rating'])
    print('[-] Removed NaN values')
    print(f'NaN values: {df.isnull().sum().sum()} | DF size: {len(df)}')

    out_path = Path('./data/imdb_final.csv')
    df.to_csv(out_path, index=False, index_label='id') # save final version



if __name__ == '__main__':
    data_processing()
