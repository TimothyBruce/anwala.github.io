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
