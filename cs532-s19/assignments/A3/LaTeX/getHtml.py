# Gets the html code for the webpage. If the link is not claimed by any server or
#   lacks a top level domain, it will raise an error.
def get_html(url):
    try:
        temp_html_reader = ul.urlopen(url)              # Opens the page.
    except ule.URLError:
        return None

    return temp_html_reader.read()                      # Returns the html code.