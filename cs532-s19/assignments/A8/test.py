import docclass
from subprocess import check_output
import os
import math

cl = docclass.naivebayes(docclass.getwords)


def main():
    # remove previous db file
    f = open('tabruce.db', 'w')
    f.close()
    check_output(['rm', 'tabruce.db'])

    cl.setdb('tabruce.db')

    train_directories([os.curdir + "/Testing/spam/", os.curdir + "/Testing/notSpam/"], ["spam", "not spam"])

    check_directories([os.curdir + "/Training/notSpam/", os.curdir + "/Training/spam/"], ["not spam", "spam"])


def train_directories(directories, order_of_correctness):
    emails = []
    key = []
    for i in range(len(directories)):
        counter = 0
        for email in get_emails(directories[i]):
            emails.append(email)
            counter += 1
        for r in range(counter):
            key.append(order_of_correctness[i])
    train_set(emails, key)


def check_directories(directories, order_of_correctness):
    for i in range(len(directories)):
        emails = get_emails(directories[i])
        check_set(emails, order_of_correctness[i])


def get_emails(directory):
    a = [directory + x for x in os.listdir(directory)]
    emails = []
    for email in a:
        f = open(email)
        string = ""
        for line in f.readlines():
            string += line
        emails.append(string)
        f.close()
    return emails


def train_set(training_data, value):
    print(value)
    length = math.floor(len(training_data)/2)
    for i in range(length):
        cl.train(training_data[i*2], value[i*2])
        cl.train(training_data[(length*2)-(i*2)-1], value[(length*2)-(i*2)-1])
        print(str(i*2) + "  " + value[i*2])
        print(str((length*2)-(i * 2) - 1) + "   " + value[(length*2)-(i*2)-1])


def check_set(training_data, value):
    for email in training_data:
        print(cl.classify(email) + " " + value)



main()
