import json

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt

datasets = ["PAKDD", "ECML", "KDD"]

for data in datasets:
    print("Start with: ", data)
    dir = "data/" + data + "/"

    with open(dir + "authors.json") as file:
        authors = json.load(file)

    authors = {int(key): value for key, value
               in authors.items()}

    tree = nx.read_gpickle(dir + "/line_parent_tree.pickle")
    rng = nx.read_gpickle(dir + "/rng.pickle")
    mg = nx.read_gpickle(dir + "/mountain_graph.pickle")

    # Small picture
    plt.figure(figsize=(13, 10))
    layout = graphviz_layout(tree, prog="dot")
    node_size = 200
    layout = {key: [value[0], -value[1]] for key, value in layout.items()}
    nx.draw_networkx(tree, pos=layout, with_labels=False, node_color="red",
                     arrows=False, node_size=node_size)
    plt.savefig(dir + "/small.png")
    plt.close()

    # With numbers
    nodes = list(tree.nodes())
    nodes.sort(key=lambda x: [-layout[x][1], layout[x][0]])

    # Make mapping of network
    old_mapping = dict(enumerate(nodes))
    reverse_mapping = {value: key for key, value
                       in old_mapping.items()}
    tree = nx.relabel_nodes(tree, mapping=reverse_mapping)
    layout = {reverse_mapping[key]: value for key, value
              in layout.items()}
    mapping = {key: authors[value] for key, value in old_mapping.items()}
    heights = {key: rng.nodes[value]["h_index"]
               for key, value in old_mapping.items()}
    prominences = {key: mg.nodes[value]["prominence"]
                   for key, value in old_mapping.items()}

    with open(dir + "tree_encoding.json", "w") as file:
        json.dump(mapping, file)

    with open(dir + "heights.json", "w") as file:
        json.dump(heights, file)

    with open(dir + "prominences.json", "w") as file:
        json.dump(prominences, file)

    plt.figure(figsize=(60, 20))

    fs = 30
    width = 1
    nx.draw_networkx(tree, pos=layout, with_labels=True, width=width, font_size=fs,
                     node_size=0, arrows=False)
    plt.savefig(dir + "/large.png")
    plt.close()

    # With Labels
    mapping = {key: value[0] for key, value in mapping.items()
               if key in tree}
    plt.figure(figsize=(26, 20))
    nx.draw_networkx(tree, pos=layout, with_labels=True, font_size=20,
                     node_color="lightcoral", arrows=False, labels=mapping)
    plt.savefig(dir + "/name.png")
    plt.close()


# Pictures for Twitter 10K
print("Start with Twitter>10K")
dir = "data/Twitter10/"
tree = nx.read_gpickle(dir + "/LP.pickle")
print("Make encoding")
nodes = list(enumerate(tree.nodes))
nodes = {node: i for [i, node] in nodes}
mapping = {}

print("Catch Twitter Ids")
with open("data/twitter-2010-ids.csv") as file:
    next(file)
    for line in file:
        row = line.split(sep=",")
        key = int(row[0])
        twitter_id = int(row[1])
        if key in nodes:
            mapping[key] = twitter_id

encoding = {i: mapping[node] for node, i in nodes.items()}
with open(dir + "tree_encoding.json", "w") as file:
    json.dump(encoding, file)

tree = nx.relabel_nodes(tree, nodes)

# Small picture
plt.figure(figsize=(13, 10))
layout = graphviz_layout(tree, prog="dot")
layout = {key: [value[0], -value[1]] for key, value in layout.items()}
nx.draw_networkx(tree, pos=layout, with_labels=False, node_color="red",
                 arrows=False, node_size=30)
plt.savefig(dir + "/small.png")
plt.close()

# With numbers
plt.figure(figsize=(80, 50))
nx.draw_networkx(tree, pos=layout, with_labels=True, font_size=10,
                 node_size=0, arrows=False)
plt.savefig(dir + "/large.png")
plt.close()

# Pictures for Twitter 100K
print("Start with Twitter>100K")
dir = "data/Twitter100/"
tree = nx.read_gpickle(dir + "/LP.pickle")
print("Make encoding")
nodes = list(enumerate(tree.nodes))
nodes = {node: i for [i, node] in nodes}
mapping = {}

print("Catch Twitter Ids")
with open("data/twitter-2010-ids.csv") as file:
    next(file)
    for line in file:
        row = line.split(sep=",")
        key = int(row[0])
        twitter_id = int(row[1])
        if key in nodes:
            mapping[key] = twitter_id

encoding = {i: mapping[node] for node, i in nodes.items()}
with open(dir + "tree_encoding.json", "w") as file:
    json.dump(encoding, file)

tree = nx.relabel_nodes(tree, nodes)

# Small picture
plt.figure(figsize=(13, 10))
layout = graphviz_layout(tree, prog="dot")
layout = {key: [value[0], -value[1]] for key, value in layout.items()}
nx.draw_networkx(tree, pos=layout, with_labels=False, node_color="red",
                 arrows=False, node_size=30)
plt.savefig(dir + "/small.png")
plt.close()

# With numbers
plt.figure(figsize=(80, 50))
nx.draw_networkx(tree, pos=layout, with_labels=True, font_size=10,
                 node_size=0, arrows=False)
plt.savefig(dir + "/large.png")
plt.close()
