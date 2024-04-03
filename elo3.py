import operator
import statbotics
import urllib
import requests
import numpy as np
import random
import json
import operator
import networkx as nx
import sympy as sp
from collections import Counter
class node:
    def __init__(self, team):
        self.team = team
        self.list = []
        self.rating_array = []
        self.average_rating = 0
    def __str__(self):
        return f"{self.team}, {self.list}"
    def add(self, item):
        for x in item:
            self.list.append(x)
    def add_rating(self, item):
        self.rating_array.append(item)
    def remove_duplicates(self):
        unique_list = []
        seen_ids = set()
        for obj in self.list:
            if obj.team not in seen_ids:
                unique_list.append(obj)
                seen_ids.add(obj.team)
        self.list = unique_list

    def check_list(self):
        team = self.team
        for x in self.list:
            if int(team) == int(x.team):
                self.list.remove(x)
    def find_average_rating(self):
        self.average_rating = sum(self.rating_array) / len(self.rating_array)
    def generate_list(self):
        team = self.team
        with open('match2.json') as f:
            x = json.load(f)
            matches_obj = x['matches']
            keys = matches_obj.keys()
            for y in range(1, len(keys)+1):
                z = "match" + str(y)
                if int(x['matches'][z]["t1"]) == team:
                    if int(x['matches'][z]["r1"]) == 1:
                        continue
                    elif int(x['matches'][z]["r1"]) == 2:
                        if int(x['matches'][z]["r2"]) == 3:
                            self.list.append(node(x['matches'][z]["t3"]))
                        else:
                            self.list.append(node(x['matches'][z]["t2"]))
                    else:
                        self.list.append(node(x['matches'][z]["t2"]))
                        self.list.append(node(x['matches'][z]["t3"]))
                elif int(x['matches'][z]["t2"]) == team:
                    if int(x['matches'][z]["r2"]) == 1:
                        continue
                    elif int(x['matches'][z]["r2"]) == 2:
                        if int(x['matches'][z]["r3"]) == 3:
                            self.list.append(node(x['matches'][z]["t1"]))
                        else:
                            self.list.append(node(x['matches'][z]["t3"]))
                    else:
                        self.list.append(node(x['matches'][z]["t1"]))
                        self.list.append(node(x['matches'][z]["t3"]))
                elif int(x['matches'][z]["t3"]) == team:
                    if int(x['matches'][z]["r3"]) == 1:
                        continue
                    elif int(x['matches'][z]["r3"]) == 2:
                        if int(x['matches'][z]["r2"]) == 3:
                            self.list.append(node(x['matches'][z]["t1"]))
                        else:
                            self.list.append(node(x['matches'][z]["t2"]))
                    else:
                        self.list.append(node(x['matches'][z]["t1"]))
                        self.list.append(node(x['matches'][z]["t2"]))
                else:
                    continue
            self.check_list()


def find_teams_worse(teams, team):
    index = teams.index(team)
    list = []
    for x in range(index + 1, len(teams)):
        list.append(teams[x])
    return list

def generate_better_than_list():
    node_list = []
    with open("match2.json", "r") as f:
        x = json.load(f)
        matches_obj = x['matches']
        keys = matches_obj.keys()
        #print(len(keys))
        for y in range(1, len(keys)+1):
            b = "match" + str(y)
            for z in range(1,4):
                c = "t" + str(z)
                a = node(int(x['matches'][b][c]))
                a.generate_list()
                node_list.append(a)
    return node_list
def find_duplicates(data_list):
    seen = {}
    for x in data_list:
        try:
            if seen[x.team] == None:
                seen[x.team] = 1
            else:
                seen[x.team] += 1
        except:
            seen[x.team] = 1
    return seen
def check_sublist_presence(larger_list, value_1, value_2):
    for sublist in larger_list:
        if len(sublist) == 3 and sublist[0] == value_1 and sublist[1] == value_2:
            #print(sublist)
            return True
    return False

def find_third_value(larger_list, value_1, value_2):
    for sublist in larger_list:
        if len(sublist) == 3 and sublist[0] == value_1 and sublist[1] == value_2:
            #print(sublist)
            #print("Weight: " + str(sublist[2]))
            return sublist[2]
    return 0
def find_node_by_team(nodes, target_team):
  for node in nodes:
    if node.team == target_team:
      return node

  return None

def weighed_graph():
    y = generate_better_than_list()
    G = nx.DiGraph()
    seen_teams = []
    seen_nodes = []
    edge_list = []
    for node in y:
        team = node.team
        if team in seen_teams:
            continue
        seen_teams.append(team)
        seen_nodes.append(node)
        outperformed_teams = node.list
        dupes = find_duplicates(node.list)
        seen = []
        for outperformed_team in outperformed_teams:
            if outperformed_team.team in seen:
                continue
            elif int(outperformed_team.team) == int(node.team):
                continue
            else:
                seen.append(outperformed_team.team)

        outperformed_teams = seen
        for outperformed_team in outperformed_teams:
            if dupes[outperformed_team] != None:
                # amount of times team outranked other team
                temp1 = dupes[outperformed_team]
                #print(temp1)
                if [node, int(outperformed_team), temp1] in edge_list:
                    continue
                edge_list.append([int(node.team), int(outperformed_team), temp1])
            else:
                edge_list.append([int(node.team), int(outperformed_team), 1])
    for x in seen_nodes:
        G.add_node(x)
    #print("x")
    for edge in edge_list:
        if G.has_edge(find_node_by_team(seen_nodes,edge[0]), find_node_by_team(seen_nodes,edge[1])):
            continue
        else:
            if check_sublist_presence(edge_list, edge[0], edge[1]):
                weight = find_third_value(edge_list,edge[0],edge[1])
                other_weight = find_third_value(edge_list,edge[1],edge[0])
                total = find_third_value(edge_list, edge[0],edge[1]) + find_third_value(edge_list, edge[1],edge[0])
                print("Node 1: " + str(edge[0]) + ", Node 2: " + str(edge[1]) + ", Weight: " + str(weight/total))
                print(edge_list)
                G.add_edge(find_node_by_team(seen_nodes,edge[0]),find_node_by_team(seen_nodes,edge[1]),weight=weight/total)
                G.add_edge(find_node_by_team(seen_nodes,edge[1]),find_node_by_team(seen_nodes,edge[0]),weight=other_weight/total)

# Example usage (replace with your actual data)
    remove = []
    for x in G.edges:
        if x[0] == x[1]:
            remove.append(x[0])
    for x in range(len(remove)):
        G.remove_edge(remove[x],remove[x])
    #for u,v in G.edges:
        #print(u)
        #print(v)
        #print(G.get_edge_data(u,v))
    for x in seen_nodes:
        x.remove_duplicates()
        x.check_list()
        #print(x.team)
        #for y in x.list:
            #print(y)
    for u,v in G.edges:
        print(str(u.team) + " -> " + str(v.team) + " Weight: " + str(G[u][v]['weight']))


    def R(A, B, currTeam, G, seen_nodes, seen, found):
        # 1st check if there exists an edge between A and B
        if G.has_edge(currTeam, find_node_by_team(seen_nodes, B)):
            return {'prob': G[currTeam][find_node_by_team(seen_nodes, B)]['weight'], 'dist': 1}
        if len(G.out_edges(currTeam)) == 0:
            print("No edges")
            return None
        print("Team: " + str(currTeam.team))
        for u,v in G.out_edges(currTeam):
            print("Node 1: " + str(u.team))
            print("Node 2: " + str(v.team))
            seen.append(currTeam.team)
            #print(seen)
            if v.team == B:
                return {'prob': G[u][v]['weight'], 'dist': 1}
            if u.team in seen and v.team in seen:
                continue
            temp = R(A, B, v, G, seen_nodes, seen, found)
            print(v.team)
            print(temp)
            if G.has_edge(v, find_node_by_team(seen_nodes, B)):
                found.append({'prob': temp['prob'] * G[u][v]['weight'], 'dist': temp['dist'] + 2})
            print(found)
        lowest = None
        if len(found) == 0:
            print("No found")
            return lowest
        #print(len(found))
        lowest = found[0]['dist']
        edge_weight = found[0]['prob']
        for x in range(len(found)):
            # maximize edge weight
            temp = found[x]['dist']
            temp2 = found[x]['prob']
            if temp <= lowest:
                lowest = temp
                edge_weight = found[x]['prob']
            #print(edge_weight)
            #print(temp2)
            if temp2 > edge_weight:
                edge_weight = temp2
                #print(str(edge_weight) + " Edge Weight!!")
        return {'prob': edge_weight, 'dist': lowest}


    #print(G.has_edge(find_node_by_team(seen_nodes, 3310),find_node_by_team(seen_nodes, 3743)))
    #for x in seen_nodes:
        #print(x)
    A = input("What team are you comparing 1st? ")
    B = input("What team are you comparing 2nd? ")
    currTeam = find_node_by_team(seen_nodes, int(A))

    '''for x,y in G.edges:
        if x.team == 9105:
            print(str(x.team) + " -> " + str(y.team) + " Probability: " + str(G[x][y]['weight']))
        if y.team == 2687:
            print(str(x.team) + " -> " + str(y.team) + " Probability: " + str(G[x][y]['weight']))'''
    if currTeam != None and find_node_by_team(seen_nodes, int(B)) != None:
        print(str(A) + " is better than " + str(B) + " about " + str(R(int(A), int(B), currTeam, G, seen_nodes, [], [])['prob'] * 100) + "% of the time, and has a distance of " + str(R(int(A), int(B), currTeam, G, seen_nodes, [], [])['dist']))
    else:
        print("Error! Team not found!")
    #for x in find_node_by_team(seen_nodes,3310).list:
        #print(x)
#3310 9088 9156 2468 3005 7492 2582 8512 418 7321 9407 9714 7534 9752 7271 4251 7506 4206 9492 8842 7503 5411

weighed_graph()
#turn it into nodes

def find_matching_dictionary(data, target_value):

    for item in data:
        for value in item.values():
            if isinstance(value, int) and value == target_value:
                return item
            elif isinstance(value, str) and value.isdigit() and int(value) == target_value:
                return item











