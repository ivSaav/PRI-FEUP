import pandas as pd
from pathlib import Path

import requests

# { OPTIONS SYSTEM 1
#     'q.OP' : 'AND',
#     'defType': 'edismax',
#     'qf': 'title genre kind language cast writer composer plot',
#     'rows': 100,
#     'fl': 'id'
# }

# { OPTIONS SYSTEM 1
#     'q.OP' : 'AND',
#     'defType': 'edismax',
#     'qf': 'title genre kind language cast writer composer plot',
#     'rows': 100,
#     'fl': 'id'
# }

QNAME = "drama_action_movies"

QUERY_URL1 = "http://localhost:8983/solr/netflix/select?defType=edismax&fq=year%3A%5B2000%20TO%20*%5D&indent=true&q.op=AND&q=drama%20AND%20action%20AND%20movie&qf=title%20genre%20kind%20language%20cast%20writer%20composer%20plot&rows=100"
QUERY_URL2 = "http://localhost:8983/solr/netflix/select?defType=edismax&fq=year%3A%5B2000%20TO%20*%5D&indent=true&q.op=AND&q=drama%20AND%20action%20AND%20movie&qf=title%5E1.2%20genre%20kind%5E0.8%20language%20cast%20writer%20composer%20plot%5E1.5&rows=100"

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


