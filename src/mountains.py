from queue import PriorityQueue
from collections import defaultdict

import networkx as nx


def mountainworld(G,
                  heights,
                  distances=None):
    """
    Compute mountain graphs and line parents from a given graph "G",
    a given dictionary "heights" that keys nodes to their height and
    a dict of dict storing the "distances" between nodes. If distances
    are not provieded, they are precomputed using Djikstra.
    """
    if not distances:
        distances = dict(nx.algorithms.all_pairs_dijkstra_path_length(G))

    # Compute all peaks
    peaks = []
    for n in G.nodes():
        h = heights[n]
        neighborheights = [heights[m] for m in G.neighbors(n)
                           if m != n]
        if max(neighborheights) < h:
            peaks.append(n)
    peakset = set(peaks)
    # Start computing mountain structure
    tupels = []
    for n in peaks:
        h = heights[n]
        queue = PriorityQueue()
        queue.put((0, n, n))
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
            for m in G.neighbors(k):
                if m in closed:
                    continue
                if heights[m] > h:
                    if m in peakset:
                        tupels.append((n, m, saddle, maxHeightDiff))
                        found_peak = True
                        prominence = maxHeightDiff
                    else:
                        queue.put((maxHeightDiff, m, saddle))
                else:
                    newDiff = h - heights[m]
                    if newDiff > maxHeightDiff:
                        queue.put((newDiff, m, m))
                    else:
                        queue.put((maxHeightDiff, m, saddle))
        if not found_peak:
            tupels.append((n, None, None, h))

    # Make Networkx Graph from them
    G1 = nx.DiGraph()
    G2 = nx.DiGraph()
    for t in tupels:
        G1.add_node(t[0], type="Peak", prominence=t[3])
        G2.add_node(t[0], type="Peak", prominence=t[3])
        if t[1] is not None:
            G1.add_node(t[2], type="Saddle", prominence=0)
    for node, parent, saddle, maxHeightDiff in tupels:
        if parent is not None and saddle is not None:
            G1.add_edge(node, saddle,
                        distance=distances[node][saddle])
            G1.add_edge(saddle, parent, distance=distances[saddle][parent])
            G2.add_edge(node, parent, distance=distances[node][parent])

    # Make peak reduced graph
    pairs = defaultdict(list)
    for node, parent, saddle, _ in tupels:
        if node is not None and saddle is not None:
            pairs[(node, saddle)].append((G1.edges[(saddle, parent)]["distance"],
                                          - heights[parent],
                                          parent))
    pairs = {(key, min(value)[2]) for key, value in pairs.items()}
    tupels = [t for t in tupels if ((t[0], t[2]), t[1]) in pairs]
    H1 = nx.DiGraph()
    H2 = nx.DiGraph()
    for t in tupels:
        H1.add_node(t[0], type="Peak", prominence=t[3])
        H2.add_node(t[0], type="Peak", prominence=t[3])
        if t[1] is not None:
            H1.add_node(t[1], type="Peak")
            H2.add_node(t[1], type="Peak")
            H1.add_node(t[2], type="Saddle", prominence=0)
    for node, parent, saddle, maxHeightDiff in tupels:
        if parent is not None and saddle is not None:
            H1.add_edge(node, saddle,
                        distance=distances[node][saddle])
            H1.add_edge(saddle, parent, distance=distances[saddle][parent])
            H2.add_edge(node, parent, distance=distances[node][parent])

    # Make saddle reduced graph
    pairs = defaultdict(list)
    for node, parent, saddle, _ in tupels:
        if node is not None and saddle is not None:
            pairs[node].append((G1.edges[(node, saddle)]["distance"],
                                G1.edges[(saddle, parent)]["distance"],
                                saddle))
    pairs = {(key, min(value)[2]) for key, value in pairs.items()}
    tupels = [t for t in tupels if (t[0], t[2]) in pairs]
    I1 = nx.DiGraph()
    I2 = nx.DiGraph()
    for t in tupels:
        I1.add_node(t[0], type="Peak", prominence=t[3])
        I2.add_node(t[0], type="Peak", prominence=t[3])
        if t[1] is not None:
            I1.add_node(t[1], type="Peak")
            I2.add_node(t[1], type="Peak")
            I1.add_node(t[2], type="Saddle", prominence=0)
    for node, parent, saddle, maxHeightDiff in tupels:
        if parent is not None and saddle is not None:
            I1.add_edge(node, saddle,
                        distance=distances[node][saddle])
            I1.add_edge(saddle, parent, distance=distances[saddle][parent])
            I2.add_edge(node, parent, distance=distances[node][parent])
    return G1, G2, H1, H2, I1, I2
