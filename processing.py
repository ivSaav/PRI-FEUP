import pandas as pd
from pathlib import Path
from time import sleep

def data_processing():

    sleep(1)

    df = pd.read_csv(Path('./data/imdb_final.csv'))   # imdb data

    # removing duplicate entries from dataset
    df = df.drop_duplicates(subset=['title', 'year', 'kind', 'genre', 'rating'])
    print('[-] Removed duplicate entries | New DF size: ', len(df))

    # removing entries that don't have any plots
    df = df[df.astype(str)['plot'] != '[]']
    print('[-] Removed entries with no plots | New DF size: ', len(df))

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
