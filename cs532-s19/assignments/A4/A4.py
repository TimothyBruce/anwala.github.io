#!/usr/bin/env python3

import statistics as s
import matplotlib.pyplot as plt
import pylab


f = open('acnwala-friendscount.csv', 'r')                    # Get the links.

print(f.readline())

data = []

for line in f:
    data.append(int(line.split(", ")[1].rstrip("\n\r")))

print(data)
print("The mean number of friends is: " + str(s.mean(data)))
print("The standard deviation of friends is: " + str(s.stdev(data)))
print("The median of friends is: " + str(s.median(data)))

data.append(len(data))
data.sort()




def histogramGenerator(input_data):  # Get the mementos and create a histogram.
    y=[]
    friendNames = []
    for i in range(len(input_data)):
        y.append(i)
        if (input_data[i] == len(data)-1):
            friendNames.append("A. Nwala")
        else:
            friendNames.append("f"+str(i))
    hist = plt.figure(num=None, figsize=(16, 6))  # Create a Bar plot.
                            #(BELOW) Create the bar chart.
    barPlot = plt.bar(y, input_data, align='edge')

    plt.xlabel('Friends')  #Label things.
    plt.ylabel('Individual\'s number of friends. (LOG Scale)')
    plt.yscale("log")
    plt.title('Alexander Nwala\'s friends in 2014 vs. Each friend\'s number of firends.')
    plt.xticks(y, friendNames, ha='right', rotation=45, fontsize=7)

    hist.savefig("foo.pdf", bbox_inches='tight')  # Save the histogram as a vector PDF.
    pylab.show()                                  #Display histogram in window for me.

histogramGenerator(data)
