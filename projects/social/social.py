import random
from collections import deque

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
            return False
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
            return False
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            return True

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name) # sets the User
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        self.len = 0
        # !!!! IMPLEMENT ME

        # Add users

        if num_users <= avg_friendships:
            return None

        for x in range(num_users):
            self.add_user("User" + str(x))

        total_cons = (num_users*avg_friendships)
        # Create friendships

        while total_cons > 0:
            if self.add_friendship(random.randint(1, num_users),
                                   random.randint(1, num_users)):
                total_cons -= 2

        self.len = 0
        for x in (self.users):
            self.len += len(self.friendships[x])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}
        Q = deque()
        Q.appendleft([user_id])

        while len(Q) > 0:

            path = Q.pop()
            x = path[-1]

            if x not in visited:
                # avoids pointing to it self
                if path[0] != x:
                    visited[x] = path
                for y in self.friendships[x]:
                    Q.appendleft([y] + path)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
