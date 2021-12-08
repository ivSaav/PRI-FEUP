import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

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
#     'qf': title^1.2 genre kind^0.8 language cast writer composer plot^1.5,
#     'rows': 100,
#     'fl': 'id'
# }


#### WW2 no documentaries ####
# QNAME = "ww2_no_docs"
# QUERY_URL1 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20title%20plot&indent=true&q.op=AND&q=%22World%20War%22%20(2%20OR%20II%20OR%20two)%20(action%20OR%20drama%20OR%20thriller)%20AND%20-documentary&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100"
# QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20genre%20plot&indent=true&q.op=AND&q=%22World%20War%22%20(2%20OR%20II%20OR%20two)%20(action%20OR%20drama%20OR%20thriller)%20AND%20-documentary&qf=title%5E1.2%20genre%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E1.5&rows=100"

#### family programs done by voice actors ####
# QNAME = "voice_actors_family"
# QUERY_URL1 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20title%20plot&indent=true&q.op=AND&q=(%22Frank%20Welker%22%20OR%20%22Kirk%20Thornton%22%20OR%20%22Wendee%20Lee%22%20OR%20%22Jeff%20Bennett%22)%20AND%20Family&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100"
# QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20genre%20plot&indent=true&q.op=AND&q=(%22Frank%20Welker%22%20OR%20%22Kirk%20Thornton%22%20OR%20%22Wendee%20Lee%22%20OR%20%22Jeff%20Bennett%22)%20AND%20Family&qf=title%5E1.2%20genre%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E1.5&rows=100"

##### romantic comedies in spanish or french #####
# QNAME = "comedy_romantic_fr_spa"
# QUERY_URL1 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20title%20plot&indent=true&q.op=AND&q=(spanish%20OR%20french)%20AND%20(comedy%20AND%20romance)&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100"
# QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20genre%20plot&indent=true&q.op=AND&q=(spanish%20OR%20french)%20AND%20(comedy%20AND%20romance)&qf=title%5E1.2%20genre%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E1.5&rows=100"

##### comedy series in english #####
QNAME = "series_comedy_english_to1995"
QUERY_URL1 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20title%20plot&fq=year%3A%5B*%20TO%201995%5D&indent=true&q.op=AND&q=(%22tv%20series%22%20OR%20%22tv%20mini%20series%22%20OR%20%22series%22)%20AND%20Comedy%20AND%20English&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100"
QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&fl=id%20genre%20plot&fq=year%3A%5B*%20TO%201995%5D&indent=true&q.op=AND&q=(%22tv%20series%22%20OR%20%22tv%20mini%20series%22%20OR%20%22series%22)%20AND%20Comedy%20AND%20English&qf=title%5E1.2%20genre%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E1.5&rows=100"


res_sys1 = requests.get(QUERY_URL1).json()['response']['docs']
res_sys2 = requests.get(QUERY_URL2).json()['response']['docs']

print("[SYS1] Saw {0} result(s).".format(len(res_sys1)))
print("[SYS2] Saw {0} result(s).".format(len(res_sys2)))

# for res in res_sys1:
#     print(res['id'])
    
relevant = list(map(lambda el: el.strip(), open(Path(f"./qrels/{QNAME}.txt")).readlines()))
relevant = [x for x in relevant if x[0] != '#'] # ignore commented lines

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

# Define metrics to be calculated
evaluation_metrics = {
    'ap': 'Average Precision',
    'p10': 'Precision at 10 (P@10)'
}

# Calculate all metrics and export results as LaTeX table
df = pd.DataFrame([['Metric','SYS1', 'SYS2']] +
    [
        [evaluation_metrics[m], calculate_metric(m, res_sys1, relevant),  calculate_metric(m, res_sys2, relevant)]
        for m in evaluation_metrics
    ]
)

with open(Path(f'../docs/eval_reports/{QNAME}_results.tex'),'w') as tf:
    tf.write(df.to_latex())

#################################################################################
#################################################################################
# PRECISION-RECALL CURVE
# Calculate precision and recall values as we move down the ranked list

def plot_precision_recal_graph(results, relevant, **kwargs): 
    
    # results = results[:20]
    precision_values = [
        len([
            doc 
            for doc in results[:idx]
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

    precision_recall_match = {k: v for k,v in zip(recall_values, precision_values)}

    # Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
    recall_values.extend([step for step in np.arange(0.1, 1.1, 0.1) if step not in recall_values])
    recall_values = sorted(set(recall_values))

    # Extend matching dict to include these new intermediate steps
    for idx, step in enumerate(recall_values):
        if step not in precision_recall_match:
            if recall_values[idx-1] in precision_recall_match:
                precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
            else:
                precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]

    disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_values], recall_values)
    disp.plot(**kwargs)
    # plt.savefig('precision_recall.pdf')

_, ax = plt.subplots(figsize=(7, 8))
  
plot_precision_recal_graph(res_sys1, relevant, name="sys1", color="red", ax=ax)
plot_precision_recal_graph(res_sys2, relevant, name="sys2", color="orange", ax=ax)

plt.show()