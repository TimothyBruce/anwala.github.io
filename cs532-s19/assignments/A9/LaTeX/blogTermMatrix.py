def popularTerms(data, wordorder):
    # Gets the most popular 1000 words from the dataset (or all of the words).
    words = {}

    for wordKey in range(len(wordorder)):
        word = wordorder[wordKey]
        wordcount = 0
        for line in data:
            wordcount += int(line[wordKey])
        if word in words.keys():
            words[word] += wordcount
        else:
            words[word] = wordcount
    if len(words) > 1000:
        return sorted(words.items(), key=lambda x: -x[1])[:1000]
    else:
        return sorted(words.items(), key=lambda x: -x[1])[:len(words)-1]


def blog_term_matrix(popTerms, data, words, blogNames):
    # Creates the blog-term matrix for all of the blogs.
    website_matricies = []
    for site in blogNames:
        website_matricies.append([site, get_blog_term_matrix(popterms, data[blogNames.index(site)], words)])

    return website_matricies


def get_blog_term_matrix(popTerms, site_data, words):
    # Creates the blog term matrix for a single website.
    matrix = []
    for item in popTerms:
        word_index = words.index(item[0])
        matrix.append(site_data[word_index])

    return matrix
