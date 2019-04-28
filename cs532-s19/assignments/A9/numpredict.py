import math


def knnestimate(data, vec1, k=5):
    # Get sorted distances
    dlist = getdistances(data, vec1)
    avg = 0.0

    # Take the average of the top k results
    for i in range(k):
        idx = dlist[i][1]
        avg += data[idx]['result']
    avg = avg / k

    return avg


def getdistances(data, vec1):
    distancelist = []

    # Loop over every item in the data set
    for i in range(len(data)):
        vec2 = data[i]['input']

        # Add the distance and the index
        distancelist.append((euclidean(vec1, vec2), i))

    # Sort by distance
    distancelist.sort()

    return distancelist


def euclidean(v1, v2):
    d = 0.0
    for i in range(len(v1)):
        d += (v1[i]-v2[i])**2
    return math.sqrt(d)
