import pandas as pd

from imdb import IMDb, IMDbError
from pandas.core.frame import DataFrame
from time import time
import requests

import os

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
    
def fetch_covers():

    ia = IMDb()

    original_df = pd.read_csv('../data/imdb.csv')
    original_df.rename(columns= {'Unnamed: 0' : 'id'}, inplace=True)

    # print(original_df.head)
    files = set(os.listdir("../img/covers/original"))

    total = len(original_df)
    start = time()
    err_cnt = 0
    no_img = 0
    no_small_img = 0
    cnt = 0
    for _idx, row in original_df.iterrows():
        
        if f"{row['id']}.png" in files:
            print( row['id'], " - Already downloaded. Skipping.")
            continue
        try:
            # search movie/show by title on IMDb
            movie_search = ia.search_movie(f"{row['title']}" )
            if (len(movie_search) <= 0):
                no_plt += 1
                continue

            search_idx = 0
            for idx, res in enumerate(movie_search):
                if res.data['year'] == row['year']:
                    search_idx = idx
                    break
            
            movie = ia.get_movie(movie_search[search_idx].movieID)
            
            # print(movie.keys())
            
            large_pic = ''
            if 'full-size cover url' in movie.keys():
                large_pic = movie['full-size cover url']
                
                print(f"Downloading large {row['id']} url: {large_pic}")
                
                with open(f'../img/covers/original/{row["id"]}.png', 'wb') as handle:
                    response = requests.get(large_pic, stream=True)

                    if not response.ok:
                        err_cnt += 1
                        print(response)

                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
    
            else:
                print("NO large image for ", row['title'])
                no_img += 1
                continue
                
            if 'cover url' in movie.keys():
                small_pic = movie['cover url']
                with open(f'../img/covers/small/{row["id"]}.png', 'wb') as handle:
                    response = requests.get(small_pic, stream=True)

                    print(f"Downloading small {row['id']} url: {small_pic}")
                    
                    if not response.ok:
                        err_cnt += 1
                        print(response)

                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
            else:
                print("NO large image for ", row['title'])
                no_small_img += 1
                continue
         
        except KeyboardInterrupt:
            print("Keyboard Interrupt.")
            exit(1)
        except:
            print('[X] Error for: ', row['title'])
            err_cnt += 1
            pass
            

    # plots_df = DataFrame(plots_dict)
    # plots_df.to_csv(f'imdb_plots.csv', index=False)
    
    diff = time() - start
    print('[!] Done - Elapsed Time: %02d:%02d' % (diff // 60, (diff % 60)))
    print('Errors: ', err_cnt, 'Missing img: ', no_img, 'Missing small', no_small_img)

if __name__ == "__main__":
    # fetch_plots(col_name='plot', m_info='plot')
    fetch_covers()
    # ia = IMDb()
    # res = ia.search_person("Dwayne Johnson")
    # print(res[0].personID)
    # res = ia.get_person(res[0].personID)
    # print(res.data)