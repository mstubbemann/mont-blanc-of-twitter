import networkx as nx
import pandas as pd

venues = ["ECML", "KDD", "PAKDD"]

results = pd.DataFrame()
for venue in venues:
    dir = "data/" + venue + "/"
    G = nx.read_gpickle(dir + "G.pickle")
    RNG = nx.read_gpickle(dir + "rng.pickle")
    M = nx.read_gpickle(dir + "mountain_graph.pickle").to_undirected()
    LP = nx.read_gpickle(dir + "line_parent_tree.pickle").to_undirected()
    d = {}
    d["data"] = venue
    d["nodes"] = len(G)
    d["density"] = nx.density(G)
    d["nodes_rng"] = len(RNG)
    d["density_rng"] = nx.density(RNG)
    d["v_m"] = len(M)
    d["d(V_m)"] = nx.density(M)
    d["V_LP"] = len(LP)
    d["E_LP"] = len(LP.edges)
    results = results.append(d, ignore_index=True)

# Small Twitter
G = nx.read_gpickle("data/Twitter100/G.pickle")
RNG = nx.read_gpickle("data/Twitter100/rng.pickle")
M = nx.read_gpickle("data/Twitter100/GM.pickle")
LP = nx.read_gpickle("data/Twitter100/LP.pickle")
d = {}
d["data"] = "Twitter100k"
d["nodes"] = len(G)
d["density"] = nx.density(G)
d["nodes_rng"] = len(RNG)
d["density_rng"] = nx.density(RNG)
d["v_m"] = len(M)
d["d(V_m)"] = nx.density(M)
d["V_LP"] = len(LP)
d["E_LP"] = len(LP.edges)
results = results.append(d, ignore_index=True)

# Large Twitter
G = nx.read_gpickle("data/Twitter10/G.pickle")
RNG = nx.read_gpickle("data/Twitter10/rng.pickle")
M = nx.read_gpickle("data/Twitter10/GM.pickle")
LP = nx.read_gpickle("data/Twitter10/LP.pickle")
d = {}
d["data"] = "Twitter10k"
d["nodes"] = len(G)
d["density"] = nx.density(G)
d["nodes_rng"] = len(RNG)
d["density_rng"] = nx.density(RNG)
d["v_m"] = len(M)
d["d(V_m)"] = nx.density(M)
d["V_LP"] = len(LP)
d["E_LP"] = len(LP.edges)

results = results.append(d, ignore_index=True)
print(results)
results.to_csv("data/dataset_stats.csv")
