#!/usr/bin/env python3

import sys
import os
import json
import urllib.request
import urllib.error

#Gets the header for the webpage. If the link is not claimed by any server or lacks a top level domain, it will raise an error.
def GetURLHeader(url):
    try:
        temp_html_reader = urllib.request.urlopen(url)              #Opens the page
    except urllib.error.URLError:
        raise BadLinkError
    
    return temp_html_reader.info()                                  #Returns the header.

def GetFinalURL(url):
	try:
        	temp_html_reader = urllib.request.urlopen(url)              #Opens the page
	except urllib.error.URLError:
        	raise BadLinkError
	return temp_html_reader.geturl()

def getSuccessfulLink(url):
	try:
		x = GetFinalURL(url)
		sys.stdout.write("\033[K")
		return x
	except(AttributeError,NameError):
		pass
	except:
		pass
	return None

def getUrlsFromTweet(file):
	return json.loads(file.read())["entities"]["urls"]

def filterUrlsDomain(urls, domainName):
	filtered = []
	for url in urls:
		if domainName not in url["expanded_url"]:
			filtered.append(url["expanded_url"])
	return filtered

def main():
	counter = 0
	totalTweetsCompleted = 0

	for file in os.listdir(str(os.getcwd())+"/Tweets"):
		completion = totalTweetsCompleted/len(os.listdir(str(os.getcwd())+"/Tweets")) * 100
		totalTweetsCompleted += 1
		sys.stdout.write("\033[K")
		print(str(completion) + "% complete")
		sys.stdout.write("\033[F")

		f = open(str(os.getcwd())+"/Tweets/"+file,"r")
		urls = getUrlsFromTweet(f)
		f.close()
		urls = filterUrlsDomain(urls, "twitter.com")

		if len(urls) > 0:
			for url in urls:
				successfulUrl = getSuccessfulLink(url)
				if successfulUrl != None:
					#sys.stdout.write("\033[K")
					#print(successfulUrl)
					f=open("unfilteredlinks.txt", "a+")
					f.write(successfulUrl + "\n")
					f.close

			counter += 1

	print(str(counter) + " links collected")
main()

#Need to check that they lead to the endpoint and hash them to ensure that each link is unique. Then write them all to a file in a meaningful way. Maybe by domain -> alphabetically.
