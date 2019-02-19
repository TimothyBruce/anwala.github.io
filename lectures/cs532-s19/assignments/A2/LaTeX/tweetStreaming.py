#A lot of this code comes from https://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/
def streamTwitter(duration, keyword):
    f = open('tweets.json', 'r')  # Get old data
    old_data = json.load(f)['tweets']
    f.close()
    # (below)Stream Twitter for Duration.
    twitterStream = Stream(auth, listener(t.timedelta(minutes=int(duration)), old_data))
    twitterStream.filter(track=[keyword])

    # (below)Return all of the Tweets.
    return json.load(open('tweets.json', 'r'))['tweets']


class listener(StreamListener):  # The SteamListener streams the tweets.
    def __init__(self, duration=1, existing_data=[]):
        self.endTime = t.datetime.now() + duration  # This is the timer.
        self.counter = 0
        self.tweets = {}  # This is where all of the tweets are stored.
        self.tweets['tweets'] = existing_data  # These are the historical tweets being added.

    def on_data(self, data):
        json_new_data = json.loads(data)  # Format the data as JSON
        json_data = {}  # Place to store all of the tweets.
        json_data['text'] = json_new_data['text']  # Store the tweet text.
        json_data['links'] = json_new_data['entities']['urls']  # Store the URIs.
        json_data['time'] = json_new_data['created_at']  # Store the creation date.
        self.tweets['tweets'].append(json_data)  # Add the tweet to the list of tweets.
        f = open('tweets.json', 'w')  # Save the tweets for future use.
        json.dump(self.tweets, f)
        f.close()

        self.counter += 1
        if self.endTime > t.datetime.now():  # If the timer has not expired,
            return True  # continue.
        else:  # If the timer has expired,
            return False  # stop.

    def on_error(self, status):
        print(status)

