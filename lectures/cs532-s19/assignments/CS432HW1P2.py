#!/usr/bin/env python3
import sys
import urllib.request
from bs4 import BeautifulSoup

def getPDFLinks():
    try:
        inputted_url = sys.argv[1]                                  #Get the input from the command line.
    except IndexError:                                              #Catch error from no input.
        print("There was no input")
        sys.exit()                                                  #If there was no input, exit the program.

    inputted_url = ParseAddress(inputted_url)                       #Ensure that the URL has an http tag.

    try:
        html = GetHTML(inputted_url)                                #Try to get the html code from the url.
    except BadLinkError:
        print("No top level domain like '.com' is provided, or there is no server that will claim the domain such as 'a.com'")
        sys.exit()                                                  #If the link is bad, exit the program.
        
    links = GetLinks(html)                                          #Get the links from the page using BeautifulSoup.
    pdfs = []                                                       #A list of the links that lead to PDF files.
    counter = 0                                                     #A counter of the number of links checked for status info.

    for link in links:                                              #For every link on the page,
        percent_complete = int((counter/len(links))*100)            #(below) output a line telling the user how close to complete the program is.
        print("Checked " + str(percent_complete) + '% of links [' + ("•"*int(percent_complete/10)) + (" "*(10-int(percent_complete/10))) + "]")
        link_url = ParseAddress(link, inputted_url)                 #Make sure the link is formatted correctly, including this page's url at the
        try:                                                        #   front of the link if necessary.
            content_type = GetURLHeader(link_url).get('Content-Type')#Get the content-type from the header, which is how the major browsers determine
        except BadLinkError:                                        #   if the link leads to a PDF file or some other type of content.
            print(link_url + " is a bad link")                      #Handles links that don't respond on the webpage.
            sys.stdout.write("\033[F")                              #Goes up one line to ensure that the completion percentage is not written over by the error output.
            sys.stdout.write("\033[F")                                  #These lines make the link status info erease itself and redisplay new info.
            sys.stdout.write("\033[K")
            continue  
        if content_type == "application/pdf":                       #If the page is a pdf
            pdfs.append(link_url)                                   #Add the link to the list of pdf links.
        counter += 1
        sys.stdout.write("\033[F")                                  #These lines make the link status info erease itself and redisplay new info.
        sys.stdout.write("\033[K")
    sys.stdout.write("\033[F")                                      #These lines delete all status lines to make way for the output.
    sys.stdout.write("\033[J")


    if len(pdfs) != 0:                                              #Prints the output.
        print("Links that lead to PDF files:")
        for pdf in pdfs:
            print(pdf)
    else:
        print("None of the links end in PDF files")


                                                                    #Error for reporting a bad link.
class BadLinkError(Exception):
    pass

#Makes sure the address has an http or https
def ParseAddress(address, initialAddress = ""):
    if (address[0:8] != "https://" and address[0:7] != "http://"):  #Checks if link has http or https
        if initialAddress != "":                                    #Checks initial address is empty
            address = initialAddress + address                      #Adds the address if there is no http and a full address was provided
        else:
            address = "https://" + address                          #Adds the http if not full address was provided
    return address

#Gets the html code for the webpage. If the link is not claimed by any server or lacks a top level domain, it will raise an error.
def GetHTML(url):
    try:
        temp_html_reader = urllib.request.urlopen(url)              #Opens the page
    except urllib.error.URLError:
        raise BadLinkError
        
    print("Got code: "+ str(temp_html_reader.getcode()))            #Useful readout of the code provided by the page. Not shown in final output
    return temp_html_reader.read()                                  #Returns the html code

#Gets the header for the webpage. If the link is not claimed by any server or lacks a top level domain, it will raise an error.
def GetURLHeader(url):
    try:
        temp_html_reader = urllib.request.urlopen(url)              #Opens the page
    except urllib.error.URLError:
        raise BadLinkError
    
    return temp_html_reader.info()                                  #Returns the header.

#Gets all of the links from the webpage given the html code.
def GetLinks(html):
    beautiful_soup_parser = BeautifulSoup(html, 'html.parser')      #Instantiates BeautifulSoup
    a_components = beautiful_soup_parser.find_all('a')              #Gets all of the <a> blocks from the html
    links = []                                                      #List of all of the links in the page.
    for i in range(len(a_components)):                              #For every link
        start_bound = str(a_components[i]).find('href=\"')+6        #Get rid of html code not in link
        end_bound = str(a_components[i])[start_bound:].find('\"') + start_bound#Get rid of end html code not in link
        links.append(str(a_components[i])[start_bound : end_bound]) #Append link to list of links
    return links


getPDFLinks()
