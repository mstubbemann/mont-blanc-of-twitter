from queue import PriorityQueue
from multiprocessing import Pool

import networkx as nx
from tqdm import tqdm
from ogb.nodeproppred import NodePropPredDataset as PD
import numpy as np
import igraph as ig

n_pools = 16

print("Load Graph")
data = PD(name="ogbn-products", root="data/ogbn-products/")
print("Convert to IGraph")
H = data[0][0]
G = ig.Graph()
print("Touch")
X = H["node_feat"]
G.add_vertices(X.shape[0])
indices = H["edge_index"]
print("Touch")
G.add_edges([(a.item(), b.item()) for a, b in zip(*indices)])



print("Make undirected and restrict to biggest connected component")
G.to_undirected()
C = G.clusters()
G = C.giant()

print("Compute heights")
nodes = list(range(G.vcount()))
for node in nodes:
    G.vs[node]["height"] = G.vs[node].degree()

print("Compute Peaks")
nodes = list(range(G.vcount()))

def is_peak(node):
    h = G.vs[node]["height"]
    neighborheights = [G.vs[m]["height"] for m in G.neighborhood(node)
                       if m != node]
    return node, max(neighborheights) < h


with Pool(n_pools) as p:
    peaks = [p for p, b in tqdm(p.imap_unordered(is_peak, nodes, chunksize=10),
                                total=len(nodes))
             if b]

print("Nodes:", len(nodes))
print("Edges:", G.ecount())
print("Peaks:", len(peaks))
peakset = set(peaks)


def mountainworld(node):
    rng = np.random.default_rng(42+node)
    tupels = []
    saddles = set()
    h = G.vs[node]["height"]
    queue = PriorityQueue()
    queue.put((0, node, node))
    closed = set()
    found_peak = False
    prominence = 0
    while not queue.empty():
        (maxHeightDiff, k, saddle) = queue.get()
        if found_peak and maxHeightDiff > prominence:
            break
        if k in closed:
            continue
        closed.add(k)
        for m in G.neighborhood(k):
            if m in closed:
                continue
            if G.vs[m]["height"] > h:
                if m in peakset:
                    tupels.append((node, m, saddle, maxHeightDiff))
                    saddles.add(saddle)
                    found_peak = True
                    prominence = maxHeightDiff
                else:
                    queue.put((maxHeightDiff, m, saddle))
            else:
                newDiff = h - G.vs[m]["height"]
                if newDiff > maxHeightDiff:
                    queue.put((newDiff, m, m))
                else:
                    queue.put((maxHeightDiff, m, saddle))
    if not found_peak:
        tupels.append((node, None, None, h))
        saddles.add(None)
    if len(saddles) > 1:
        saddlelist = list(saddles)
        distances = G.shortest_paths(node, saddlelist)
        distances = {node: value for node, value in zip(saddlelist,
                                                        distances[0])}
        minimum = min(distances.values())
        saddles = {s for s in saddles if distances[s] == minimum}
        s = rng.choice(a=list(saddles),
                       size=1)[0]
        saddles = {s}
        tupels = [t for t in tupels
                  if t[2] == s]
    if len(tupels) == 1:
        return (node, tupels[0][1])
    else:
        parent_peaks = list(set([t[1] for t in tupels]))
        distances = G.shortest_paths(node, parent_peaks)
        distances = {node: value for node, value in zip(parent_peaks,
                                                        distances[0])}
        minimum = min(distances.values())
        tupels = [t for t in tupels
                  if distances[t[1]] == minimum]
        tupel = rng.choice(tupels, 1)[0]
        return (node, tupel[1])


with Pool(n_pools) as p:
    edges = [e for e in tqdm(p.imap(mountainworld, peaks, chunksize=10),
                             total=len(peaks))]

G = nx.DiGraph()
G.add_edges_from([e for e in edges if e[1] is not None])
nx.write_gpickle(G, "data/ogbn-products/tree.pickle")
