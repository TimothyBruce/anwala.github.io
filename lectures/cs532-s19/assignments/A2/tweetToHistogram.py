#!/usr/bin/env python3

import argparse
import sys
import datetime as t
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import urllib.request
import urllib.error
import matplotlib.pyplot as plt
import pylab
import math
import numpy as np

# Below are the Twitter API keys
auth = OAuthHandler("d15DI0RupmimlyDiQUUYLr1Ha", "UI7GPwdN0R0PmGbAsFuhhw9j53X1yvEqcowbFrP22lOhjvJIsB")
auth.set_access_token("88949861-GPwANfnvGAHlVkf9WN6Kp7yK3OIkMoQOHIJrR1DsN",
                      "4lDgep14e5hihu310yErW4176wD8LPhR4KTIf5seJA8Qx")


# Main is called from the command line with three parameters:
# 1. Duration in minutes as a whole integer. This controls how long it'll stream tweets for.
# 2. Keyword that the Twitter API will look for.
# 3. existing_data is a boolean value that if True will cause the program to look for tweets.json and
# #	pull tweets from there before deleting them.
def is_int(val):
    try:
        int(val)
    except:
        return False
    return True


def main():
    argument_parser = argparse.ArgumentParser(description='Streaming and learning from Tweets')
    argument_parser.add_argument('--stream', '-s',
                                 help='Steam Tweets. Write streaming duration in minutes followed by the keyword you are looking for.',
                                 nargs=2)
    argument_parser.add_argument('--parseLinks', '-p', help='Parse and format links in all Tweets in tweets.json',
                                 action='store_true')
    argument_parser.add_argument('--mementoDict', '-md',
                                 help='Create a dictionary of the number of links that have a number of mementos.',
                                 action='store_true')
    argument_parser.add_argument('--histogram', '-H',
                                 help='Create a histogram of the number of links that have a number of mementos.',
                                 action='store_true')

    args = argument_parser.parse_args()

    if args.stream:
        if is_int(args.stream[0]):
            stream = True
            duration = int(args.stream[0])
            keyword = args.stream[1]
        elif is_int(args.stream[1]):
            stream = True
            duration = int(args.stream[1])
            keyword = args.stream[0]
        else:
            stream = False
            print("ERROR! INVALID DURATION!")

    if args.stream and duration != 0:
        data = streamTwitter(duration, keyword)
        print("Done streaming.")
        print("Got " + str(len(data)) + " tweets.")
    else:
        f = open('tweets.json', 'r')  # Get old data
        data = json.load(f)['tweets']
        f.close()

    if args.parseLinks:
        links = parseLinks(data)
        print("Done parsing links.")
        print("Out of " + str(len(data)) + " tweets, there were " + str(len(links)) + " unique successful links.")
        print("That is a " + str(round((len(links)/len(data))*100, 2)) + "% success rate.")
    else:
        f = open('hashedlinks.txt', 'r')
        links = []
        for line in f:
            links.append(line.rstrip("\n\r"))
        f.close()

    if args.mementoDict:
        memento_dictionary = memento_counter(links)
        print("Done getting mementos.")
        print(str(round((len(links) - memento_dictionary['0'])/len(links)*100, 2)) + "% of links had mementos.")
    else:
        try:
            f = open('mementos.json', 'r')  # Save the tweets for future use.
            memento_dictionary = json.load(f)
            f.close()
        except:
            print("No mementos.json file created yet.")

    if args.histogram:
        histogramGenerator(memento_dictionary)  # Generate the histogram, including memento retrieval.


def parseLinks(JSONTweets):
    links = []
    for tweet in JSONTweets:  # For every tweet
        for url in tweet['links']:
            if url != []:  # If there is a URI in the tweet
                links.append(url['expanded_url'])  # Add the URI to the list.
    urls = filterUrlsDomain(links, "twitter.com")  # Remove twitter domain URIs.

    counter = 0
    unfiltered_successful_urls = []
    if len(urls) > 0:  # Follow all redirects until code 200.
        for url in urls:  # (below) actually gets the successful link.
            #Tracker Section
            sys.stdout.write("\033[K")
            print("Parsing links " + str(round((counter / len(urls)) * 100, 2)) + "% complete.")
            sys.stdout.write("\033[F")
            counter += 1

            successfulUrl = getSuccessfulLink(url)
            if successfulUrl != None:  # If the tweet has a successful link, add it to the list.
                unfiltered_successful_urls.append(successfulUrl)
    # (below) remove duplicate links.
    complete_urls = removeDuplicates(unfiltered_successful_urls)

    f = open("hashedlinks.txt", 'w')  # Write the URLs to a file.
    for link in complete_urls:
        f.write(link + "\n")
    f.close()

    return complete_urls


#A lot of this code comes from https://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/
def streamTwitter(duration, keyword):
    f = open('tweets.json', 'r')  # Get old data
    old_data = json.load(f)['tweets']
    f.close()
    # (below)Stream Twitter for Duration.
    twitterStream = Stream(auth, listener(t.timedelta(minutes=int(duration)), old_data))
    twitterStream.filter(track=[keyword])

    # (below)Return all of the Tweets.
    return json.load(open('tweets.json', 'r'))['tweets']


class listener(StreamListener):  # The SteamListener streams the tweets.
    def __init__(self, duration=1, existing_data=[]):
        self.endTime = t.datetime.now() + duration  # This is the timer.
        self.counter = 0
        self.tweets = {}  # This is where all of the tweets are stored.
        self.tweets['tweets'] = existing_data  # These are the historical tweets being added.

    def on_data(self, data):
        json_new_data = json.loads(data)  # Format the data as JSON
        json_data = {}  # Place to store all of the tweets.
        json_data['text'] = json_new_data['text']  # Store the tweet text.
        json_data['links'] = json_new_data['entities']['urls']  # Store the URIs.
        json_data['time'] = json_new_data['created_at']  # Store the creation date.
        self.tweets['tweets'].append(json_data)  # Add the tweet to the list of tweets.
        f = open('tweets.json', 'w')  # Save the tweets for future use.
        json.dump(self.tweets, f)
        f.close()

        #Timer and countdown area
        time_remaining = self.endTime - t.datetime.now()
        output_string = "Time remaining for streaming Tweets is "
        sys.stdout.write("\033[K")
        if int(math.floor(time_remaining.seconds/60)) > 1:
            output_string = output_string + str(math.floor(time_remaining.seconds/60)) + " minutes"
        elif int(math.floor(time_remaining.seconds/60)) == 1:
            output_string = output_string + str(math.floor(time_remaining.seconds/60)) + " minute"

        if int(time_remaining.seconds%60) != 0 and int(math.floor(time_remaining.seconds/60)) != 0:
            output_string += " and "
        elif int(time_remaining.seconds%60) == 0 and int(math.floor(time_remaining.seconds/60)) == 0:
            output_string = "Done"


        if int(time_remaining.seconds % 60) != 0:
            if int(time_remaining.seconds%60) > 1:
                output_string = output_string + str(int(time_remaining.seconds%60)) + " seconds."
            elif time_remaining.seconds%60 == 1:
                output_string = output_string + str(int(time_remaining.seconds%60)) + " second."
        else:
            output_string += "."

        print(output_string)
        sys.stdout.write("\033[F")
        self.counter += 1
        if self.endTime > t.datetime.now():  # If the timer has not expired,
            return True  # continue.
        else:  # If the timer has expired,
            return False  # stop.

    def on_error(self, status):
        print(status)


def filterUrlsDomain(urls, domainName):  # Filter links out of a list that contain domainName.
    filtered = []  # Final list of links stored here.
    for url in urls:  # For every URI,
        if domainName not in url:  # If domainName is not in the link,
            filtered.append(url)  # Add the URI to the list.
    return filtered  # The weakness of this program is the lack of ability to
    #       deal with the domainName being later in the link.


def getSuccessfulLink(url):  # This function follows redirects until a 200 is returned
    try:  # or there is a timeout.
        x = GetFinalURL(url)
        sys.stdout.write("\033[K")
        return x
    except(AttributeError, NameError, TimeoutError):
        pass
    except:
        pass
    return None


def GetFinalURL(url):  # This function is a worker for the getSucessfulLink Function.
    try:
        temp_html_reader = urllib.request.urlopen(url)  # Opens the page using urllib.
    except urllib.error.URLError:
        raise TimeoutError
    return temp_html_reader.geturl()  # This is used to see if a redirect was followed. It returns
    #       the final URI.


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

def histogramGenerator(hashed_links):  # Get the mementos and create a histogram.
    matplot_understandable = fix_json_to_matplotlib(hashed_links)
    hist = plt.figure()  # Create a histogram for the memento data.
                            #(BELOW) Create the histogram.
    histogram = plt.hist(matplot_understandable,  bins=[0, 1, 2, 3, 4, 5, 6, 7, 8], align='left', rwidth=0.8)

    plt.xlabel('Mementos')  #Label things.
    plt.ylabel('Number of URIs With Memento Count (LOG Scale)')
    plt.yscale("log")
    plt.title('Frequency of URIs With Given Memento Count Among Tweets With Keyword \'nasa\'')
    xKey = ['0', '1', '2', '3-10','11-15','16-20','21-25','25+']
    xTicks = [0, 1, 2, 3, 4, 5, 6, 7]
    plt.xticks(xTicks, xKey)

    for rect in histogram[2]:#Label bars. This was found in the matplotlib documentation.
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., 1.03*height,
                '%d' % int(height),
                ha='center', va='bottom')

    hist.savefig("foo.pdf", bbox_inches='tight')  # Save the histogram as a vector PDF.
    pylab.show()                                  #Display histogram in window for me.

def fix_json_to_matplotlib(hashed_links):   #Puts data into format readable by matplotlib.hist.
    values = []
    for key in hashed_links.keys():
        for i in range(hashed_links[key]):
            values.append(int(key))

    histogram_appropriate = []
    for val in values:
        if val == 0:
            histogram_appropriate.append(0)
        elif val == 1:
            histogram_appropriate.append(1)
        elif val == 2:
            histogram_appropriate.append(2)
        elif val > 2 and val <= 10:
            histogram_appropriate.append(3)
        elif val > 10 and val <= 15:
            histogram_appropriate.append(4)
        elif val > 15 and val <= 20:
            histogram_appropriate.append(5)
        elif val > 20 and val <= 25:
            histogram_appropriate.append(6)
        elif val > 25:
            histogram_appropriate.append(7)

    return histogram_appropriate

def memento_counter(urls):
    totalLinksCompleted = 0
    fileLength = len(urls)
    x = dict()  # Dictionary of all histogram values.
    y = []
    for line in urls:  # For every URL
        # Tracker Section
        sys.stdout.write("\033[K")
        print("Parsing links " + str(round((totalLinksCompleted / fileLength) * 100, 2)) + "% complete.")
        sys.stdout.write("\033[F")
        totalLinksCompleted += 1  # These are a sanity percentage output.

        line = line.rstrip("\n\r")  # Get mementos.
        raw_json = GetHTML("http://memgator.cs.odu.edu/timemap/json/" + line)
        if raw_json != None:
            full_json = json.loads(raw_json)  # (below) get the length of mementos.
            mementos = len(full_json["mementos"]["list"])
            y.append(mementos)
            if mementos in x:  # Add to the dictionary using the memento length as the key.
                x[mementos] += 1
            else:
                x[mementos] = 1
        else:
            if '0' in x:  # If there are no mementos, add a 0 memento link.
                x['0'] += 1
            else:
                x['0'] = 1
        f = open('mementos.json', 'w')  # Save the tweets for future use.
        json.dump(x, f)
        f.close()
    return x


def alternate():  # Get the length of the hashed links.
    f = open("hashedlinks.txt", 'r')
    counter = 0
    for line in f:
        counter += 1
    return counter


# Gets the html code for the webpage. If the link is not claimed by any server or lacks a top level domain, it will raise an error.
def GetHTML(url):
    try:
        temp_html_reader = urllib.request.urlopen(url)  # Opens the page
    except urllib.error.URLError:
        return None
    except:
        return None

    return temp_html_reader.read()  # Returns the html code


main()
