from room import Room
from player import Player
from world import World
from worldmap import Map
import requests
import hashlib
import random
import time
import json
import sys
from cpu import *
from ast import literal_eval
from util import Stack, Queue

from graph import Graph

# Load world
world = World()
world_map = Map()
graph = Graph()

def format_map(unformatted):
    formatted = {}
    for i in unformatted:
        # print(unformatted[i])
        if 'n' in unformatted[i] and 's' not in unformatted[i] and 'e' not in unformatted[i] and 'w' not in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'n': unformatted[i]['n']}]
        if 'n' not in unformatted[i] and 's' in unformatted[i] and 'e' not in unformatted[i] and 'w' not in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'s': unformatted[i]['s']}]
        if 'n' not in unformatted[i] and 's' not in unformatted[i] and 'e' in unformatted[i] and 'w' not in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'e': unformatted[i]['e']}]
        if 'n' not in unformatted[i] and 's' not in unformatted[i] and 'e' not in unformatted[i] and 'w' in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'w': unformatted[i]['w']}]
        if 'n' in unformatted[i] and 's' in unformatted[i] and 'e' not in unformatted[i] and 'w' not in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'n': unformatted[i]['n'], 's': unformatted[i]['s']}]
        if 'n' in unformatted[i] and 's' not in unformatted[i] and 'e' in unformatted[i] and 'w' not in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'n': unformatted[i]['n'], 'e': unformatted[i]['e']}]
        if 'n' in unformatted[i] and 's' not in unformatted[i] and 'e' not in unformatted[i] and 'w' in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'n': unformatted[i]['n'], 'w': unformatted[i]['w']}]
        if 'n' not in unformatted[i] and 's' in unformatted[i] and 'e' in unformatted[i] and 'w' not in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'s': unformatted[i]['s'], 'e': unformatted[i]['e']}]
        if 'n' not in unformatted[i] and 's' in unformatted[i] and 'e' not in unformatted[i] and 'w' in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'s': unformatted[i]['s'], 'w': unformatted[i]['w']}]
        if 'n' not in unformatted[i] and 's' not in unformatted[i] and 'e' in unformatted[i] and 'w' in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'e': unformatted[i]['e'], 'w': unformatted[i]['w']}]
        if 'n' in unformatted[i] and 's' in unformatted[i] and 'e' in unformatted[i] and 'w' not in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'n': unformatted[i]['n'], 's': unformatted[i]['s'], 'e': unformatted[i]['e']}]
        if 'n' in unformatted[i] and 's' in unformatted[i] and 'e' not in unformatted[i] and 'w' in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'n': unformatted[i]['n'], 's': unformatted[i]['s'], 'w': unformatted[i]['w']}]
        if 'n' in unformatted[i] and 's' not in unformatted[i] and 'e' in unformatted[i] and 'w' in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'n': unformatted[i]['n'], 'e': unformatted[i]['e'], 'w': unformatted[i]['w']}]
        if 'n' not in unformatted[i] and 's' in unformatted[i] and 'e' in unformatted[i] and 'w' in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'s': unformatted[i]['s'], 'e': unformatted[i]['e'], 'w': unformatted[i]['w']}] 
        if 'n' in unformatted[i] and 's' in unformatted[i] and 'e' in unformatted[i] and 'w' in unformatted[i]:
            formatted[int(i)] = [literal_eval(unformatted[i]['coordinates']), {'n': unformatted[i]['n'], 's': unformatted[i]['s'], 'e': unformatted[i]['e'], 'w': unformatted[i]['w']}]
    return formatted
# print(world_map.unformatted)
# print(format_map(world_map.unformatted))

# Loads the map into a dictionary
# literal_eval(open(map_file, "r").read())
room_graph = format_map(world_map.unformatted)
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()
player = Player(world.starting_room)

print(f'Staring Room:  {player.current_room.id}')
# print(f'Staring Room2:  {world_map.unformatted[str(player.current_room.id)][direction]}')



def init_player():
    headers = {'Authorization': 'Token 580b9c2887edeae63aab95321ff746911427cc27'}
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
    r = requests.get(url=url, headers=headers)
    data = r.json()
    return data


def move_player(direction, next_room_id):
    headers = {'Authorization': 'Token 580b9c2887edeae63aab95321ff746911427cc27'}
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
    post_data = {"direction":direction, "next_room_id": str(next_room_id)}
    r = requests.post(url=url, json=post_data, headers=headers)
    data = r.json()
    print(data)
    return data

def pickup_item(item):
    headers = {'Authorization': 'Token 580b9c2887edeae63aab95321ff746911427cc27'}
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/take/'
    post_data = {"name": item}
    r = requests.post(url=url, json=post_data, headers=headers)
    data = r.json()
    return data

def check_inventory():
    headers = {'Authorization': 'Token 580b9c2887edeae63aab95321ff746911427cc27'}
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/status/'
    post_data = {}
    r = requests.post(url=url, json=post_data, headers=headers)
    data = r.json()
    return data

def sell_treasure(item):
    headers = {'Authorization': 'Token 580b9c2887edeae63aab95321ff746911427cc27'}
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/'
    post_data = {"name": item, "confirm": 'yes'}
    r = requests.post(url=url, json=post_data, headers=headers)
    data = r.json()
    print(f'data:  {data}')
    return data

def change_name():
    headers = {'Authorization': 'Token 580b9c2887edeae63aab95321ff746911427cc27'}
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/'
    post_data = {"name": "[Ryan the Quail]", 'confirm':'aye'}
    r = requests.post(url=url, json=post_data, headers=headers)
    print(r)
    data = r.json()
    print(data)
    return data    

def examine_well():
    headers = {'Authorization': 'Token 580b9c2887edeae63aab95321ff746911427cc27'}
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/'
    post_data = {"name": "well"}
    r = requests.post(url=url, json=post_data, headers=headers)
    print(r)
    data = r.json()
    print(data)
    return data

def make_proof():
    headers = {'Authorization': 'Token 580b9c2887edeae63aab95321ff746911427cc27'}
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/'
    r = requests.get(url=url, headers=headers)
    print(r)
    data = r.json()
    hash_value = ''
    while hash_value[0:data['difficulty']] != '0'*data['difficulty']:
        new_proof = random.randrange(0,999999999999)
        old_proof = data['proof']
        proof_string = f'{old_proof}{new_proof}'
        current = proof_string.encode()
        hash_value = hashlib.sha256(current).hexdigest()

    return new_proof
    

def dfs(starting_vertex, destination_vertex):
    stack = Stack()
    stack.push([['', starting_vertex]])
    visited=set()
    while stack.size() > 0:
        current_path = stack.pop()
        current_node = current_path[-1][1]

        if current_node == destination_vertex:
            return current_path
        elif not current_node in visited:
            visited.add(current_node)
            for node in graph.get_neighbors(current_node):
                path_dup = list(current_path)
                if str(node) in room_graph[current_node][1]:
                    path_dup.append([node, room_graph[current_node][1][node]])
                    stack.push(path_dup)

def bfs(starting_vertex, destination_vertex):
    queue = Queue()
    queue.enqueue([['', starting_vertex]])
    visited = set()
    while queue.size() > 0:
        current_path = queue.dequeue()
        current_node = current_path[-1][1]
        if current_node == destination_vertex:
            # print(current_path)
            return current_path
        elif not current_node in visited:
            visited.add(current_node)
            for node in graph.get_neighbors(current_node):
                path_dup = list(current_path)
                if str(node) in room_graph[current_node][1]:
                    path_dup.append([node, room_graph[current_node][1][node]])
                    queue.enqueue(path_dup)

def create_graph():
    for i in room_graph:
        graph.add_vertex(i)
    for i in room_graph:
        if 'n' in room_graph[i]:
            graph.vertices[int(i)]['n'] = room_graph[i]['n']
        if 'e' in room_graph[i]:
            graph.vertices[int(i)]['e'] = room_graph[i]['e']
            # graph.add_edge(int(i), room_graph[i]['e'])
        if 's' in room_graph[i]:
            graph.vertices[int(i)]['s'] = room_graph[i]['s']
            # graph.add_edge(int(i), room_graph[i]['s'])
        if 'w' in room_graph[i]:
            graph.vertices[int(i)]['w'] = room_graph[i]['w']
            # graph.add_edge(int(i), room_graph[i]['w'])
create_graph()

def treasure_hunt():
    location = init_player()['room_id']
    print(f'location: {location}')
    time.sleep(1)
    inventory = check_inventory()
    time.sleep(inventory['cooldown'])
    print(f'gold  {type(inventory["gold"])}')
    print(f'encumbrance  {inventory["encumbrance"]}')
    if inventory['gold'] >= 1000:
        print(inventory['gold'])
        return
    if inventory['encumbrance'] >= 10:
        for i in dfs(location, 1):
            if i[0] != '':
                res = move_player(i[0], i[1])
                time.sleep(res['cooldown'])
        for i in inventory['inventory']:
            print(i)
            res = sell_treasure(i)
            time.sleep(res['cooldown'])
        treasure_hunt()
    dest = random.randrange(0,500)
    for i in dfs(location, dest):
        if i[0] != '':
            res = move_player(i[0], i[1])
            time.sleep(res['cooldown'])
            if len(res['items']) > 0:
                res = pickup_item(res['items'][0])
                time.sleep(res['cooldown'])
    treasure_hunt()

def go_to_pirate():
    location = init_player()['room_id']
    print(f'location: {location}')
    time.sleep(1)
    for i in bfs(location, 467):
        if i[0] != '':
            res = move_player(i[0], i[1])
            time.sleep(res['cooldown'])

def go_to_well():
    location = init_player()['room_id']
    print(f'location: {location}')
    time.sleep(1)
    for i in bfs(location, 55):
        if i[0] != '':
            res = move_player(i[0], i[1])
            time.sleep(res['cooldown'])

def decode_well():
    res = examine_well()
    f = open("well.txt", "w")
    f.write(res['description'])
    f.close()
    cpu = CPU()

    cpu.load()
    cpu.run()

def go_to_coin(room):
    location = init_player()['room_id']
    print(f'location: {location}')
    time.sleep(1)
    for i in bfs(location, room):
        if i[0] != '':
            res = move_player(i[0], i[1])
            time.sleep(res['cooldown'])

def mine_coin(new_proof):
    headers = {'Authorization': 'Token 580b9c2887edeae63aab95321ff746911427cc27'}
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/'
    post_data = {"proof":new_proof}
    r = requests.post(url=url, json=post_data, headers=headers)
    print(r)
    data = r.json()
    print(data)
    return data

def get_balance():
    headers = {'Authorization': 'Token 580b9c2887edeae63aab95321ff746911427cc27'}
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/'
    r = requests.get(url=url, headers=headers)
    print(r)
    data = r.json()
    print(data)
    return data



# dfs(location, 1)
# treasure_hunt()
# go_to_pirate()
# change_name()
# print(check_inventory())
# go_to_well()
# examine_well()
# decode_well() it said to go to room 214
# go_to_coin(214)
# valid_proof = make_proof()
# mine_coin(valid_proof)
get_balance()
