from collections import defaultdict
import json

import networkx as nx
import numpy as np
import igraph as ig


def sp_to_peaks_twitter(graph,
                        peaks):
    H = ig.Graph.from_networkx(graph)
    names = list(H.vs["_nx_name"])
    peakset = set(peaks)
    peaks = [i for i, p in enumerate(names)
             if p in peakset]
    peakset = set(peaks)
    distance_matrix = H.shortest_paths(target=peaks,
                                       weights="weight",
                                       mode="all")
    result = [min(pl)
              for i, pl in enumerate(distance_matrix)
              if i not in peakset]
    return result


def sp_to_peaks(graph,
                peaks):
    distances = {p: nx.algorithms.single_source_dijkstra_path_length(graph,
                                                                     p)
                 for p in peaks}
    sps = defaultdict(dict)
    peakset = set(peaks)
    # Save for all non-peaks the distances
    # to the peaks
    for p, values in distances.items():
        for k, dist in values.items():
            if k not in peakset:
                sps[k][p] = dist
    # For each non-peak, return sp to the peaks
    result = [min(value.values()) for value in sps.values()]
    return result


if __name__ == "__main__":
    venues = ["PAKDD", "ECML", "KDD"]
    for venue in venues:
        print("-----------")
        print("Start with venue: ", venue)
        G = nx.read_gpickle("data/" + venue + "/G.pickle")
        tree = nx.read_gpickle("data/" + venue + "/line_parent_tree.pickle")
        peaks = list(tree.nodes)

        # Highest Baseline
        heights = nx.get_node_attributes(G, "h_index")
        heights = list(heights.items())
        nodes = [x[0] for x in heights]
        height_list = [x[1] for x in heights]
        relevant_indices = np.argpartition(list(height_list),
                                           kth=len(peaks))[:len(peaks)]
        highest_nodes = [nodes[i] for i in relevant_indices]

        print("Results")
        distances = sp_to_peaks(G, peaks)
        np.save("data/" + venue + "/G_to_trees.pickle",
                distances)
        baseline_distances = sp_to_peaks(G, highest_nodes)
        np.save("data/" + venue + "/G_to_highest.npy",
                baseline_distances)
        print(np.mean(distances), np.median(distances), np.max(distances))
        print(np.mean(baseline_distances), np.median(
            baseline_distances), np.max(baseline_distances))

    print("Start computations for Twitter Graph")
    for t in [str(10),
              str(100)]:
        print("---------")
        print("Twitter-", t)
        G = nx.read_gpickle("data/Twitter" + t + "/G.pickle")
        rng = nx.read_gpickle("data/Twitter" + t + "/rng.pickle")
        tree = nx.read_gpickle("data/Twitter" + t + "/LP.pickle")  
        peaks = list(tree.nodes)
        with open("data/Twitter" + t + "/relevant_authors.json") as file:
            heights = json.load(file)
        heights = list(heights.items())
        nodes = [int(x[0]) for x in heights]
        height_list = [x[1] for x in heights]
        relevant_indices = np.argpartition(list(height_list),
                                           kth=len(peaks))[:len(peaks)]
        highest_nodes = [nodes[i] for i in relevant_indices]

        print("Results")
        distances = sp_to_peaks_twitter(G, peaks)
        np.save("data/Twitter" + str(t) + "/G_to_trees.pickle",
                distances)
        baseline_distances = sp_to_peaks(G, highest_nodes)
        np.save("data/Twitter" + str(t) + "/G_to_highest.npy",
                baseline_distances)
        print(np.mean(distances), np.median(distances), np.max(distances))
        print(np.mean(baseline_distances), np.median(
            baseline_distances), np.max(baseline_distances))
