#
# COSC2671 Social Media and Network Analytics
# @author Jeffrey Chan, 2018
#

import sys
import praw


def redditClient():
    """
        Setup Reedit API authentication.
        Replace username, secrets and passwords with your own.

        @returns: praw Reedit object
    """

    try:
        #
        # TODO: you specify with your details
        #
        clientId = "cD79Uwu99ztptrlGwjWTmg"
        clientSecret = "18_XOUDNWrxDCYJsvo8_BI1KYy1yUg"
        password = "3Bptek^d%W4!C4T7"
        userName = "LuKrO99"
        userAgents = 'client for SNAM2018'

        redditClient = praw.Reddit(client_id = clientId,
                                   client_secret = clientSecret,
                                   password = password,
                                   username = userName,
                                   user_agent = userAgents)

    except KeyError:
        sys.stderr.write("Key or secret token are invalid.\n")
        sys.exit(1)


    return redditClient
