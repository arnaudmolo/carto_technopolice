import csv
import networkx as nx
from pyvis.network import Network

interet = {}
nodes = []
rows = []

G = nx.Graph()
with open("data.csv") as csvfile:
    csvReader = csv.reader(csvfile, delimiter=";")
    for row in csvReader:
        if row[0][0] == "#":
            continue
        rows.append(row)
        if not row[1] in interet:
            interet[row[1]] = 0
        interet[row[1]] += 1

for row in rows:
    if row[0] != "NODE":
        continue
    if not row[1] in nodes:
        G.add_node(
            row[1],
            category=row[2],
        )
        nodes.append(row[1])

for row in rows:
    if row[0] != "EDGE":
        continue
    if not row[1] in interet or interet[row[1]] < 2:
        continue
    G.add_edge(row[1], row[2], relation=row[3], url=row[4])

nx.write_gexf(G, "export.gexf")

net = Network(notebook=True, height="750px", width="100%")
net.from_nx(G)
net.show("carto.html")


def extract(graph):
    with open("./data/nodes.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "label", "category"])
        for label, data in graph.nodes(data=True):
            writer.writerow([label, label, data.get("category", "null")])

    with open("./data/edges.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["source", "target", "type", "url"])
        for source, target, data in graph.edges(data=True):
            writer.writerow([source, target, data.get("relation"), data.get("url")])


extract(G)
