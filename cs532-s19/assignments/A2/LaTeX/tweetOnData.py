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
