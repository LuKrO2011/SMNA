import tweepy

def twitterClient():
    """
        Setup Twitter API client.

        @returns: tweepy.API object
    """
    bearerToken = "ENTER TOKEN HERE"

    client = tweepy.Client(bearerToken)

    return client