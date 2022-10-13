import json

from workshop03Code import twitterClient
import tweepy
import math
import networkx as nx

client = twitterClient.twitterClient()

# Assigns a logarithmic value depending on the follower count
def calculate_importance(follower_count):
    if follower_count <= 0:
        follower_count = 1
    return math.ceil(math.log10(follower_count))


def load(filename):
    datas = []
    with open(filename, 'r') as f:
        for line in f:
            data = json.loads(line)
            datas.append(data)
    return datas


# Username of the ego
input_filename = "most_common_users_filtered.json"

# Where to store the graph to
output_filename = 'connections.graphml'

# maximum number of results
maxResults = 100

# All user fields
all_user_fields = ["id", "name", "username", "created_at", "description", "location", "entities", "pinned_tweet_id",
                   "profile_image_url", "protected", "public_metrics", "url", "verified", "withheld"]

# Fields of interest
user_fields_of_interest = ["id", "name", "public_metrics"]

# Load the users
egos = load(input_filename)

# Create graph
ego_graph = nx.DiGraph()

for ego in egos:

    # ego attributes
    ego_id = ego.get("id")
    ego_username = ego.get("username")
    ego_name = ego.get("name")

    # Add ego
    ego_graph.add_node(ego_username)

    # Get followers of ego
    followers = []
    twitterResponse = client.get_users_followers(id=ego_id, max_results=100, user_fields=all_user_fields)
    if twitterResponse.data is not None:
        for user in twitterResponse.data:
            followers.append(user)

    while len(followers) < maxResults:
        try:
            twitterResponse = client.get_users_followers(id=ego_id, max_results=100, user_fields=all_user_fields)
        except Exception as e:
            print(e)

        if twitterResponse.data is not None:
            for user in twitterResponse.data:
                followers.append(user)

    print("Followers downloaded: " + str(len(followers)))

    # Remove not interesting fields
    for follower in followers:
        for key in list(follower.keys()):
            if key not in user_fields_of_interest:
                delattr(follower, key)

    # Construct followers graph
    for user in followers:
        follower_name = user.username
        followers_count = user.public_metrics.get('followers_count')
        following_count = user.public_metrics.get('following_count')
        tweet_count = user.public_metrics.get('tweet_count')
        ego_graph.add_node(follower_name, followers_count=followers_count, following_count=following_count,
                           tweet_count=tweet_count, color_id=calculate_importance(followers_count))
        ego_graph.add_edge(ego_username, follower_name)

    # Get users that the ego follows
    following = []
    twitterResponse = client.get_users_following(id=ego_id, max_results=100, user_fields=all_user_fields)
    if twitterResponse.data is not None:
        for user in twitterResponse.data:
            following.append(user)

    while len(following) < maxResults:
        try:
            twitterResponse = client.get_users_following(id=ego_id, max_results=100, user_fields=all_user_fields)
        except Exception as e:
            print(e)

        if twitterResponse.data is not None:
            for user in twitterResponse.data:
                following.append(user)

    print("Followers downloaded: " + str(len(following)))

    # Construct following graph
    for user in following:
        following_name = user.username
        followers_count = user.public_metrics.get('followers_count')
        following_count = user.public_metrics.get('following_count')
        tweet_count = user.public_metrics.get('tweet_count')
        ego_graph.add_node(following_name, followers_count=followers_count, following_count=following_count,
                           tweet_count=tweet_count, color_id=calculate_importance(followers_count))
        ego_graph.add_edge(following_name, ego_username)

# Store the graph
with open(output_filename, 'wb') as fOut:
    nx.write_graphml(ego_graph, fOut)

print("Done!")


#%%
