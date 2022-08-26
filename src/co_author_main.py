import networkx as nx

from preprocessing import collect_co_author_data as collect, create_graph as graph
from rng_graph import rng_graph as rng
from mountains import mountainworld


def main(folder="data/WWW/",
         venue="WWW"):
    """
    Main function for co-author networks. Computes
    RNG, mountain_graph and line parent.
    """
    # Create graph if not exists, else load
    try:
        print("Try to load graph.")
        G = nx.read_gpickle(folder+"G.pickle")
    except FileNotFoundError:
        print("Could not find Graph. Creating it.")
        print("Start searching through Semantic Scholar.")
        collect(venue=venue,
                start=2000,
                end=2020,
                destination=folder)
        print("Create co-author Graph-")
        G = graph(source=folder)
    
    print("Start computation of distances.")
    distances = dict(nx.algorithms.all_pairs_dijkstra_path_length(G))

    print("Start creation of rng graph.")
    RNG = rng(G,
              distances=distances,
              destination=folder)

    heights = {node: RNG.nodes[node]["h_index"]
               for node in RNG.nodes}
    G_M, _, _, _, _, LP = mountainworld(RNG,
                                        heights=heights,
                                        distances=distances)
    nx.write_gpickle(G_M, folder + "mountain_graph.pickle")
    nx.write_gpickle(LP, folder + "line_parent_tree.pickle")


if __name__ == "__main__":
    venues = ["WWW", "WSDM", "SEMWEB"]
    for venue in venues:
        print("-----------")
        print("Start with venue: ", venue)
        folder = "data/" + venue + "/"
        main(folder=folder,
             venue=venue)
        print("-------------")
