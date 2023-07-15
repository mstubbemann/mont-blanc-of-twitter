import os
import gzip
import json
from collections import defaultdict

import networkx as nx


def collect_co_author_data(source="data/semantic_scholar/",
                           venue="WWW",
                           start=2000,
                           end=2020,
                           destination="data/www/"):
    """
    Collect for a given "venue" all needed information from semantic_scholar
    "source" and store it in "destination".
    """
    authors = defaultdict(set)
    author_publication_pairs = []
    publications = []
    publication_for_cite_counting = set()
    files = [file_path for file_path in os.listdir(source)
             if "s2-corpus-" in file_path]

    # In first run, catch author_ids
    first_found = {}
    finally_found = set()

    for i, file_path in enumerate(files):
        # if i >100:
        #     break
        with gzip.open(source + file_path,
                       'rt',
                       encoding="utf-8") as file:
            for line in file:
                line = json.loads(line)
                if "year" not in line or not line["year"]:
                    continue
                year = int(line["year"])
                if (start <= year <= end) and (line["venue"].upper() == venue):
                    for author in line["authors"]:
                        if len(author["ids"]) > 1:
                            print(author)
                            raise NameError("Multiple IDS found!")
                        for id in author["ids"]:
                            authors[id].add(author["name"])
                            if id not in first_found:
                                first_found[id] = year
                            elif line["year"] != first_found[id]:
                                finally_found.add(id)
        print(i + 1, "/", len(files), "/", 1)
        print(len(first_found))
        print(len(finally_found))

    # Filter to authors found more than once
    authors = {key: value for key, value in authors.items()
               if key in finally_found}
    print(len(authors))

    # In second run, catch all relevant publications
    relevant_ids = set(authors.keys())
    for i, file_path in enumerate(files):
        with gzip.open(source + file_path,
                       'rt',
                       encoding="utf-8") as file:
            for line in file:
                line = json.loads(line)
                if ("year" not in line) or (not line["year"]) or not (start <= int(line["year"]) <= end):
                    continue
                author_ids = {id for author in line["authors"]
                              for id in author["ids"]}
                author_ids = author_ids & relevant_ids
                if author_ids:
                    publications.append(line)
                    for id in author_ids:
                        author_publication_pairs.append([id,
                                                         line["id"]])
                        for cite_id in line["inCitations"]:
                            publication_for_cite_counting.add(cite_id)
        print(i + 1, "/", len(files), "/", 2)

    # In this run, get infos for all citation relevant
    # publications
    for i, file_path in enumerate(files):
        # if i >100:
        #     break
        with gzip.open(source + file_path,
                       'rt',
                       encoding="utf-8") as file:
            for line in file:
                line = json.loads(line)
                id = line["id"]
                if ("year" not in line) or (not line["year"]) or (not start <=
                                                                  int(line["year"]) <=
                                                                  end):
                    publication_for_cite_counting.discard(id)
        print(i + 1, "/", len(files), "/", 3)

    author_encoding = {key: i for i, key in enumerate(authors.keys())}
    # Run through authors for useful ids
    authors = {author_encoding[key]: list(value)
               for key, value in authors.items()}
    pubs = {}

    # Run through publications for altering stuff
    for i, publication in enumerate(publications):
        old_id = publication["id"]
        pubs[old_id] = i
        publication["id"] = i
        publication["inCitations"] = [x for x in publication["inCitations"]
                                      if x in publication_for_cite_counting]
        new_authors = []
        for author in publication["authors"]:
            author["ids"] = [author_encoding[id] for id in author["ids"]
                             if id in author_encoding]
            new_authors.append(author)
        publication["authors"] = new_authors

    author_publication_pairs = [[author_encoding[author_id],
                                 pubs[paper_id]]
                                for [author_id, paper_id]
                                in author_publication_pairs]
    # Make destination
    if not os.path.isdir(destination):
        os.makedirs(destination)

    with open(destination + "authors.json", "w") as file:
        json.dump(authors, file)

    with open(destination + "publications.json", "w") as file:
        json.dump(publications, file)

    with open(destination + "author_paper_pairs.json", "w") as file:
        json.dump(author_publication_pairs, file)


def create_graph(source="data/WWW/"):
    """
    Create networkx graph from graph in "source"
    """
    with open(source + "authors.json") as file:
        authors = {int(key): value
                   for key, value in json.load(file).items()}

    with open(source + "publications.json") as file:
        pubs = json.load(file)

    with open(source + "author_paper_pairs.json") as file:
        pairs = json.load(file)

    # First make bipartite
    # author-vs-publication-graph
    B = nx.Graph()
    authorlist = list(authors.keys())
    B.add_nodes_from(authorlist, bipartite="author")
    B.add_nodes_from(["p_" + str(line["id"])
                      for line in pubs], bipartite="publication")
    nx.set_node_attributes(B,
                           {"p_" + str(line["id"]): len(line["inCitations"])
                            for line in pubs},
                           "n_citations")
    B.add_edges_from([(author, "p_" + str(pub))
                      for [author, pub] in pairs])

    # Make weighted-coauthor graph, just greatest connected component
    G = nx.algorithms.bipartite.overlap_weighted_projected_graph(B, authorlist)
    gcc = max(nx.connected_components(G), key=len)
    G = G.subgraph(gcc).copy()
    for e in G.edges:
        # Weights should be distances
        G.edges[e]["weight"] = 1 - G.edges[e]["weight"]
    # If two authors have distance 0, replace
    weights = [G.edges[e]["weight"]
               for e in G.edges
               if G.edges[e]["weight"] > 0]
    zero_value = min(weights)/2
    for e in G.edges:
        G.edges[e]["weight"] = max(zero_value,
                                   G.edges[e]["weight"])
    # Add H-indices as node attributes
    for author in G.nodes:
        citation_list = [B.nodes[pub]["n_citations"] for pub
                         in B.neighbors(author)]
        G.nodes[author]["h_index"] = h_index(citation_list)
    nx.write_gpickle(G, source + "G.pickle")
    return G


# Utility functions for author attributes

def h_index(citation_list):
    """
    Compute h_index from a given "citation_list".
    """
    citation_list.sort(reverse=True)
    for i, cites in enumerate(citation_list, start=1):
        if i > cites:
            return i - 1
    return len(citation_list)
