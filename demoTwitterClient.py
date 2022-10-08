#
# COSC2671 Social Media and Network Analytics
# @author Jeffrey Chan, RMIT University, 2022
#

import tweepy


def twitterClient():
    """
        Setup Twitter API client.

        @returns: tweepy.API object
    """
    bearerToken = "ENTER TOKEN HERE"

    client = tweepy.Client(bearerToken)

    return client