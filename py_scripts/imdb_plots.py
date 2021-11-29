import pandas as pd

from imdb import IMDb, IMDbError
from pandas.core.frame import DataFrame
from time import time

def fetch_plots(col_name='plot', m_info='plot'):

    ia = IMDb()

    original_df = pd.read_csv('./data/imdb.csv')
    original_df.rename(columns= {'Unnamed: 0' : 'id'}, inplace=True)

    print(original_df.head)

    plots_dict = {'id': list(), 'title': list(), 'plot': list()}

    total = len(original_df)
    start = time()
    err_cnt = 0
    no_plt = 0
    cnt = 0
    for _idx, row in original_df.iterrows():
        try:
            # search movie/show by title on IMDb
            movie_search = ia.search_movie(f"{row['title']} ({row['year']})" )
            if (len(movie_search) <= 0):
                no_plt += 1
                continue

            print(movie_search)

            movie = ia.get_movie(movie_search[0].movieID, info=m_info)

            # print(movie['synopsis'])

            plots_dict['id'].append(row['id'])
            plots_dict['title'].append(row['title'])

            print(movie['runtime'])

            print("----------------------")
            print(f'[{row["id"]}/{total}] {row["title"]}')
            if m_info in movie:
                plots_dict[col_name].append(max(movie[m_info], key=len))  # assign smaller plot to respective movie/show
            else:
                plots_dict[col_name].append(None)
                print(f'[!] No {m_info} found')
                no_plt += 1   
        except:
            # print('[X] Error for: ', row['title'])
            err_cnt += 1
            pass
            

    # plots_df = DataFrame(plots_dict)
    # plots_df.to_csv(f'imdb_plots.csv', index=False)
    
    diff = time() - start
    print('[!] Done - Elapsed Time: %02d:%02d' % (diff // 60, (diff % 60)))
    print('Errors: ', err_cnt, 'Missing plots: ', no_plt)

if __name__ == "__main__":
    fetch_plots(col_name='plot', m_info='plot')