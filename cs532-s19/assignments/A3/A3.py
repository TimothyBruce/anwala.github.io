#!/usr/bin/env python3

import urllib.request as ul
import urllib.error as ule
import sys
from boilerpipe.extract import Extractor
import json
import math
import scipy.stats as stats





def saveHtml():
    f = open('hashedlinks.txt', 'r')                    # Get the links.
    links = []
    for line in f:
        links.append(line.rstrip("\n\r"))               # Put the links in a list.

    counter = 0
    html_dump = dict()                                  # All of the HTML Data goes here.

    for link in links:                                  # For every link
        # Stressed human loading bar
        sys.stdout.write("\033[K")
        print("Getting HTML " + str(round((counter / len(links)) * 100, 2)) + "% complete.")
        sys.stdout.write("\033[F")
        counter += 1

        try:
            html_data = get_html(link)                  # Get the HTML Code
        except:
            pass

        if html_data != None:
            html_dump[link] = html_data

    to_save_link_text = dict()                          # JSON is outputted from here.

    for key in html_dump.keys():                        # For everything in html dump
        raw_html = html_dump[key]                       # The raw html.

        ex = Extractor(extractor='ArticleExtractor', html=raw_html)
        text = ex.getText()                      # The parsed html.

        linkdict = dict()                               # This is where the clean formatted data goes.
        linkdict['raw_html'] = str(raw_html)            # Put in the raw html.
        linkdict['clean_html'] = str(text)              # Put in the clean text.
        linkdict['link'] = str(key)                     # Put in the link for output.

        to_save_link_text[hash(key)] = linkdict

    f = open('html_data.json', 'w')                     # Save the html for future use.
    json.dump(to_save_link_text, f)
    f.close()


# Gets the html code for the webpage. If the link is not claimed by any server or
#   lacks a top level domain, it will raise an error.
def get_html(url):
    try:
        temp_html_reader = ul.urlopen(url)              # Opens the page.
    except ule.URLError:
        return None

    return temp_html_reader.read()                      # Returns the html code.

#Calculate tfidf and output in requested format.
def tf_idf(searchTerm, IDF):
    f = open('html_data.json', 'r')                     # Get old data.
    data = json.load(f)
    f.close()

    print("TFIDF	TF	    IDF	        URI")
    print("-----	--	    ---	        ---")           # (below) Initialize data storage list.
    outputList = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]
    for key in data.keys():                             # For every link.
        clean_html = data[key]['clean_html']            # Get the clean text.
        instances = clean_html.count(searchTerm)        # Get count of of instances of the search term in the text.
        words = clean_html.split(' ')
        word_count = len(words)                         # Get word count of clean text.
        tf = instances/word_count                       # Calculate tf value.
        tfidf = (instances/word_count) * IDF            # Calculate tf-idf value.
        if round(tf, 3) != 0:                           # (below) store all relevant data.
            outputList = little_sorter(outputList, tfidf, str(round_sig(tfidf, 3)) + "   " + str(round_sig(tf, 3)) + "       " + str(round_sig(IDF, 3)) + "     " + data[key]['link'])

    for data in outputList:
        print(data[1])                                  # Print the data


# Sorts the links by tf-idf value, maximum to minimum.
def little_sorter(list, newVal, fullLine, extraData = None):
    listCounter = 0
    nlist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(12):                                 # Find the maximum value 12 times. (NOTE in homework output will only display 10. Two results are bad bad bad.
        if newVal > list[listCounter][0]:
            nlist[i] = [newVal, fullLine, extraData]
            newVal = 0
        else:
            nlist[i] = list[listCounter]
            listCounter += 1

    return nlist


# Calculate idf based on number of google search results.
def idf(results_in_engine):
    return math.log(130000000000000/results_in_engine, 2.0)


# Rounds to sig figs. From user Stephen Rauch at location https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
def round_sig(x, sig=2):
    return round(x, sig-int(math.floor(math.log10(abs(x))))-1)


# Uses the scipy library to calculate kendal tau b. Turns out its a basic function ¯\_(ツ)_/¯.
def kendallTauCalculation(a1, a2):
    return stats.kendalltau(a1, a2)

#saveHtml()
tf_idf('opportunity', idf(3170000000))                  # Calculate tf-idf and output it.


tfidf_values = [0.356, 0.288, 0.214, 0.214, 0.158, 0.151, 0.15, 0.124, 0.123, 0.114]
page_rank = [9.2, 8.5, 8.7, 8.9, 8.5, 8.5, 8.5, 8.5, 8.5, 8.6]
alexa = [1721, 814, 934, 1462, 814, 162, 814, 4914, 4914, 597]  # https://www.rank2traffic.com/
print("FOR TFIDF AND PAGERANK")
print(kendallTauCalculation(tfidf_values, page_rank))

print("FOR TFIDF AND alexa")
print(kendallTauCalculation(tfidf_values, alexa))

print("FOR alexa AND PAGERANK")
print(kendallTauCalculation(alexa, page_rank))





tfidf_values = [0.967, 0.0579, 0.0126, 0.151, 0.022, 0.0234, 0.0196, 0.05, 0.0692, 0.03]
page_rank = [9.5, 10.0, 8.5, 8.5, 7.5, 2.5, 3.7, 4.0, 8.9, 6.7]
print("FOR RANDOM")
print(kendallTauCalculation(tfidf_values, page_rank))
