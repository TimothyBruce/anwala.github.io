for user in followers:          # (above) For each user, get followers
    ff = []                     # FF stands for "follower's followers"
    for page in tweepy.Cursor(api.followers_ids, user_id=user).pages():
        ff.extend(page)         # (above) actually gets the followers.
        if len(page) > 5000:    # If it is a long page,
            time.sleep(60)      # Treat it as a new call.
    data.append(len(ff))
    print(data[-1])
    time.sleep(60)              # Next user.
