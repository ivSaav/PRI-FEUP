# If on Python 2.X
# from __future__ import print_function

import pandas as pd
from pathlib import Path
import pysolr

# solrpy examples: https://github.com/django-haystack/pysolr

# Create a client instance. The timeout and authentication options are not required.
solr = pysolr.Solr('http://localhost:8983/solr/courses', always_commit=False)

# Do a health check.
solr.ping()

# edit according to query needs
QRELS_FILE = "system_qrels.txt"
QNAME = "simple"

relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))

res_sys1 = solr.search('informaçao dados^2', **{
    'q.OP': 'OR',
    'defType': 'edismax',
    'qf': 'title^2 objectives learning_outcomes'
}).docs

res_sys2 = solr.search('informaçao dados^2', **{
    'q.OP': 'OR',
    'defType': 'edismax',
    'qf': 'title^2 objectives learning_outcomes'
}).docs

res_sys3 = solr.search('informaçao dados^2', **{
    'q.OP': 'OR',
    'defType': 'edismax',
    'qf': 'title^2 objectives learning_outcomes'
}).docs

# The ``Results`` object stores total results found, by default the top
# ten most relevant results and any additional data like
# facets/highlighting/spelling/etc.
print("[SYS1] Saw {0} result(s).".format(len(res_sys1)))
print("[SYS2] Saw {0} result(s).".format(len(res_sys2)))
print("[SYS3] Saw {0} result(s).".format(len(res_sys3)))

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
df = pd.DataFrame([['Metric','SYS1', 'SYS2', 'SYS3']] +
    [
        [evaluation_metrics[m], calculate_metric(m, res_sys1, relevant),  calculate_metric(m, res_sys2, relevant), calculate_metric(m, res_sys3, relevant)]
        for m in evaluation_metrics
    ]
)

with open(Path(f'../docs/eval_reports/{QNAME}_results.tex'),'w') as tf:
    tf.write(df.to_latex())


