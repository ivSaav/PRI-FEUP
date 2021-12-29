import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import io

from pathlib import Path
from sklearn.metrics import PrecisionRecallDisplay


# { OPTIONS SYSTEM 1
#     'q.OP' : 'AND',
#     'defType': 'edismax',
#     'qf': 'title genre kind language cast writer composer plot',
#     'rows': 100,
#     'fl': 'id'
# }

# { OPTIONS SYSTEM 2
#     'q.OP' : 'AND',
#     'defType': 'edismax',
#     'qf': title^1.2 genre^1.1 kind^0.8 language cast writer composer plot^0.7,
#     'rows': 100,
#     'fl': 'id'
# }


#### WW2 no documentaries ####
# QNAME = "ww2_no_docs"
# QUERY_URL1 = "http://localhost:8983/solr/netflix/select?defType=edismax&indent=true&q.op=AND&q=%22World%20War%22%20(2%20OR%20II%20OR%20two)%20(action%20OR%20drama%20OR%20thriller)%20AND%20-documentary&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100"
# # QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20genre%20plot&indent=true&q.op=AND&q=%22World%20War%22%20(2%20OR%20II%20OR%20two)%20(action%20OR%20drama%20OR%20thriller)%20AND%20-documentary&qf=title%5E1.2%20genre%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E1.5&rows=100"
# QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&indent=true&q.op=AND&q=%22World%20War%22%20(2%20OR%20II%20OR%20two)%20(action%20OR%20drama%20OR%20thriller)%20AND%20-documentary&qf=title%5E1.2%20genre%5E1.1%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E0.7&rows=100"

#### family programs done by voice actors ####
# QNAME = "voice_actors_family"
# QUERY_URL1 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20title%20plot&indent=true&q.op=AND&q=(%22Frank%20Welker%22%20OR%20%22Kirk%20Thornton%22%20OR%20%22Wendee%20Lee%22%20OR%20%22Jeff%20Bennett%22)%20AND%20Family&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100"
# # QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20genre%20plot&indent=true&q.op=AND&q=(%22Frank%20Welker%22%20OR%20%22Kirk%20Thornton%22%20OR%20%22Wendee%20Lee%22%20OR%20%22Jeff%20Bennett%22)%20AND%20Family&qf=title%5E1.2%20genre%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E1.5&rows=100"
# QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&indent=true&q.op=AND&q=(%22Frank%20Welker%22%20OR%20%22Kirk%20Thornton%22%20OR%20%22Wendee%20Lee%22%20OR%20%22Jeff%20Bennett%22)%20AND%20Family&qf=title%5E1.2%20genre%5E1.1%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E0.7&rows=100"

##### romantic comedies in spanish or french #####
# QNAME = "comedy_romantic_fr_spa"
# QUERY_URL1 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20title%20plot&indent=true&q.op=AND&q=(spanish%20OR%20french)%20AND%20(comedy%20AND%20romance)&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100"
# # QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20genre%20plot&indent=true&q.op=AND&q=(spanish%20OR%20french)%20AND%20(comedy%20AND%20romance)&qf=title%5E1.2%20genre%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E1.5&rows=100"
# QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&indent=true&q.op=AND&q=(spanish%20OR%20french)%20AND%20(comedy%20AND%20romance)&qf=title%5E1.2%20genre%5E1.1%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E0.7&rows=100"

##### comedy series in english #####
# QNAME = "series_comedy_english_to1995"
# QUERY_URL1 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20title%20plot&fq=year%3A%5B*%20TO%201995%5D&indent=true&q.op=AND&q=(%22tv%20series%22%20OR%20%22tv%20mini%20series%22%20OR%20%22series%22)%20AND%20Comedy%20AND%20English&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100"
# # QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20genre%20plot&fq=year%3A%5B*%20TO%201995%5D&indent=true&q.op=AND&q=(%22tv%20series%22%20OR%20%22tv%20mini%20series%22%20OR%20%22series%22)%20AND%20Comedy%20AND%20English&qf=title%5E1.2%20genre%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E1.5&rows=100"
# QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&fq=year%3A%5B*%20TO%201995%5D&indent=true&q.op=AND&q=(%22tv%20series%22%20OR%20%22tv%20mini%20series%22%20OR%20%22series%22)%20AND%20Comedy%20AND%20English&qf=title%5E1.2%20genre%5E1.1%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E0.7&rows=100"


# #### star wars ambiguity search ####
# QNAME = "simple_sw"
# QUERY_URL1 = "http://localhost:8983/solr/netflix/select?defType=edismax&indent=true&q.op=AND&q=Star%20Wars&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100"
# # QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20title%20genre%20plot%20composer&indent=true&q.op=AND&q=Star%20Wars&qf=title%5E1.2%20genre%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E1.5&rows=50"
# QUERY_URL2 ="http://localhost:8983/solr/netflix/select?defType=edismax&indent=true&q.op=AND&q=Star%20Wars&qf=title%5E1.2%20genre%5E1.1%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E0.7&rows=100"


def print_header(name):
    print('\n#######################')
    print(name)
    print('#######################')


def convertToLaTeX(df, alignment="|c"):
    """
    Convert a pandas dataframe to a LaTeX tabular.
    Prints labels in bold, does not use math mode
    """
    numColumns = df.shape[1]
    numRows = df.shape[0]
    output = io.StringIO()
    colFormat = ("%s%s|" % (alignment, alignment * numColumns))
    
    #Write header
    output.write("\\begin{table}[]\n")
    output.write("\\begin{tabular}{%s} \\hline\n" % colFormat)
    columnLabels = ["\\textbf{%s}" % label for label in df.columns]
    output.write("& %s\\\\\\hline\n" % " & ".join(columnLabels))
    #Write data lines
    for i in range(numRows):
        output.write("\\textbf{%s} & %s\\\\ \\hline\n"
                     % (df.index[i], " & ".join([str(val) for val in df.iloc[i]])))
    #Write footer
    output.write("\\end{tabular}\n\\end{table}")
    return output.getvalue()

#################################################################################
#################################################################################
# EVALUATION METRICS

def ranking(qname, res1, res2, relevant, n=10):
    df = pd.DataFrame(
        {
            'Rank' : [i for i in range(1, n+1)],
            'SYS1' : ["X" if doc['id'] in relevant else "" for doc in res1[:n] ],
            'SYS2':  ["X" if doc['id'] in relevant else "" for doc in res2[:n] ]
        }
    )
    df = df.set_index('Rank')
    with open(Path(f'./reports/{qname}_rank.tex'),'w') as tf:
        # tf.write(df.to_latex(index=False))
        tf.write(convertToLaTeX(df))
    print()
    print(df)
    

# METRICS TABLE
# Define custom decorator to automatically calculate metric based on key
metrics = {}
metric = lambda f: metrics.setdefault(f.__name__, f)

@metric
def ap(results, relevant):
    """Average Precision"""
    precision_values = [
        len([
            doc 
            for doc in results[:idx]
            if doc['id'] in relevant
        ]) / idx 
        for idx in range(1, len(results))
    ]
    return sum(precision_values)/len(precision_values)

@metric
def p10(results, relevant, n=10):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['id'] in relevant])/n

def calculate_metric(key, results, relevant):
    return metrics[key](results, relevant)


def calculate_metrics(qname, res1, res2, relevant):
    # Define metrics to be calculated
    evaluation_metrics = {
        'ap': 'AP',
        'p10': 'P@10'
    }

    df = pd.DataFrame(
            {
                "Metric": [evaluation_metrics[m] for m in evaluation_metrics],
                "SYS1" :  [calculate_metric(m, res1, relevant) for m in evaluation_metrics],
                "SYS2" :  [calculate_metric(m, res2, relevant) for m in evaluation_metrics]
            }
        )
    df.set_index('Metric', inplace=True)

    with open(Path(f'./reports/{qname}_results.tex'),'w') as tf:
        tf.write(convertToLaTeX(df))
    print()   
    print(df)
    print()

#################################################################################
#################################################################################
# PRECISION-RECALL CURVE
# Calculate precision and recall values as we move down the ranked list

def plot_precision_recal_graph(results, relevant, avp=None, **kwargs): 
    
    # results = results[:20]
    precision_values = [
        len([
            doc for doc in results[:idx]
            if doc['id'] in relevant
        ]) / idx 
        for idx, _ in enumerate(results, start=1)
    ]

    recall_values = [
        len([
            doc for doc in results[:idx]
            if doc['id'] in relevant
        ]) / len(relevant)
        for idx, _ in enumerate(results, start=1)
    ]

    # disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_values], recall_values)
    disp = PrecisionRecallDisplay(precision=precision_values, recall=recall_values, average_precision=avp)
    disp.plot(**kwargs)
    # plt.savefig('precision_recall.pdf')


def evaluate(qname, url1, url2):
    res_sys1 = requests.get(url1).json()['response']['docs']
    res_sys2 = requests.get(url2).json()['response']['docs']

    print("[SYS1] Saw {0} result(s).".format(len(res_sys1)))
    print("[SYS2] Saw {0} result(s).".format(len(res_sys2)))
        
    relevant = list(map(lambda el: el.strip(), open(Path(f"./qrels/{qname}.txt")).readlines()))
    relevant = [x for x in relevant if x[0] != '#'] # ignore commented lines
    
    calculate_metrics(qname, res_sys1, res_sys2, relevant)
    
    _, ax = plt.subplots(figsize=(8, 8))
    plot_precision_recal_graph(res_sys1, relevant,  name="sys1", color="red", ax=ax)
    plot_precision_recal_graph(res_sys2, relevant, name="sys2",  color="orange", ax=ax)
    ax.set_ylim([0.3, 1.01])
    plt.savefig(Path(f'./reports/{qname}_curve.png'), bbox_inches='tight')

    ranking(qname, res_sys1, res_sys2, relevant, 10)
    
if __name__ == '__main__':
    
    # Boosts
    TITLE = 3
    GENRE = 2
    KIND = 2
    PLOT = 0.7
    CAST = 0.8
    
    # Star Wars
    print_header('Star Wars')
    evaluate("simple_sw", 
             "http://localhost:8983/solr/netflix/select?defType=edismax&indent=true&q.op=AND&q=Star%20Wars&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100", 
             f"http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20title%20genre%20plot&indent=true&q.op=AND&q=Star%20Wars&qf=title%5E{TITLE}%20genre%5E{GENRE}%20kind%5E{KIND}%20language%20cast%5E{CAST}%20writer%20composer%20plot%5E{PLOT}&rows=100")
    
    # World War II series or movies (no documentaries)
    print_header("World War II")
    evaluate("ww2_no_docs", 
             "http://localhost:8983/solr/netflix/select?defType=edismax&indent=true&q.op=AND&q=%22World%20War%22%20(2%20OR%20II%20OR%20two)%20(action%20OR%20drama%20OR%20thriller)%20AND%20-documentary&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100", 
             f"http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20title%20genre%20plot&indent=true&q.op=AND&q=%22World%20War%22%20(2%20OR%20II%20OR%20two)%20(action%20OR%20drama%20OR%20thriller)%20AND%20-documentary&qf=title%5E{TITLE}%20genre%5E{GENRE}%20kind%5E{KIND}%20language%20cast%5E{CAST}%20writer%20composer%20plot%5E{PLOT}&rows=100")

    # Romantic comedies in spanish or french
    print_header("Romantic Comedy")
    evaluate("comedy_romantic_fr_spa", 
             "http://localhost:8983/solr/netflix/select?defType=edismax&indent=true&q.op=AND&q=(spanish%20OR%20french)%20AND%20(comedy%20AND%20romance)&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100", 
             f"http://localhost:8983/solr/netflix/select?defType=edismax&indent=true&q.op=AND&q=(spanish%20OR%20french)%20AND%20(comedy%20AND%20romance)&qf=title%5E{TITLE}%20genre%5E{GENRE}%20kind%5E{KIND}%20language%20cast%5E{CAST}%20writer%20composer%20plot%5E{PLOT}&rows=100")
    
    # Drama and Action movies
    print_header("Drama and Action Movies")
    evaluate("drama_action_movies", 
             "http://localhost:8983/solr/netflix/select?defType=edismax&fq=year%3A%5B2000%20TO%20*%5D&indent=true&q.op=AND&q=drama%20AND%20action%20AND%20movie&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100", 
             f"http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20title%20genre%20plot&fq=year%3A%5B2000%20TO%20*%5D&indent=true&q.op=AND&q=drama%20AND%20action%20AND%20movie&qf=title%5E{TITLE}%20genre%5E{GENRE}%20kind%5E{KIND}%20language%20cast%5E{CAST}%20writer%20composer%20plot%5E{PLOT}&rows=100")
    
    # English Comedies up to (1995)
    print_header("English Comedies")
    evaluate("series_comedy_english_to1995", 
             "http://localhost:8983/solr/netflix/select?defType=edismax&fq=year%3A%5B*%20TO%201995%5D&indent=true&q.op=AND&q=comedy%20AND%20english%20AND%20tv%20show&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100", 
             f"http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20title%20genre%20plot%20kind&fq=year%3A%5B*%20TO%201995%5D&indent=true&q.op=AND&q=comedy%20AND%20english%20AND%20tv%20show&qf=title%5E{TITLE}%20genre%5E{GENRE}%20kind%5E{KIND}%20language%20cast%5E{CAST}%20writer%20composer%20plot%5E{PLOT}&rows=100")
    
    # Voice Actors 
    print_header("Voice Actors")
    evaluate("voice_actors_family", 
             "http://localhost:8983/solr/netflix/select?defType=edismax&indent=true&q.op=AND&q=(%22Frank%20Welker%22%20OR%20%22Kirk%20Thornton%22%20OR%20%22Wendee%20Lee%22%20OR%20%22Jeff%20Bennett%22)%20AND%20Family&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100", 
             f"http://localhost:8983/solr/netflix/select?debugQuery=true&defType=edismax&fl=id%20title%20genre%20plot%20kind&indent=true&q.op=AND&q=(%22Frank%20Welker%22%20OR%20%22Kirk%20Thornton%22%20OR%20%22Wendee%20Lee%22%20OR%20%22Jeff%20Bennett%22)%20AND%20Family&qf=title%5E{TITLE}%20genre%5E{GENRE}%20kind%5E{KIND}%20language%20cast%5E{CAST}%20writer%20composer%20plot%5E0.7&rows=100")