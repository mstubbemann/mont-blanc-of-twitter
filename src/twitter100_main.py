from collections import defaultdict
import json
from multiprocessing import Pool
import os

import networkx as nx
import igraph as ig

from .rng_graph import rng_graph as rng
from .mountains import mountainworld

n_pools = 14
followers = defaultdict(lambda: 0)


if __name__ == "__main__":
    if not os.path.isdir("data/Twitter100"):
        os.makedirs("data/Twitter100")

    print("Catch relevant authors")
    with open("data/twitter-2010.txt") as file:
        for i, line in enumerate(file):
            nodes = line.split(sep=" ")
            n0 = int(nodes[0])
            followers[n0] += 1
            if i % 100000 == 0:
                print(i+1, "/", 1468364884)

    relevant_authors = {key: value for key, value in followers.items()
                        if value >= 100000}
    print("Dump relevant authors")
    with open("data/Twitter100/relevant_authors.json", "w") as file:
        json.dump(relevant_authors, file)

    print("Catch followers of relevant authors")
    followers = defaultdict(set)
    with open("data/twitter-2010.txt") as file:
        for i, line in enumerate(file):
            nodes = line.split(sep=" ")
            n0 = int(nodes[0])
            if n0 not in relevant_authors:
                continue
            n1 = int(nodes[1])
            followers[n0].add(n1)
            if i % 100000 == 0:
                print(i+1, "/", 1468364884)

    print("Make coupling graph")
    authors = list(relevant_authors)
    n_authors = len(authors)
    G = nx.Graph()


    def neighbors(i):
        author = authors[i]
        m1 = followers[author]
        neighbors = []
        for author1 in authors[i+1:]:
            m2 = followers[author1]
            intersection = len(m1 & m2)
            if intersection:
                neighbors.append((author1,
                                  1 - (intersection/len(m1 | m2))))
        if i % 10 == 0:
            print(i+1, "/", n_authors)
        return neighbors


    with Pool(n_pools) as p:
        edges = p.map(neighbors, range(n_authors))

    print("Finished edge identification")
    print("Now make graph")
    for i, (a, e) in enumerate(zip(authors,
                                   edges)):
        for neighbor, weight in e:
            G.add_edge(a, neighbor, weight=weight)
        if i % 10 == 0:
            print(i+1, "/", n_authors)

    print("Just look at gcc")
    gcc = max(nx.connected_components(G), key=len)
    G = G.subgraph(gcc).copy()

    heights = {key: value for key, value in relevant_authors.items()
               if key in G}

    nx.set_node_attributes(G, values=heights, name="height")

    print("Remove Edges with Zero Weights")
    weight = min([G.edges[e]["weight"] for e in G.edges
                  if G.edges[e]["weight"] > 0])/2
    print(weight)
    for i, e in enumerate(G.edges):
        G.edges[e]["weight"] = max(G.edges[e]["weight"], weight)
        if i % 1000 == 0:
            print(i, "/", len(G.edges))
    print("Save nx Graph")
    nx.write_gpickle(G, "data/Twitter100/G.pickle")

    print("Compute shortest paths via iGraph.")
    H = ig.Graph.from_networkx(G)
    distance_matrix = H.shortest_paths(weights="weight", mode="all")
    print("Make distance dictionary.")
    names = list(H.vs["_nx_name"])
    distances = defaultdict(dict)
    for i, v in enumerate(names):
        for j, w in enumerate(names):
            distances[v][w] = distance_matrix[i][j]
        if i % 100 == 0:
            print(i + 1, "/", len(names))

    print("Compute RNG.")
    RNG = rng(G,
              distances=distances)
    nx.write_gpickle(RNG, "data/Twitter100/rng.pickle")


    print("Make Mountainworld.")
    heights = {node: G.nodes[node]["height"] for node in G.nodes}
    GM, _, _, _, _, LP = mountainworld(RNG,
                                       heights=heights,
                                       distances=distances)
    nx.write_gpickle(GM, "data/Twitter100/GM.pickle")
    nx.write_gpickle(LP, "data/Twitter100/LP.pickle")
