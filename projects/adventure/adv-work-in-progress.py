#COPY PASTED WORK OVER TO ADV.PY FROM ADV-WORK-IN-PROGRESS.PY

import random
from ast import literal_eval
from room import Room
from player import Player
from world import World
world = World()

mapFile = "maps/main_maze.txt"

graph = literal_eval(open(mapFile, "r").read())
world.load_graph(graph)

world.print_rooms()

player = Player(world.starting_room)

traversalPath = []
#declaring opposite directions
dirPairs = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

def calc_path(starting_room, defaultVisited=set()):
    #init
    visited = set()
    path = []
    for r in defaultVisited:
        visited.add(r)
    #function to add room to path
    # ret = return, reserved keyword by python
    def add(room, ret=None):
        allExits = room.get_exits()
        #adds room
        visited.add(room)
        # checks exits
        for d in allExits:
            # checks wether than room was visited before, if not add to path
            if room.get_room_in_direction(d) not in visited:
                path.append(d)
                add(room.get_room_in_direction(d), dirPairs[d])
        if ret:
            path.append(ret)
    add(starting_room)
    return path

def pathing(starting_room, visited=set()):
    path = []
    def add(room, ret=None):
        #init
        lenPath = {}
        traverse = []
        #same as above add room, get exits
        visited.add(room)
        allExits = room.get_exits()
        for d in allExits:
            lenPath[d] = len(calc_path(room.get_room_in_direction(d), visited))
        #sorted by path length
        for d, i in sorted(lenPath.items()): 
            traverse.append(d)
        for d in traverse:
            #if not visited
            if room.get_room_in_direction(d) not in visited:
                # add, because not visited yet
                path.append(d)
                # recursion
                add(room.get_room_in_direction(d), dirPairs[d])
        #break if all visited
        if len(world.rooms) == len(visited): 
            return "Done"
        #continue if not
        elif ret:
            path.append(ret)
    add(starting_room)
    return path

traversalPath = pathing(world.starting_room)



#################################################################
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversalPath:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(graph):
    print(f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited")
    #wanted to output graph would need to change output function for that
    f = open("output.txt", "w")
    print(f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited", file=f)

else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(graph ) - len(visited_rooms)} unvisited rooms")