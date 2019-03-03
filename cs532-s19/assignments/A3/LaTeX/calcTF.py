instances = clean_html.count(searchTerm)        # Get count of of instances of the search term in the text.
words = clean_html.split(' ')
word_count = len(words)                         # Get word count of clean text.
tf = instances/word_count                       # Calculate tf value.
tfidf = (instances/word_count) * IDF            # Calculate tf-idf value.
