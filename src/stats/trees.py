from collections import Counter

import networkx as nx
import pandas as pd

def stats(T, name=None):
    T = T.reverse()
    # First get root
    n_nodes = len(T)
    root = [n for n in T if T.in_degree(n) == 0]
    print(root)
    root = root[0]
    sps = nx.shortest_path_length(T, root)
    widths = Counter(list(sps.values()))
    max_width = widths.most_common(1)[0][1]
    depth = max(sps.values())
    result = {"#V": n_nodes,
              "max width": max_width,
              "depth": depth}
    if name is not None:
        result["name"] = name
    return result


def main():
    venues = ["WWW", "WSDM", "SEMWEB"]
    venue_trees = [nx.read_gpickle("data/" + venue + "/line_parent_tree.pickle")
                   for venue in venues]
    twitter_trees = [nx.read_gpickle("data/Twitter" + str(i) + "/LP.pickle")
                     for i in [10, 100]]
    ogbn_tree = [nx.read_gpickle("data/ogbn-products/tree.pickle")]
    trees = venue_trees + twitter_trees + ogbn_tree
    names = ["WebConf", "WSDM", "ISWC", "Twitter>10k", "Twitter>100k", "OGBN-Products"]
    tree_stats = [stats(T, name) for T, name
                  in zip(trees, names)]
    d = pd.DataFrame(tree_stats)
    print(d)
    d.to_csv("data/tree_stats.csv", index=False)

main()
