#!/usr/bin/python

"""
For Question One, some users that are closest in name and occupation to me.


"""

class User:
    user_id = None
    age = None
    gender = None
    occupation = ""
    zip_code = None
    ageGenderOccupationValue = None
    inputString = ""

    def __init__(self, UID, Age, Gender, Occupation, Zip_Code, inputString):
        self.user_id = int(UID)
        self.age = int(Age)
        self.gender = Gender
        self.occupation = Occupation
        self.zip_code = Zip_Code
        self.inputString = inputString


def main():
    f = open("ml-100k/u.user", 'r')
    users = []
    ageRange = [300, 0]
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

    me = User(1000, 22, 1, "programmer", "04473", "")
    me.ageGenderOccupationValue = calculateAGOValue(me, ageRange)
    closestUser = [None, None, None]
    cUVal = [20, 20, 20]

    for user in users:
        for i in range(len(closestUser)):
            if abs(user.ageGenderOccupationValue - me.ageGenderOccupationValue) < cUVal[i] and user not in closestUser:
                cUVal[i] = abs(user.ageGenderOccupationValue - me.ageGenderOccupationValue)
                closestUser[i] = user

    for user in closestUser:
        print(user.inputString)
        reviewData = getReviewsByUser(user.user_id)

        for review in reviewData:
            print(str(review[1]) + "    " + str(getMovieTitle(int(review[0]))))

def getMovieTitle(movieID):
    f = open("ml-100k/u.item")

    for line in f.readlines():
        d = line.split("|")
        if int(d[0]) == movieID:
            return d[1]
    f.close()


def getReviewsByUser(UID):
    f = open("ml-100k/u.data")
    output = []
    for line in f.readlines():
        d = line.split("\t")
        if int(d[0]) == UID:
            output.append([int(d[1]), int(d[2])])
    f.close()
    return output


def calculateAGOValue(user, ageRange):
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
        return 1
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
