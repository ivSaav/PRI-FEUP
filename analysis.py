import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from pathlib import Path

def data_analysis():

    df = pd.read_csv(Path('./data/imdb_final.csv'))   # imdb data
    # df['kind'].value_counts().plot.bar()
    # plt.savefig('kind_counts')

    # TODO: maybe draw "the line"
    # TODO: check number of votes aswell
    # df['rating'].plot.hist()
    # plt.xlabel('Rating')
    # plt.xticks(range(0,11,1))

    # TODO: maybe draw "the line"
    df['year'].plot.hist()
    plt.xlabel('Year')
    plt.show()


    



    




if __name__ == "__main__":
    data_analysis()