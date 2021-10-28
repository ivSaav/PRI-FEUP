import pandas as pd

from imdb import IMDb, IMDbError

def fetch_plots(df):

    ia = IMDb()
    df['plot'] = '' # add new column for plots

    for idx, row in df.iterrows():
        try:
            print('\n\n#############################')
            print(idx, row['title'])
            # search movie by title on IMDb
            movie_search = ia.search_movie(row['title'])
            movie = ia.get_movie(movie_search[0].movieID, info=['plot'])
            df['plot'][idx] = min(movie['plot'], key=len) if 'plot' in movie else '' # assign plot to respective movie
            print(df['plot'][idx])

        except IMDbError as e:
            print('[X] Error for: ', row['title'])
            print('-------\n', e)


def data_processing():

    df = pd.read_csv('./data/imdb.csv')

    # renaming first column (edit csv maybe?)
    df = df.rename(columns= {'Unnamed: 0' : 'id'})

    print(f'NaN values: {df.isnull().sum().sum()} | DF size: {len(df)}')

    # removing rows pertaining to video games
    df = df.loc[df['kind'] != 'video game']
    
    # removing rows with NaN values
    df = df.dropna(axis=0, subset=['title', 'year', 'kind', 'genre', 'rating'])
    print('[-] Removed NaN values')
    print(f'NaN values: {df.isnull().sum().sum()} | DF size: {len(df)}')

    fetch_plots(df)


if __name__ == '__main__':
    data_processing()
