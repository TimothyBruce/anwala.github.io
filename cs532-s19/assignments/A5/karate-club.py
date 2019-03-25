#!/usr/bin/env python3
from igraph import *
import re


def main():
    g = Graph()                                     # The initializer for the graph.

    data = get_data()                               # Calls the get_data function which is below.
    vertices = []
    for value in data:                              # For every value
        g, vertices = check_vertex_list(value, vertices, g)
        g.add_edge(str(value[0]), str(value[1]))    # Generate the edges and vertices.

    g.vs["label"] = g.vs["name"]                    # Label the nodes in the chart.
    layout = g.layout_auto()

    counter = 0
    while len(g.es) != 0 and counter < 200:         # While the are edges and no more than 200 times (prevents error).
        counter += 1
        layout = g.layout_auto()
        ebs = g.edge_betweenness()                  # Calculate the betweenness of all edges.
        delete = []
        for idx, eb in enumerate(ebs):              # For every edge
            if eb == max(ebs):                      # If it is the edge with max betweenness
                if "color" in g.es[idx].attributes().keys() and g.es[idx]["color"] == "blue":
                    delete.append(g.es[idx])        # If it's highlighted blue, delete it.
                else:                               # Otherwise, highlight it blue.
                    g.es[idx]["color"] = "blue"

        f = True
        for d in delete:                            # This block actually deletes the edges to be deleted.
            print("Deleted: " + g.vs[d.source]["name"] + ", " + g.vs[d.target]["name"])
            g.delete_edges(d)
            f = False

        if f:                                       # Plot and save the graph.
            p = plot(g, layout=layout)
            #pngs.add()
            p.save("mostRecent.png")


def check_vertex_list(vertex_list, vertices, g):    # If the vertex does not exist, this function creates it.
    for value in vertex_list:
        if value not in vertices:
            g.add_vertex(str(value))
            vertices.append(value)
            colorList = [9, 10, 15, 16, 19, 21]     # These are the number node exceptions in the blue group.
            if value >= 23 or value in colorList:
                g.vs.find(str(value))["color"] = "blue"
    return g, vertices


def get_data():                                     # Get the data from the text file.
    f = open("karate_club_data.txt", "r")
    data = []
    for line in f.readlines():
        m = re.findall("\d+", str(line))            # Find all the numeric characters.
        if m:
            for i in range(int(len(m)/2)):
                data.append([int(m[i*2]), int(m[(i*2)+1])])
    return data


main()
