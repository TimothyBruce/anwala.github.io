#!/usr/bin/env python3
from igraph import *
import re

def main():
    g = Graph()

    data = get_data()
    verteces = []
    for value in data:
        g, verteces = check_vertex_list(value, verteces, g)
        g.add_edge(str(value[0]), str(value[1]))

    g.vs["label"] = g.vs["name"]
    layout = g.layout_auto()#g.layout("kk")

    counter = 0
    while len(g.es) != 0 and counter < 200:
        counter += 1
        layout = g.layout_auto()
        ebs = g.edge_betweenness()
        delete = []
        for idx, eb in enumerate(ebs):
            if eb == max(ebs):
                if "color" in g.es[idx].attributes().keys() and g.es[idx]["color"] == "blue":
                    delete.append(g.es[idx])
                else:
                    g.es[idx]["color"] = "blue"

        f = True
        for d in delete:
            print("Deleted: " + g.vs[d.source]["name"] + ", " + g.vs[d.target]["name"])
            g.delete_edges(d)
            f = False

        if f:
            p = plot(g, layout=layout)
            #pngs.add()
            p.save("mostRecent.png")

def check_vertex_list(vertex_list, verteces, g):
    for value in vertex_list:
        if value not in verteces:
            g.add_vertex(str(value))
            verteces.append(value)
            colorList = [9, 10, 15, 16, 19, 21]
            if value >= 23 or value in colorList:
                g.vs.find(str(value))["color"] = "blue"
    return g, verteces


def get_data():
    f = open("karate_club_data.txt", "r")
    data = []
    for line in f.readlines():
        m = re.findall("\d+", str(line))
        if m:
            for i in range(int(len(m)/2)):
                data.append([int(m[i*2]), int(m[(i*2)+1])])
    return data



main()