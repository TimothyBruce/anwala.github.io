import urllib
import requests
import feedparser
from bs4 import BeautifulSoup as bs4
import time
from HTMLParser import HTMLParser
import random as r
import clusters


def main():
    stopWords = []
    swtxt = open("stopwords.txt", "r")
    for line in swtxt.readlines():
        stopWords.append(line.split("\n")[0])
    listOfWordsBySite = {}

    #x =findfeed("https://f-measure.blogspot.com")
    #print(x)
    #getwordcounts(x[0])
    #words = getWords('https://f-measure.blogspot.com/feeds/posts/default?alt=rss')
    #print(words)
    URLS = getURLS()
    print(URLS)
    #URLS = ['https://therecipefile23-index.blogspot.com/2010/05/my-mums-spottier-dick.html']

    rsss = []
    for url in URLS:
        rss = findfeed(url)
        if len(rss) > 0:
            """
            words = getWords(rss[0])
            wordsDict = {}
            for word in words[1]:
                if word in wordsDict.keys() and word.lower() not in stopWords:
                    wordsDict[word] += 1
                elif word.lower() not in stopWords:
                    wordsDict[word] = 1
            listOfWordsBySite[words[0]] = wordsDict
            """
            rsss.append(rss[0])

    file = open('feedlist.txt', 'w')
    for rss in rsss:
        file.write(rss + "\n")
    file.close()


# Returns title and dictionary of
# word counts for an RSS feed


def popularTerms(listOfWordsBySite):
    words = {}
    for site in listOfWordsBySite:
        for word in listOfWordsBySite[site]:
            if word in words.keys():
                words[word] += 1
            else:
                words[word] = 1
    if len(words) > 1000:
        return sorted(words.items(), key=lambda x: -x[1])[:1000]
    else:
        return sorted(words.items(), key=lambda x: -x[1])[:len(words)-1]


def getURLS():
    output = []
    f = open("blogs.txt", "r")
    for url in f.readlines():
        output.append(url.split("\n")[0])
    return output


def getWords(url):
    output = []
    # Parse the feed
    d = feedparser.parse(url)
    wc = {}

    # Loop over all the entries
    # description==RSS; summary==Atom
    for e in d.entries:
        for value in e.title.split():
            nopunct = noPunctuation(value)
            if nopunct != "":
                output.append(nopunct)
    return [d.feed.title, output]


def noPunctuation(punctualString):  # https://www.programiz.com/python-programming/examples/remove-punctuation
    punct = '''!()-[]{};:'"\,<>./?@#$%^&*_~1234567890'''
    notPunctualString = ""
    for char in punctualString:
        if char not in punct:
            notPunctualString = notPunctualString + char
    return notPunctualString


def findfeed(site):
    """
    From user alexmill on github, this is a truly spectacular bit of code. Be cautious of 404 errors, because they
    cause the program to spin its wheels. Other than that it tends to find the rss feed every time one is present.
    https://gist.github.com/alexmill/9bc634240531d81c3abe
    """
    print(site)
    raw = requests.get(site).text
    result = []
    possible_feeds = []
    html = bs4(raw, features="html.parser")
    feed_urls = html.findAll("link", rel="alternate")
    for f in feed_urls:
        t = f.get("type", None)
        if t:
            if "rss" in t or "xml" in t:
                href = f.get("href", None)
                if href:
                    possible_feeds.append(href)
    parsed_url = urllib.parse.urlparse(site)
    base = "https" + "://" + parsed_url.hostname
    atags = html.findAll("a")
    for a in atags:
        href = a.get("href", None)
        if href:
            if "xml" in href or "rss" in href or "feed" in href:
                possible_feeds.append(base + href)
    for url in list(set(possible_feeds)):
        blacklist = open("blacklistUrls.txt", "r")
        bl = []
        for item in blacklist.readlines():
            bl.append(item.split("\n")[0])
        if url not in bl and "https://" not in url[1:] and "http://" not in url[1:]:
            f = feedparser.parse(url)
            if len(f.entries) > 0:
                if url not in result:
                    result.append(url)
    return (result)


def getBlogs():
    try: 
        from googlesearch import search 
    except ImportError:  
        print("No module named 'google' found")

    finalResults = []
    for query in getNewWords():
        print(query)
        queryResults = []
        query = query + " .blogspot.com"
        time.sleep(60)
        for j in search(query, num=10, stop=20, pause=2):
            if ".blogspot.com" in j:
                queryResults.append(j)
                f =open("blogs.txt", "a")
                f.write(j)
                f.write('\n')
                f.close()
        finalResults.append(queryResults)
        print(queryResults[0])
    print(finalResults)


def getNewWords():
    words = randomWords(10)
    return words


def getResultFromSearchTerm(term):
    link = "https://www.searchblogspot.com/search?q=" + term
    fp = urllib.request.urlopen(link)
    mybytes = fp.read()
    text = mybytes.decode("utf8")
    fp.close()

    print(text)
    parser = MyHTMLParser()
    parser.feed(text)


def randomWords(numberOfWords):
    words = []
    f = open("wordsEn.txt")
    for word in f.readlines():
        words.append(word.split("\n")[0])
    searchTerms = []
    for i in range(numberOfWords):
        searchTerms.append(words[r.randint(0, len(words)-1)])
    return searchTerms


class MyHTMLParser(HTMLParser):
    flag = False
    def handle_starttag(self, tag, attrs):
        if tag == "link":
            self.flag = True
            for value in attrs:
                if value[0] == 'href':
                    print(value[1])

    def handle_endtag(self, tag):
        self.flag = False

    def handle_data(self, data):
        if self.flag == True:
            print("Encountered some data  :", data)

def printkclustValues(kclust):
    print(kclust)
    for value in kclust:
        names = [blognames[blogIndex] for blogIndex in value]
        print(names)

#getBlogs()
#main()

blognames,words,data=clusters.readfile('blogdata.txt')
print(blognames)
print(words)
print(data)
for i in range(len(data[1:])):
    if len(data[i+1]) != len(data[i]):
        print(blognames[i+1])
        print(len(data[i+1]))
        print(blognames[i])
        print(len(data[i]))
clust = clusters.hcluster(data)
clusters.printclust(clust, labels=blognames)
clusters.drawdendrogram(clust, blognames, jpeg='blogclust.jpg')

kclust=clusters.kcluster(data, k=5)
printkclustValues(kclust)
kclust=clusters.kcluster(data, k=10)
printkclustValues(kclust)
kclust=clusters.kcluster(data, k=20)
printkclustValues(kclust)
coords=clusters.scaledown(data)
clusters.draw2d(coords,blognames,jpeg='blogs2d.jpg')