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
