import csv
import networkx as nx
from pyvis.network import Network

interet = {}
nodes = []
rows = []

categories = {
    "Acteur privé": {"color": "red", "shape": "diamond", "size": 20},
    "Acteur public": {"color": "green", "shape": "square", "size": 20},
    "actionnaire": {"color": "yellow", "shape": "circle", "size": 20},
    "Association professionnelle": {"color": "orange", "shape": "triangle", "size": 20}
}

G = nx.Graph()
with open('data.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=';')
    for row in csvReader:
        if row[0][0] == '#':
            continue
        rows.append(row)
        if not row[1] in interet:
            interet[row[1]] = 0
        interet[row[1]] += 1

for row in rows:
    if row[0] != 'NODE':
        continue
    if not row[1] in nodes:
        G.add_node(row[1], category=row[2], color=categories[row[2]]["color"], shape=categories[row[2]]["shape"], size=categories[row[2]]["size"])
        nodes.append(row[1])

for row in rows:
    if row[0] != 'EDGE':
        continue
    if not row[1] in interet or interet[row[1]] < 2:
        continue
    if not row[1] in nodes:
        G.add_node(row[1])
        nodes.append(row[1])
#        print(['node', row[1]])
    if not row[2] in nodes:
        G.add_node(row[2])
        nodes.append(row[2])
#        print(['node', row[2]])
#    print(['edge', row[1], row[2], row[3]])
    G.add_edge(row[1], row[2], relation=row[3])

nx.write_gexf(G, "export.gexf")

net = Network(notebook=True, height="750px", width="100%")
net.from_nx(G)
net.show("carto.html")
