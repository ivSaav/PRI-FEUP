import pandas as pd
from pathlib import Path
from time import sleep

def reduce_plot(lst_str):
    
    if (len(lst_str) > 1800):
        return list(str(min(eval(lst_str), key=len)))
    return lst_str
    

def data_processing():

    # sleep(1)

    df = pd.read_csv(Path('./data/imdb_final.csv'))   # imdb data

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

    out_path = Path('./data/imdb_final.csv')
    df.to_csv(out_path, index=False, index_label='id') # save final version


if __name__ == '__main__':
    final = data_processing()
