#!/usr/bin/python

"""
For Question One, some users that are closest in name and occupation to me.
"""


class User:
    """
    This class holds user data for organized, easy access.
    """
    user_id = None
    age = None
    gender = None
    occupation = ""
    zip_code = None
    ageGenderOccupationValue = None
    inputString = ""
    reviews = []

    def __init__(self, uid, age, gender, occupation, zip_code, input_string):
        self.user_id = int(uid)
        self.age = int(age)
        self.gender = gender
        self.occupation = occupation
        self.zip_code = zip_code
        self.inputString = input_string


ageRange = [300, 0]


def get_user_data():
    """
    This function collects user data from a file, and puts into the format of the User class.
    It also does some formatting, and calculates the AGO value for comparison.
    :return:
    A list of User class objects with some data populated.
    """
    f = open("ml-100k/u.user", 'r')
    users = []
    for line in f.readlines():
        u = line.split("|")
        u[0] = int(u[0])
        u[1] = int(u[1])

        gender = 0
        if u[2] == "M":
            gender = 1

        if u[1] > ageRange[1]:
            ageRange[1] = u[1]
        elif u[1] < ageRange[0]:
            ageRange[0] = u[1]

        user = User(u[0], u[1], gender, u[3], u[4], line)
        users.append(user)

    for user in users:
        user.ageGenderOccupationValue = calculateAGOValue(user, ageRange)
    return users


def main():
    users = get_user_data()

    me = User(1000, 22, 1, "programmer", "04473", "")               # Create a user class for me to compare.
    me.ageGenderOccupationValue = calculateAGOValue(me, ageRange)
    closestUser = [None, None, None]
    cUVal = [20, 20, 20]

    for user in users:                                              # Compares every user to me, and picks the top three
        for i in range(len(closestUser)):
            if abs(user.ageGenderOccupationValue - me.ageGenderOccupationValue) < cUVal[i] and user not in closestUser:
                cUVal[i] = abs(user.ageGenderOccupationValue - me.ageGenderOccupationValue)
                user.reviews = getReviewsByUser(user.user_id)
                closestUser[i] = user

    for user in closestUser:                                        # For each of the close users, this section finds
        print(user.inputString.split("\n")[0])                      # (cont) the highest and lowest rated movies the
        user.reviews = sorted(user.reviews, key=lambda x: x[1])     # (cont) user has seen.

        topThree = []
        bottomThree = []
        for i in range(len(user.reviews)):
            if i < 3:
                bottomThree.append(user.reviews[i])
            if len(user.reviews) - i < 4:
                topThree.append(user.reviews[i])

        print("User's top three movies:")                           # This section prints the top three and bottom three
        for movie in topThree:                                      # (cont) reviewed movies that the user has seen.
            print(getMovieTitle(movie[0]))

        print("\nUser's bottom three movies:")
        for movie in bottomThree:
            print(getMovieTitle(movie[0]))
        print("\n"*2)


def getMovieTitle(movieID):
    """
    This function gets the movie title from the movie id

    :param movieID:
    The movie ID as found in u.item from the data set as an int

    :return:
    The movie title as a string
    """
    f = open("ml-100k/u.item")

    for line in f.readlines():
        d = line.split("|")
        if int(d[0]) == movieID:
            return d[1]
    f.close()


def getReviewsByUser(UID):
    """
    Gets all the reviews that a user has done.
    :param UID:
    The ID of the user as found in u.data, as an integer

    :return:
    A list containing two items:
    (1) The ID number of the movie.
    (2) The rating that the user left for the movie.
    """
    f = open("ml-100k/u.data")
    output = []
    for line in f.readlines():
        d = line.split("\t")
        if int(d[0]) == UID:
            output.append([int(d[1]), int(d[2])])
    f.close()
    return output


def calculateAGOValue(user, ageRange):
    """
    Calculates an aggregate score from user data on age, occupation, and gender. Assumed to be a bad system, needs
    to be fixed.

    :param user:
    A User class object for which the score will be calculated.

    :param ageRange:
    The range of ages found in the data set (to calculate with the smallest numbers possible)

    :return:
    An integer that represents the aggregate score.
    """
    ageNorm = 0.5
    occupationNorm = 0.5
    if user.age != None:
        ageNorm = (float(user.age) - float(ageRange[0]))/float(ageRange[1])

    if user.occupation != None:
        occ = occupation_to_val(user.occupation)
        if occ != None:
            occupationNorm = (float(occupation_to_val(user.occupation)) - 1.0)/40.0

    return (ageNorm + occupationNorm + float(user.gender)) / 3.0


def occupation_to_val(input):               # Arbitrarily sets value of occupation to a number. I've made this up.
    if input == "administrator":            # None is a neutral value. It's something that may be too variable to be
        return 21                           # (continued)  classified.
    elif input == "artist":
        return 1                            # This is largely based on personal bias on how different jobs are similar.
    elif input == "doctor":
        return 26
    elif input == "educator":
        return 13
    elif input == "engineer":
        return 22
    elif input == "entertainment":
        return 2
    elif input == "executive":
        return 20
    elif input == "healthcare":
        return 25
    elif input == "homemaker":
        return 40
    elif input == "lawyer":
        return 19
    elif input == "librarian":
        return 14
    elif input == "marketing":
        return 17
    elif input == "none":
        return None
    elif input == "other":
        return None
    elif input == "programmer":
        return 23
    elif input == "retired":
        return None
    elif input == "salesman":
        return 18
    elif input == "scientist":
        return 24
    elif input == "student":
        return 8
    elif input == "technician":
        return 22
    else:
        return 4


main()
