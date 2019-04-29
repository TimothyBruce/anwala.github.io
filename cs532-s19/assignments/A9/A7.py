import requests
from bs4 import BeautifulSoup as bs4
import clusters
import math
from scipy import spatial


def links(url):
    html = requests.get(url).content
    bsObj = bs4(html, 'lxml')

    links = bsObj.findAll('a')
    finalLinks = set()
    for link in links:
        finalLinks.add(link.attrs['href'])


# Returns title and dictionary of
# word counts for an RSS feed

def popularTerms(data, wordorder):
    # Gets the most popular 1000 words from the dataset (or all of the words).
    words = {}

    for wordKey in range(len(wordorder)):
        word = wordorder[wordKey]
        wordcount = 0
        for line in data:
            wordcount += int(line[wordKey])
        if word in words.keys():
            words[word] += wordcount
        else:
            words[word] = wordcount
    if len(words) > 1000:
        return sorted(words.items(), key=lambda x: -x[1])[:1000]
    else:
        return sorted(words.items(), key=lambda x: -x[1])[:len(words)-1]


def blog_term_matrix(popTerms, data, words, blogNames):
    # Creates the blog-term matrix for all of the blogs.
    website_matricies = []
    for site in blogNames:
        website_matricies.append([site, get_blog_term_matrix(popterms, data[blogNames.index(site)], words)])

    return website_matricies


def get_blog_term_matrix(popTerms, site_data, words):
    # Creates the blog term matrix for a single website.
    matrix = []
    for item in popTerms:
        word_index = words.index(item[0])
        matrix.append(site_data[word_index])

    return matrix

def printkclustValues(kclust):
    print(kclust)
    for value in kclust:
        names = [blognames[blogIndex] for blogIndex in value]
        print(names)


def knnestimate(data, vec1, k=5):
    # Get sorted distances
    dlist = getdistances(data, vec1)
    avg = []

    # Take the average of the top k results
    for i in range(k):
        avg.append(data[dlist[i][1]][0])

    return avg


def getdistances(data, vec1):
    distancelist = []

    # Loop over every item in the data set
    for i in range(len(data)):
        vec2 = data[i][1]

        # Add the distance and the index
        if vec1 != vec2:
            distancelist.append((spatial.distance.cosine(vec1, vec2), i))

    # Sort by distance
    distancelist.sort()

    return distancelist


def euclidean(v1, v2):
    d = 0.0
    for i in range(len(v1)):
        d += (v1[i]-v2[i])**2
    return math.sqrt(d)

blognames, words, data = clusters.readfile('blogdata.txt')
# print(blognames)    # row
# print(words)       # columns
# print(data)        # data
popterms = popularTerms(data, words)
btm = blog_term_matrix(popterms, data, words, blognames)

for blog in btm:
    if blog[0] == "F-Measure" or blog[0] == "ws-dl":
        print(blog[0])
        print(btm.index(blog))
        print(knnestimate(btm, btm[btm.index(blog)][1], 20))
