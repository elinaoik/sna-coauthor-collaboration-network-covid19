#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 11:53:57 2020

@author: elinaoik
"""

from neo4j import GraphDatabase
import igraph as ig

driver = GraphDatabase.driver("neo4j://18.195.170.133:7687",
                              auth = ("neo4j", "alssn"),
                              encrypted = False)
session = driver.session()
print(session)

results = session.run("MATCH (n)-[r]-() RETURN count(distinct n) + count(distinct r) as cnt")

for result in results:
    print(result['cnt'])
    print(result)
    
edges = list()
edge_w = list()
vertices = set()

# Finds paths between all stops that are connected with all existing trips
results = session.run("match (n:Stop)<-[:PART_OF]-(:Stop)-[:LOCATED_AT]-(s:Stoptime)-[:PART_OF_TRIP]-(t:Trip {}) "\
  "-[:PART_OF_TRIP]-(:Stoptime)-[:LOCATED_AT]-(:Stop)-[:PART_OF]->(m:Stop) "\
  "where n.id<>m.id and t.id starts with 'IC'"\
  "return n,m, count(s) as cnt")
    
g = ig.Graph()

for result in results:
    vertices.add(str(result["n"]["name"]))
    vertices.add(str(result["m"]["name"]))
    edges.append([str(result["n"]["name"]), str(result["m"]["name"])])
    edge_w.append(1/result["cnt"])

g.add_vertices(list(vertices))
g.add_edges(edges)
g.es["weight"]=edge_w 

print(g.is_weighted())
print(g.ecount())

# Calculate layout
layout_fr = g.layout("fr")

# Define style from network plotting
visual_style = {}
visual_style["vertex_size"] = 1
visual_style["vertex_label_size"]=14
visual_style["vertex_color"] = "red"
visual_style["vertex_label"] = g.vs["name"]
visual_style["layout"] = layout_fr
visual_style["bbox"] = (2000, 3000)
visual_style["margin"] = 20

ig.plot(g, **visual_style)

# Task 1

result1 = session.run("match (leuven:Stop)-[PART_OF]-(ls:Stop)--(lst:Stoptime) "\
    "where toUpper(leuven.name)='LEUVEN' and lst.departure_time >=\"07:00:00\" and lst.departure_time <=\"08:00:00\" "\
    "with leuven,lst,ls "\
    "match (brugge:Stop)-[PART_OF]-(bs:Stop)--(bst:Stoptime) "\
    "where toUpper(brugge.name)='BRUGGE' and lst.departure_time < bst.arrival_time "\
    "with leuven,lst, brugge, bst,ls,bs "\
    "match p = shortestpath((lst)-[:PRECEDES*]-(bst)) "\
    "with leuven,ls,brugge,bs, lst,bst,nodes(p) as n "\
    "unwind n as nodes "\
    "match (nodes)-[:PART_OF_TRIP]->(t:Trip)-[:USES]-(route) "\
    "return bst,lst,route,leuven,ls,brugge,bs,t")

g1 = ig.Graph()

edges = list()
vertices = set()

for result in result1:
    vertices.add(str(result["leuven"]["name"]))
    vertices.add(str(result["brugge"]["name"]))
    vertices.add(str(result["bst"]["name"]))
    vertices.add(str(result["lst"]["name"]))
    vertices.add(str(result["ls"]["name"]))
    vertices.add(str(result["bs"]["name"]))
    edges.append([str(result["leuven"]["name"]), str(result["brugge"]["name"])])

g1.add_vertices(list(vertices))
g1.add_edges(edges)  

ig.summary(g1)
g1.is_weighted()

# Get the attributes and the number of nodes
print(g1.vs.attribute_names())
print(g1.vcount())

# Get the attributes and the number of edges
print(g1.es.attribute_names())
print(g1.ecount())              
                      
# Calculate layout
layout_fr = g1.layout("fr")

# Define style from network plotting
visual_style = {}
visual_style["vertex_size"] = 5
visual_style["vertex_label_size"]=24
visual_style["vertex_color"] = "red"
visual_style["vertex_label"] = g.vs["name"]
visual_style["layout"] = layout_fr
visual_style["bbox"] = (2000, 3000)
visual_style["margin"] = 20

ig.plot(g1, **visual_style)                     
                      