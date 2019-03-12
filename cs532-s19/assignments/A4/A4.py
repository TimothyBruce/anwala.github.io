#!/usr/bin/env python3

import statistics as s
import matplotlib.pyplot as plt
import pylab
from tweepy import Stream
from tweepy import OAuthHandler
import tweepy
import urllib
import time

# Below are the Twitter API keys
auth = OAuthHandler("NJm6rzzKKSEIyBZfSG2KhJIeu", "YV1mrqxSMS7TnKuzPg71oCNLhGDo2JdR0F4H5clzL42abHjy23")
auth.set_access_token("88949861-GPwANfnvGAHlVkf9WN6Kp7yK3OIkMoQOHIJrR1DsN",
                      "4lDgep14e5hihu310yErW4176wD8LPhR4KTIf5seJA8Qx")
api = tweepy.API(auth)


def q1():
    f = open('acnwala-friendscount.csv', 'r')                    # Get the links.

    f.readline()

    data = []

    for line in f:
        data.append(int(line.split(", ")[1].rstrip("\n\r")))

    data.append(len(data))
    data.sort()

    friend_data_generator(data, "A. Nwala")


def q2(name):       #https://stackoverflow.com/questions/17431807/get-all-follower-ids-in-twitter-by-tweepy
    followers = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=name).pages():
        followers.extend(page)
        if len(page) > 5000:
            time.sleep(5)

    data = []
    for user in followers:
        ff = []                             #FF stands for "followers followers" nifty.
        for page in tweepy.Cursor(api.followers_ids, user_id=user).pages():
            ff.extend(page)
            if len(page) > 5000:
                time.sleep(60)
        data.append(len(ff))
        print(data[-1])
        time.sleep(60)

    data.append(len(data))
    data.sort()

    friend_data_generator(data, name)


def friend_data_generator(data, name):
    print("The mean number of friends" + name +"\'s friends has is: " + str(s.mean(data)))
    print("The standard deviation of friends" + name +"\'s friends has is: " + str(s.stdev(data)))
    print("The median of friends" + name +"\'s friends has is: " + str(s.median(data)))
    histogramGenerator(data, name)


def histogramGenerator(input_data, name):  # Get the mementos and create a histogram.
    y=[]
    friendNames = []
    for i in range(len(input_data)):
        y.append(i)
        if (input_data[i] == len(input_data)-1):
            friendNames.append(name)
        else:
            friendNames.append("f"+str(i))
    hist = plt.figure(num=None, figsize=(16, 6))  # Create a Bar plot.
                            #(BELOW) Create the bar chart.
    barPlot = plt.bar(y, input_data, align='edge')

    plt.xlabel('Friends')  #Label things.
    plt.ylabel('Individual\'s number of friends. (LOG Scale)')
    plt.yscale("log")
    plt.title(name + '\'s number of friends vs. Each friend\'s number of firends.')
    plt.xticks(y, friendNames, ha='right', rotation=45, fontsize=7)

    hist.savefig(name.rstrip(".")+".pdf", bbox_inches='tight')  # Save the histogram as a vector PDF.
    pylab.show()                                  #Display histogram in window for me.


def GetHTML(url):
    try:
        temp_html_reader = urllib.request.urlopen(url)  # Opens the page
    except urllib.error.URLError:
        return None

    return temp_html_reader.read()  # Returns the html code


q2("acnwala")
