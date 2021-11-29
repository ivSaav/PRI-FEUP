import pandas as pd
from pathlib import Path

def handle_mult_plot(lst):
    # only keep 2 plots
    if (len(lst) > 2):
        # print(type(lst))
        return [min(lst, key=len), max(lst, key=len)]
    return lst

def data_merging():

    data = pd.read_csv(Path('./data/imdb.csv'))   # imdb data
    # renaming first column
    data.rename(columns= {'Unnamed: 0' : 'id'}, inplace=True)

    plots = pd.read_csv(Path('./data/imdb_all_plots.csv')) # read imdb plots
    
    plots['plot'] = plots['plot'].apply(eval)
    plots['plot'] = plots['plot'].apply(handle_mult_plot)

    # # adding plots to the original data
    df = pd.merge(data, plots, on=['id', 'title'])


    out_path = Path('./data/imdb_final.csv')
    df.to_csv(out_path, index=False, index_label='id', encoding='utf-8') # save final version


if __name__ == '__main__':
    final = data_merging()
