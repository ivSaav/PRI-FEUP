import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import seaborn as sns

out_dir = Path('./img/')
sns.set_theme(style='darkgrid')


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
    s = s.sort_values(by=['rating'], ascending=False)
    s.drop('rating_votes', axis=1, inplace=True)
    print(s.head(size))

def genre_hist(df):
    # turning string values into propper list values
    df['genre'] = df['genre'].apply(eval)
    _fig, ax = plt.subplots(figsize=(12, 6))
    genre_1D = to_1D(df['genre'])
    genre_1D = genre_1D.to_frame(name='genre')
    sns.countplot(data=genre_1D, y='genre', order=genre_1D['genre'].value_counts().index, palette=sns.color_palette('YlOrRd'))
    ax.set_ylabel('Genre')
    ax.set_xlabel('Count')
    plt.savefig(out_dir / 'genre_hist')
    plt.close()

    return genre_1D

def density_plot(df, field, xlabel, lower=None, upper=None):
    ratings = df[field]
    ax = sns.histplot(ratings, color='#CC2600', bins=10)
    ax.set_xlabel(xlabel)
    # ratings.plot(kind='density', xlim=(lower, upper))
    # plt.xlabel(xlabel)
    plt.xlim(0, 10)
    plt.savefig(out_dir / f'{field}_hist')
    plt.close()

def year_counts(df, field):
    counts = df['year'].value_counts().rename_axis('year').to_frame('counts')
    ax = sns.lineplot(data=counts, x='year', y='counts', color='#CC2600')
    plt.xlim(1920, 2021)
    plt.ylim(0, None)
    ax.set_xlabel('Year')
    ax.set_ylabel('Counts')

    plt.savefig(out_dir / f'{field}_line_plot')
    plt.close()

def top_actors(df):
    tmp = df.dropna(subset=['cast'])
    tmp['cast'] = tmp['cast'].apply(eval)

    print(type(tmp['cast'][0]))
    members = to_1D(tmp['cast']).value_counts()

    # print(members.head(50))
    # print(to_1D(df['cast']).value_counts())


def plot_size(df):
    tmp = df[['kind', 'plot']].copy()
    tmp['length'] = df['plot'].apply(len)
    

    plt.figure(figsize=(11, 8))
    # print(sorted(tmp))
    ax = sns.boxplot(data=tmp, x='length', y='kind', palette=sns.color_palette('YlOrRd', n_colors=4))
    ax.set_xlabel('Plot Length')
    ax.set_ylabel('Kind')
    plt.savefig(out_dir / 'plot_size_boxplots')
    plt.close()
    print(tmp)

def boolean_df(item_lists, unique_items):# Create empty dict
    # from: https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173
    bool_dict = {}
    
    # Loop through all the tags
    for i, item in enumerate(unique_items):
        
        # Apply boolean mask
        bool_dict[item] = item_lists.apply(lambda x: item in x)
            
    # Return the results as a dataframe
    return pd.DataFrame(bool_dict)

def plot_heatmap(df):
    
    # from: https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173
    df['genre'] = df['genre'].apply(eval)
    unique_items = to_1D(df['genre']).value_counts()
    genres_bool = boolean_df(df['genre'], unique_items.keys())
    genres_corr = genres_bool.corr(method = "pearson")
    genres_int = genres_bool.astype(int)
    genres_freq_mat = np.dot(genres_int.T, genres_int)

    genres_freq = pd.DataFrame(genres_freq_mat, columns = unique_items.keys(), index = unique_items.keys())

    import seaborn as sn
    fig, ax = plt.subplots(figsize = (9,5))
    sn.heatmap(genres_freq, cmap = "Blues")
    plt.xticks(rotation=50)
    plt.savefig("heatmap.png", dpi = 300)

def pie_plot(df):

    perc_df = df['kind'].value_counts().to_frame('count')
    perc_df.index.rename('kind', inplace=True)
    perc_df['perc'] = perc_df['count'] / len(df)

    lables = []
    for x in list(perc_df.index):
        tmp = x.split(' ')
        tmp = [i.capitalize() for i in tmp]
        lables.append(' '.join(tmp))

    # lables = [x.capitalize() for x in list(perc_df.index)]
    plt.figure(figsize=(11, 8))
    colors = sns.color_palette('YlOrRd')
    plt.pie(x=perc_df['perc'], labels=lables, colors=colors, autopct='%.0f%%', normalize=True)
    plt.savefig(out_dir / 'pie_chart')
    plt.close()

def general_analysis(df, field):
    print("\n====== " + field.capitalize() + " ======")
    
    # tmp = df.dropna(subset=[field]).copy()
    tmp = df.copy()
    tmp[field].fillna("[]", inplace=True)
    tmp[field] = tmp[field].apply(eval).copy()

    tmp['size'] = tmp[field].apply(len)

    actor_freq = to_1D(tmp[field]).value_counts()

    print('total', len(actor_freq))
    print('max ', tmp['size'].max())
    print('avrg', tmp['size'].mean())
    print('missing', len(tmp.loc[tmp['size'] == 0]))

    
    


    


def data_analysis():

    df = pd.read_csv(Path('./data/imdb_final.csv'))   # imdb data


    genre_1D = genre_hist(df)
    general_analysis(df, 'cast')
    general_analysis(df, 'director')
    general_analysis(df, 'composer')
    general_analysis(df, 'writer')
    general_analysis(df, 'country')
    general_analysis(df, 'language')
    # plot_heatmap(df)    
    
    plot_size(df)
    
    # plt.savefig('kind_counts')

    # top 100 programs
    top_shows(df, 100, 'movie')

    density_plot(df, 'rating', 'Rating', lower=1, upper=10)
    year_counts(df, 'year')
    # density_plot(df, 'year', 'Year', lower=1900, upper=2020)

    # runtime_comparison(df)
    # top_actors(df)
    plot_size(df)

    pie_plot(df)
    
    print(df['rating'].describe())



if __name__ == "__main__":
    data_analysis()