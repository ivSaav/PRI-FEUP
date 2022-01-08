import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import io
import math

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

    return df
    

# METRICS TABLE
# Define custom decorator to automatically calculate metric based on key
metrics = {}
metric = lambda f: metrics.setdefault(f.__name__, f)

@metric
def avp(ranks, n=10):
    res = list()
    for i in range(1, n+1):
        tmp = ranks[:i]
        sum = np.sum(tmp)
        res.append(round(sum/i, 2))
        
    # extract only the positive ones
    p_values = [res[x] for x in range(n) if ranks[x] == 1]
    return round(np.sum(p_values)/len(p_values), 2), res
    

@metric
def recall(ranks, n=10):
    res = list()
    total = np.sum(ranks)
    
    for i in range(1, n+1):
        tmp = ranks[:i]
        res.append(round(np.sum(tmp)/total, 2))
    return -1, res

def interp_pr(p_values, r_values):
    steps = [x for x in np.arange(0, 1.1, 0.1)]
    res = list()
    n = len(p_values)
    for idx, step in enumerate(steps):
        tmp_p = [p_values[i] for i in range(0, n) if r_values[i] >= step]
        res.append(np.max(tmp_p))
        
    return res


def calculate_metrics(qname, ranks):
    # Define metrics to be calculated
    evaluation_metrics = {
        'avp': 'AvP',
        'p10' : 'P@10',
    }
    
    results = {}
    results["SYS1"] = calculate_system_metrics(qname, ranks["SYS1"])
    results["SYS2"] = calculate_system_metrics(qname, ranks["SYS2"])
    results["SYS3"] = calculate_system_metrics(qname, ranks["SYS3"])
    
    metric_dict =  {
        "Metric": [evaluation_metrics[m] for m in evaluation_metrics],
        "SYS1" :  [results["SYS1"][m] for m in evaluation_metrics],
        "SYS2" :  [results["SYS2"][m] for m in evaluation_metrics],
        "SYS3" :  [results["SYS3"][m] for m in evaluation_metrics]
    }

    df = pd.DataFrame(metric_dict)
    df.set_index('Metric', inplace=True)

    with open(Path(f'./reports/{qname}_results.tex'),'w') as tf:
        tf.write(convertToLaTeX(df))
    print()   
    print(df)
    print()
    
    
    return results

def calculate_system_metrics(qname, ranks):
    results = {}
    results['avp'], results['p_values'] = avp(ranks)
    results['recall'], results['r_values'] = recall(ranks)
    results['p10'] = results['p_values'][-1]
    return results

#################################################################################
#################################################################################
# PRECISION-RECALL CURVE
# Calculate precision and recall values as we move down the ranked list

def plot_precision_recal_graph(precision_values, recall_values, avp=None, **kwargs): 
    
    interp_p = interp_pr(precision_values, recall_values)
    
    # disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_values], recall_values)
    disp = PrecisionRecallDisplay(precision=interp_p, recall=[x for x in np.arange(0, 1.1, 0.1)], average_precision=avp)
    disp.plot(**kwargs)
    # # plt.savefig('precision_recall.pdf')


def evaluate(qname, url1, url2):
    res_sys1 = requests.get(url1).json()['response']['docs']
    res_sys2 = requests.get(url2).json()['response']['docs']

    print("[SYS1] Saw {0} result(s).".format(len(res_sys1)))
    print("[SYS2] Saw {0} result(s).".format(len(res_sys2)))
        
    relevant = list(map(lambda el: el.strip(), open(Path(f"./qrels/{qname}.txt")).readlines()))
    relevant = [x for x in relevant if x[0] != '#'] # ignore commented lines
    
    ranks = ranking(qname, res_sys1, res_sys2, relevant, 10)
    
    metrics = calculate_metrics(qname, ranks)
    
    _, ax = plt.subplots(figsize=(8, 8))
    plot_precision_recal_graph(res_sys1, relevant,  name="sys1", color="red", ax=ax)
    plot_precision_recal_graph(res_sys2, relevant, name="sys2",  color="orange", ax=ax)
    ax.set_ylim([0.3, 1.01])
    plt.savefig(Path(f'./reports/{qname}_curve.png'), bbox_inches='tight')

    
    
if __name__ == '__main__':
    
    # # Boosts
    # TITLE = 3
    # GENRE = 2
    # KIND = 2
    # PLOT = 0.7
    # CAST = 0.8
    
    
    dic = {"Rank" : [i for i in range(1, 10+1)], "SYS1" : [1,1,1,0,0,1,0,0,0,0], "SYS2": [1,0,0,1,0,0,1,0,1,1], "SYS3" : [1,1,1,1,1,0,0,0,1,0]}
    df = pd.DataFrame(dic)
    
    # ap, p_values = avp(df["SYS1"], 10)
    # recall = recall(df["SYS1"], 10)
    
    # pr = interp_pr(p_values, recall)
    
    # print("Recall: ", recall)
    # print("AvP", ap, p_values)
    # print("Interp PR ", pr)
    results = calculate_metrics("test", dic)
    print(results)
    _, ax = plt.subplots(figsize=(8, 8))
    plot_precision_recal_graph(results["SYS1"]["p_values"], results["SYS1"]["r_values"], ax=ax, color="red")
    plot_precision_recal_graph(results["SYS2"]["p_values"], results["SYS2"]["r_values"], ax=ax, color="orange")
    plot_precision_recal_graph(results["SYS3"]["p_values"], results["SYS3"]["r_values"], ax=ax, color="blue")
    
    plt.show()