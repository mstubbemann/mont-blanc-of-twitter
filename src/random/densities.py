import networkx as nx
import numpy as np
import pandas as pd

from ..rng_graph import rng_graph as rng
from ..mountains import mountainworld

n = 100
interval = np.arange(start=0.01, stop=1, step=0.01)


def random(n=100,
           number=1,
           repeats=20,
           interval=np.arange(start=0.01, stop=1, step=0.01)):
    results = pd.DataFrame()
    for i, p in enumerate(interval):
        for j in range(repeats):
            B = nx.bipartite.random_graph(100, n, p, seed=i+j+42)
            nodeset = {node for node in B
                       if B.nodes[node]["bipartite"] == 0}
            G = nx.bipartite.overlap_weighted_projected_graph(B,
                                                              nodeset)
            gcc = max(nx.connected_components(G), key=len)
            G = G.subgraph(gcc).copy(G)
            for e in G.edges:
                G.edges[e]["weight"] = 1 - G.edges[e]["weight"]
            # Force positive edges
            weights = [G.edges[e]["weight"]
                       for e in G.edges
                       if G.edges[e]["weight"] > 0]
            zero_value = min(weights)/2
            for e in G.edges:
                G.edges[e]["weight"] = max(zero_value,
                                           G.edges[e]["weight"])

            heights = {node: len(list(B.neighbors(node)))
                       for node in G}
            result = {"n": n,
                      "p": p,
                      "i": j,
                      "nodes": len(G),
                      "edges": len(G.edges),
                      "density": nx.density(G)}
            RNG = rng(G)
            result.update({"RNG_nodes": len(RNG),
                           "RNG_edges": len(RNG.edges),
                           "RNG_density": nx.density(RNG)})
            pgr = mountainworld(RNG, heights)
            GM = pgr[0].to_undirected()
            result.update({"GM_nodes": len(GM),
                           "GM_edges": len(GM.edges),
                           "GM_density": nx.density(GM)})
            LP = pgr[5].to_undirected()
            result.update({"LP_nodes": len(LP),
                           "LP_edges": len(LP.edges),
                           "LP_density": nx.density(LP)})
            results = results.append(result,
                                     ignore_index=True)
        print(p)

    results.to_csv("data/random_" + str(n) + "_" + str(number) + ".csv")
    return results


if __name__ == "__main__":
    random(n=100000,
           interval=np.arange(start=0.0001, stop=0.0200, step=0.0001))
    random(n=100)
