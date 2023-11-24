import random
import copy
import networkx as nx
import matplotlib.pyplot as plt
import csv
import pandas as pd
import math
import timeit
import difflib

# Karger’s Algorithm
def kargerMinCut(graph, n):
    gn = {k: str(i) for (i, k) in enumerate(graph.keys(), 0)}
    while len(graph) > n:
        v = random.choice(list(graph.keys()))  # the key
        w = random.choice(graph[v])  # the list of connections

        # assigning the same label to the nodes that are being grouped
        label = gn[w]
        for key in gn.keys():
            if gn[key] == label:
                gn[key] = gn[v]

        contract(graph, v, w)  # merge together

    mincut = len(graph[list(graph.keys())[0]])  # calculate mincut
    return gn, mincut

def contract(graph, v, w):
    for node in graph[w]:  # merge the nodes from w to v
        if node != v:  # we don't want to add self-loops
            graph[v].append(node)
        graph[node].remove(w)  # delete the edges to the absorbed
        if node != v:
            graph[node].append(v)
    del graph[w]  # delete the absorbed vertex 'w'

def load_data(csv_file):
    data = {}
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = int(row['id'])
            communities = [row['username'], row['full_name'], row['profile_pic_url'], row['is_private'],
                           row['is_verified']]
            data[user_id] = communities
    return data

def similarity_ratio(list1, list2):
    # Calculate the similarity ratio between two lists
    sm = difflib.SequenceMatcher(None, list1, list2)
    return sm.ratio()

def create_similarity_graph(data, threshold):
    graph = {}
    user_ids = list(data.keys())

    for i, user_id1 in enumerate(user_ids, 1):
        for user_id2 in user_ids[i:]:
            if user_id1 != user_id2:
                similarity = similarity_ratio(data[user_id1], data[user_id2])
                if similarity >= threshold:
                    graph.setdefault(user_id1, []).append(user_id2)
                    graph.setdefault(user_id2, []).append(user_id1)

    return graph

# Specify the CSV file containing user data
csv_file = 'follower_data.csv'

# Load data from the CSV file
user_data = load_data(csv_file)

# Create the similarity graph based on the threshold
g = create_similarity_graph(user_data, 0.05)

def main(g, n):
    res = {}
    cuts = []
    iterations = len(list(g.keys())) * int(math.log(len(list(g.keys())), 2))
    for i in range(iterations):
        labels, mincut = kargerMinCut(copy.deepcopy(g), n)
        cuts.append(mincut)
        if min(cuts) == mincut:
            res = labels

        print(i, "/", iterations)

    print("minimum cuts: ", min(cuts))
    return res

# Run Karger's algorithm for community detection
KargerStart = timeit.default_timer()
labelsData = main(g, 12)
KargerEnd = timeit.default_timer()
print("Karger clusterization finished, took: ", KargerEnd - KargerStart, "s")

# Check how many elements are in each group
ne = {}
for k, v in labelsData.items():
    ne[v] = ne.get(v, 0) + 1
print("Number of entries in each group: ", ne)

# Construct graph for visualization
edges = []
for k, v in g.items():
    for e in v:
        edges.append(tuple([k, e]))
G = nx.Graph()
G.add_edges_from(edges)

# Color the graph
carac = pd.DataFrame({'ID': list(labelsData.keys()), 'groups': list(labelsData.values())})
carac = carac.set_index('ID')
carac = carac.reindex(G.nodes())
carac['groups'] = pd.Categorical(carac['groups'])
carac['groups'].cat.codes

# Draw the graph
pos = nx.spring_layout(G)  # Using spring_layout for better visualization
nx.draw(G, pos=pos, labels=labelsData, with_labels=True, node_color=carac['groups'].cat.codes,
        cmap=plt.cm.tab10, node_size=200, font_size=8, font_color='black', font_weight='bold', alpha=0.8)
plt.title("Community Detection using Karger's Algorithm")
plt.show()
