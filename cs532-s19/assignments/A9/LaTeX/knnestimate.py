def knnestimate(data, vec1, k=5):
    # Get sorted distances
    dlist = getdistances(data, vec1)
    avg = []

    # Take the average of the top k results
    for i in range(k):
        avg.append(data[dlist[i][1]][0])

    return avg
