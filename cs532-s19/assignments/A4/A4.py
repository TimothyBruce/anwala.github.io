#!/usr/bin/env python3

import math as m
import statistics as s

f = open('acnwala-friendscount.csv', 'r')                    # Get the links.

print(f.readline())

data = []

for line in f:
    data.append(int(line.split(", ")[1].rstrip("\n\r")))

print(data)
print("The mean number of friends is: " + str(s.mean(data)))
print("The standard deviation of friends is: " + str(s.stdev(data)))
print("The median of friends is: " + str(s.median(data)))