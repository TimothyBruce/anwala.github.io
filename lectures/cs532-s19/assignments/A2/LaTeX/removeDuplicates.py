def removeDuplicates(urls): # This function removes duplicate URIs.
    x = dict()              # Dictionary for storing hashed URIs.
    for url in urls:
        h = hash(url)       # Basic Python hash function appears to be appropriate for this use case.
        if h not in x:      # If hash does not yet exist.
            x[h] = [url, 1] # Add the hash and a counter for duplicate URIs.
        else:               # Else, hash does exist.
            if x[h][0] != url:# Check to see if hash has duplicated a key incorrectly.
                raise Exception("Something is wrong with the hash")
            i = x[h]
            x[h] = [i[0], i[1] + 1]# Add to the counter.
    links = []
    for site in x:          # Add one of each hashed link to the output list.
        links.append(x[site][0])
    links.sort()            # Sort the output into alphabetical order.
    return links
