#!/usr/bin/python
import recommendations as r
import os
import multiprocessing as mp

sub_id = 4                                              # The ID number of the user found to be similar to me.
favorite_movie = "Blues Brothers, The (1980)"           # My favorite move from the data set.
least_favorite_movie = "Citizen Kane (1941)"            # My least favorite movie from the data set.
# I really don't like Citizen Kane


def main():
    prefs = r.loadMovieLens(os.getcwd() + "/ml-100k")   # Calculates the preferences using recommendations.py
    movie_recommendations = r.getRecommendations(prefs, str(sub_id))  # Calculates all recommendations for sub user.

    print("\nThe most recommended movies for " + get_user(sub_id) + " (which is the substitute) are:")
    for i in range(5):                                  # This section prints out the recommendations for sub user.
        u = movie_recommendations[i][1]
        print(u)
    print("\nThe least recommended movies for the substitute are: ")
    for i in range(5):
        u = movie_recommendations[len(movie_recommendations) - (i + 1)][1]
        print(u)

    similiar_item_data = r.calculateSimilarItems(prefs)  # Calculate all similar movie data.
    print("\nFive similar movies to my favorite movie " + favorite_movie + " are:")
    fav_mov_sim = similiar_item_data[favorite_movie][0:5]  # For real me, some recommended movies for my preferences.
    for mov in fav_mov_sim:
        print(mov[1] + "    "+ str(mov[0]))

    print("\nFive similar movies to my least favorite movie " + least_favorite_movie + " are:")
    lea_fav_mov_sim = similiar_item_data[least_favorite_movie][0:5]
    for mov in lea_fav_mov_sim:
        print(mov[1] + "    "+ str(mov[0]))


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


def get_similarity_data(prefs, other_id):   # This function is part of the multi-threading process for the above.
    return [other_id, r.sim_distance(prefs, str(sub_id), str(other_id))]


def get_user(user_id):
    """
    Returns the printed data about the user from u.user.

    :param user_id:
    The user ID from u.user as an integer.

    :return:
    The line containing the user's data from u.user.
    """
    f = open("ml-100k/u.user", 'r')
    for line in f.readlines():
        u = line.split("|")
        if int(u[0]) == user_id:
            return line.split("\n")[0]


get_most_and_least_similar_users()
print("\n"*1)
main()
