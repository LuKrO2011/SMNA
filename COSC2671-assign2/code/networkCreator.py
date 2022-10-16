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


def save(filename, data):
    with open(filename, 'w') as json_file:
        for user in data:
            json.dump(user.data, json_file)
            json_file.write('\n')

    print("Users successfully stored to: ", output_filename)


def load(filename):
    datas = []
    with open(filename, 'r') as f:
        for line in f:
            data = json.loads(line)
            datas.append(data)
    return datas


def add_node(graph, node, **attr):
    if node not in seen_nodes:
        graph.add_node(node, **attr)
        seen_nodes.add(node)


def add_edge(graph, edge_from, edge_to):
    if (edge_from, edge_to) not in seen_edges:
        graph.add_edge(edge_from, edge_to)
        seen_edges.add((edge_from, edge_to))


# Username of the ego
input_filename = "most_common_users_filtered.json"

# Where to store the graph to
# output_filename = 'connections.graphml'
output_dir = "../graph_data"
output_filename = 'following'

# maximum number of results
max_results = 10

max_results_per_request = 1000

# All user fields
all_user_fields = ["id", "name", "username", "created_at", "description", "location", "entities", "pinned_tweet_id",
                   "profile_image_url", "protected", "public_metrics", "url", "verified", "withheld"]

# Fields of interest
user_fields_of_interest = ["id", "name", "public_metrics"]

# Load the users
egos = load(input_filename)

# Create graph
graph = nx.DiGraph()

seen_nodes = set()
seen_edges = set()

for ego in egos:

    # ego attributes
    ego_id = ego.get("id")
    ego_username = ego.get("username")
    ego_name = ego.get("name")

    # Add ego
    add_node(graph, ego_username)

    # Get followers of ego
    followers = []

    twitterResponse = client.get_users_followers(id=ego_id, max_results=max_results_per_request, user_fields=all_user_fields)
    if twitterResponse.data is not None:
        for user in twitterResponse.data:
            followers.append(user)

    while len(followers) < max_results:
        try:
            twitterResponse = client.get_users_followers(id=ego_id, max_results=max_results_per_request, user_fields=all_user_fields)
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
        add_node(graph, follower_name, followers_count=followers_count, following_count=following_count,
                 tweet_count=tweet_count, color_id=calculate_importance(followers_count))
        add_edge(graph, ego_username, follower_name)

    # Get users that the ego follows
    following = []
    twitterResponse = client.get_users_following(id=ego_id, max_results=max_results_per_request, user_fields=all_user_fields)
    if twitterResponse.data is not None:
        for user in twitterResponse.data:
            following.append(user)

    print("Followers downloaded: " + str(len(following)))

    filename = output_dir + "/" + output_filename + "_" + ego_username + ".json"
    save(filename, following)
    print("Followers stored: " + str(filename))

    while len(following) < max_results:
        try:
            twitterResponse = client.get_users_following(id=ego_id, max_results=max_results_per_request, user_fields=all_user_fields)
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
        add_node(graph, following_name, followers_count=followers_count, following_count=following_count,
                 tweet_count=tweet_count, color_id=calculate_importance(followers_count))
        add_edge(graph, following_name, ego_username)

# Store the graph
with open(output_filename, 'wb') as fOut:
    nx.write_graphml(graph, fOut)

print("Done!")



#%%
