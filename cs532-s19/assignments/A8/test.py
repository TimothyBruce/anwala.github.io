import docclass
from subprocess import check_output
import os

cl = docclass.naivebayes(docclass.getwords)


def main():
    # remove previous db file
    f = open('tabruce.db', 'w')
    f.close()
    check_output(['rm', 'tabruce.db'])

    cl.setdb('tabruce.db')

    train_directories([os.curdir + "/Training/spam/", os.curdir + "/Training/notSpam/"], ["spam", "not spam"])

    check_directories([os.curdir + "/Testing/notSpam/", os.curdir + "/Testing/spam/"], ["not spam", "spam"])


def train_directories(directories, order_of_correctness):
    for i in range(len(directories)):
        emails = get_emails(directories[i])
        train_set(emails, order_of_correctness[i])


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
    for email in training_data:
        cl.train(email, value)


def check_set(training_data, value):
    for email in training_data:
        print(cl.classify(email) + " " + value)



main()