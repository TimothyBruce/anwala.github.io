finalResults = []
    for query in getNewWords():
        print(query)
        queryResults = []
        query = query + " .blogspot.com"
        time.sleep(60)
        for j in search(query, num=10, stop=20, pause=2):
            if ".blogspot.com" in j:
                queryResults.append(j)
                f =open("blogs.txt", "a")
                f.write(j)
                f.write('\n')
                f.close()
        finalResults.append(queryResults)
        print(queryResults[0])
    print(finalResults)
