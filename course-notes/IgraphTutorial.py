#
# Analysis of Large Scale Social Networks
#

# Get Started with Igraph Tutorial

# Import the required libraries and packages
import igraph as ig
import easygui
from matplotlib import pyplot as plt
import numpy as np

print(ig.__version__)

#
# TASK 1: Read Data Files
#

filename = "./USAir97.net"
print(filename)

g = ig.Graph.Read_Pajek(filename)

ig.summary(g)
g.is_weighted()

# Get the attributes and the number of nodes
print(g.vs.attribute_names())
print(g.vcount())

# Get the attributes and the number of edges
print(g.es.attribute_names())
print(g.ecount())

#
# TASK 2: Calculating Centrality Measures
#

degree = g.degree()
betweenness = g.betweenness(weights=None)
print("Number of degrees calculated : % 2d, minimum : % 2d, maximum : % 2d" % (len(degree), min(degree), max(degree)))
print("Betweenness: minimum: % 5.2f, maximum: % 5.4f" %(min(betweenness), max(betweenness)))

apl = g.average_path_length()
print("Average Path Length: % 5.2f" % (apl))

cls = g.closeness()

trans = g.transitivity_local_undirected() # Local clustering coefficient

plt.scatter(degree, betweenness)
np.corrcoef(degree, betweenness)

# Using the default igraph function for the calculation and plotting of the degree distribution
deg_dist = g.degree_distribution()
ig.plot(deg_dist)

# Improved calculation of degree distribution and plotting using numpy and matplotlib
print(max(degree))
hist, bins = np.histogram(degree, bins=np.linspace(0,140,29))
print(hist)
print(bins)
plt.plot(bins[1:], hist)

#
# PART 3: Graph Processing
#

# Average Degree
avg_deg = np.average(degree)
print("Average degree: % 2d" %(avg_deg))
      
# Convert list of node degree to an np.array
# This allows the use of functions from numpy
np_deg = np.array(degree)

np_deg = np.where(np_deg>=avg_deg)
print("Number of nodes with degree equal to or greater than the average: % 2d" %(len(np_deg[0])))

# Create subgraph using IDs of nodes to be retained
red_g = g.subgraph(np_deg[0])
print("Number of nodes in subgraph: % 2d"  %(len(red_g.vs()))) 

#
# PART 4: Network Visualization
#

# Calculate Kamada-Kawai layout
layout_kk = g.layout('kk')

# Define style from network plotting
visual_style = {}
visual_style["vertex_size"] = 15
visual_style["vertex_label_size"] = 5
visual_style["vertex_color"] = "blue"
visual_style["vertex_label"] = g.vs["name"]
visual_style["edge_width"] = [5 * w for w in g.es["weight"]]
visual_style["layout"] = layout_kk
visual_style["bbox"] = (600,600)
visual_style["margin"] = 20

ig.plot(g, **visual_style)

# Calculate Fruchterman-Reingold layout
layout_fr = g.layout("fr")

# Define style from network plotting
visual_style = {}
visual_style["vertex_size"] = 15
visual_style["vertex_label_size"] = 5
visual_style["vertex_color"] = "blue"
visual_style["vertex_label"] = g.vs["name"]
visual_style["edge_width"] = [5 * w for w in g.es["weight"]]
visual_style["layout"] = layout_fr
visual_style["bbox"] = (600,600)
visual_style["margin"] = 20

ig.plot(g, **visual_style)

# Calculate DRL layout
layout_drl = g.layout("drl")

# Define style from network plotting
visual_style = {}
visual_style["vertex_size"] = 15
visual_style["vertex_label_size"] = 5
visual_style["vertex_color"] = "blue"
visual_style["vertex_label"] = g.vs["name"]
visual_style["edge_width"] = [5 * w for w in g.es["weight"]]
visual_style["layout"] = layout_drl
visual_style["bbox"] = (600,600)
visual_style["margin"] = 20

ig.plot(g, **visual_style)
#ig.plot(g, easygui.filesavebox(), **visual_style)

#
# PART 5: Shortest Path
#

# Node Sheppard Afb/Wichita Falls Mun
id1 = g.vs["name"].index("Sheppard Afb/Wichita Falls Mun")
id2 = g.vs["name"].index("West Tinian")
print("Sheppard Afb/Wichita Falls Mun = % 2d, West Tinian = % 2d" %(id1, id2))

# Nodes extracted from shortest path
path = g.get_shortest_paths(id1, id2)
print(path)

for n in path[0]:
    print("{}".format(g.vs[n]['id']))

# Edges extracted from shortest path
epath = g.get_shortest_paths(id1, id2, output='epath')
print(epath)

for n in epath[0]:
    print("edge: % 2d; % 2d -- % 2d" %(n, g.es[n].source, g.es[n].target))
    
# Visualize the shortest path in the Fruchterman-Reingold layout
vcolor = ["blue"]*g.vcount()
for n in path[0]:
    vcolor[n]="red"
    
ecolor = ["black"]*g.ecount()
for n in epath[0]:
    ecolor[n]="red"    

visual_style = {}
visual_style["vertex_size"] = 15
visual_style["vertex_label_size"] = 5
visual_style["vertex_color"] = "blue"
visual_style["vertex_label"] = g.vs["name"]
visual_style["edge_width"] = [5 * w for w in g.es["weight"]]
visual_style["layout"] = layout_fr
visual_style["bbox"] = (600,600)
visual_style["margin"] = 20

ig.plot(g, **visual_style)
#ig.plot(g, easygui.filesavebox(), **visual_style)

#
# PART 6: Export network and visualization
#

# filename = easygui.filesavebox()
# g.save(filename)

#ig.plot(g, easygui.filesavebox(), **visual_style)