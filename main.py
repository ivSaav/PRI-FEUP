import pandas as pd

def data_processing():

    # TODO: merge plots with imdb data

    df = pd.read_csv('./data/imdb.csv')

    # renaming first column
    df = df.rename(columns= {'Unnamed: 0' : 'id'}, inplace=True)
    print(f'NaN values: {df.isnull().sum().sum()} | DF size: {len(df)}')

    # removing rows pertaining to video games
    df = df.loc[df['kind'] != 'video game']
    
    # removing rows with NaN values
    df = df.dropna(axis=0, subset=['title', 'year', 'kind', 'genre', 'rating'])
    print('[-] Removed NaN values')
    print(f'NaN values: {df.isnull().sum().sum()} | DF size: {len(df)}')

    pd.to_csv('imdb_final.csv') # save final version



if __name__ == '__main__':
    data_processing()
