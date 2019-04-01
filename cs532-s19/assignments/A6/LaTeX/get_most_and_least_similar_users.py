def get_most_and_least_similar_users():
    """
    Calculates users that are similar to the substitute user from problem one. Early on, I noticed that the program
    took a while to execute, so I multi-threaded the sim_distance function to expedite execution.

    :return:
    Prints out data on the top five most similar and least similar users to the substitute user.
    """
    pool = mp.Pool(mp.cpu_count())
    prefs = r.loadMovieLens(os.getcwd()+"/ml-100k")
    similarity_data = [pool.apply(get_similarity_data, args=(prefs, other_id+1)) for other_id in range(943)]
    pool.close()
    similarity_data = sorted(similarity_data, key=lambda x: x[1])

    print("The most similar users to " + get_user(sub_id) + " (which is the substitute) are:")
    for i in range(5):
        u = get_user(similarity_data[len(similarity_data)-(i+1)][0])
        print(u)

    print("\nThe least similar users are: ")
    for i in range(5):
        u = get_user(similarity_data[i][0]).split("\n")[0]
        print(u)
