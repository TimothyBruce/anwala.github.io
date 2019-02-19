#!/usr/bin/env python3

import urllib.request
import urllib.error

f = open('hashedlinks.txt','r')
for url in f.readlines():
	print("http://localhost:8000/timemap/json/" + url.rstrip('\n'))
	temp_html_reader = urllib.request.urlopen("http://localhost:8888/timemap/json/" + url.rstrip('\n'))
	print(temp_html_reader.read())

#GET http://localhost:8888/cd/http://www.cs.odu.edu/
