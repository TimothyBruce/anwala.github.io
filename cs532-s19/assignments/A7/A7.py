import random as r
import urllib.request
from html.parser import HTMLParser
import google


def main():
    try: 
        from googlesearch import search 
    except ImportError:  
        print("No module named 'google' found") 
  
    # to search 
    query = "Test"
  
    for j in search(query, tld="blogspot.com", num=10, stop=1, pause=2): 
        print(j) 

def t():
    words = randomWords(1)
    links = []
    for value in words:
        result = getResultFromSearchTerm(value)


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
        searchTerms.append(words[r.randint(0,len(words)-1)])
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

main()
