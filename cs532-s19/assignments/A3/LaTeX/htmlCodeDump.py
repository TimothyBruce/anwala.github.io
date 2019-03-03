for key in html_dump.keys():                        # For everything in html dump
        raw_html = html_dump[key]                       # The raw html.
        soup = BeautifulSoup(raw_html, 'html.parser')   # Create html parser.
        text = soup.get_text()                          # The parsed html.

        linkdict = dict()                               # This is where the clean formatted data goes.
        linkdict['raw_html'] = str(raw_html)            # Put in the raw html.
        linkdict['clean_html'] = str(text)              # Put in the clean text.
        linkdict['link'] = str(key)                     # Put in the link for output.

        to_save_link_text[hash(key)] = linkdict