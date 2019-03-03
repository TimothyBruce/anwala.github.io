tfidf_values = [0.356, 0.288, 0.214, 0.214, 0.158, 0.151, 0.15, 0.124, 0.123, 0.114]
page_rank = [9.2, 8.5, 8.7, 8.9, 8.5, 8.5, 8.5, 8.5, 8.5, 8.6]
alexa = [1721, 814, 934, 1462, 814, 162, 814, 4914, 4914, 597]  # https://www.rank2traffic.com/
print("FOR TFIDF AND PAGERANK")
print(kendallTauCalculation(tfidf_values, page_rank))

print("FOR TFIDF AND alexa")
print(kendallTauCalculation(tfidf_values, alexa))

print("FOR alexa AND PAGERANK")
print(kendallTauCalculation(alexa, page_rank))
