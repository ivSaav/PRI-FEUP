import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

out_dir = Path('./img/')

def to_1D(series):
    # from: https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173
    return pd.Series([x for _list in series for x in _list])

def runtime_comparison(df):
    # TODO (problem) some tv series have runtime of episode and other have full runtime of series
    print('\n\n---Runtime Comparisons---')

    # tmp = df.loc[df['kind'] == 'tv series']
    # tmp = tmp.sort_values(by=['runtime'], ascending=False)
    # print(tmp.head())

    print(df.groupby(['kind', 'runtime']).sum().reset_index().groupby('kind').mean())

    tmp = df.loc[df['kind'] == 'movie']
    print(tmp.groupby(['genre', 'runtime']).sum().reset_index().groupby('genre').mean())


def top_shows(df, size, kind):
    """
    Displays the nth top rated movie/show\n
    df - dataframe\n
    size - number of entries to display\n
    kind - "movie" or "tv show"  
    """

    print(f'Top {size} {kind}s')
    tmp_df = df[['id', 'title', 'rating', 'vote', 'kind']].copy()
    tmp_df['rating_votes'] = tmp_df['rating'] / tmp_df['vote']
    tmp_df = tmp_df.loc[df['kind'] == kind]
    s = tmp_df.nsmallest(size, ['rating_votes'])
    s = s.sort_values(by=['rating_votes'])
    print(s.head(size))

def genre_hist(df):
    # TODO fix size
    # turning string values into propper list values
    df['genre'] = df['genre'].apply(eval)
    to_1D(df['genre']).value_counts().plot(kind='bar')
    plt.savefig(out_dir / 'genre_hist')
    plt.close()

def density_plot(df, field, xlabel, lower=None, upper=None):
    ratings = df[field]
    ratings.plot(kind='density', xlim=(lower, upper))
    plt.xlabel(xlabel)
    plt.savefig(out_dir / f'{field}_density')
    plt.close()

def top_actors(df):
    tmp = df.dropna(subset=['cast'])
    tmp['cast'] = tmp['cast'].apply(eval)

    print(type(tmp['cast'][0]))
    members = to_1D(tmp['cast']).value_counts()

    
    print(members)
    # print(to_1D(df['cast']).value_counts())


def data_analysis():

    df = pd.read_csv(Path('./data/imdb_final.csv'))   # imdb data

    # genre_hist(df)
    
    # df['kind'].value_counts().plot.bar()
    # plt.savefig('kind_counts')

    # top 100 programs
    # top_shows(df, 25, 'movie')

    # density_plot(df, 'rating', 'Rating', lower=1, upper=10)
    # density_plot(df, 'year', 'Year', lower=1900, upper=2020)

    # runtime_comparison(df)
    top_actors(df)



if __name__ == "__main__":
    data_analysis()