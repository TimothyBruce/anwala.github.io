tfidf_values = [0.356, 0.288, 0.214, 0.214, 0.158, 0.151, 0.15, 0.124, 0.123, 0.114]
page_rank = [9.2, 8.5, 8.7, 8.9, 8.5, 8.5, 8.5, 8.5, 8.5, 8.6]

print("FOR TFIDF AND PAGERANK")
print(kendallTauCalculation(tfidf_values, page_rank))
