import networkx as nx


def rng_graph(G,
              weight="weight",
              distances=None,
              destination=None):
    """
    Compute RNG graph of a given graph. Edge weights are given via the attribute "weight".
    "Distances" should be a dict of dict storing distance value between nodes. If not provided,
    distances are computed first.
    """
    if not distances:
        distances = dict(nx.algorithms.all_pairs_dijkstra_path_length(G,
                                                                      weight=weight))
    H = G.copy()
    for i, (v1, v2) in enumerate(G.edges):
        d = distances[v1][v2]
        for v3 in G.nodes:
            if d > distances[v1][v3] and d > distances[v2][v3]:
                H.remove_edge(v1, v2)
                break
    if destination:
        nx.write_gpickle(H, destination + "rng.pickle")
    return H
