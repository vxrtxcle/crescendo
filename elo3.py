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
    def check_list(self):
        team = self.team
        for x in self.list:
            if team == x.team:
                self.list.remove(x)
    def find_average_rating(self):
        self.average_rating = sum(self.rating_array) / len(self.rating_array)
    def generate_list(self):
        team = self.team
        with open('match2.json') as f:
            x = json.load(f)
            for y in range(1,301):
                z = "match" + str(y)
                if int(x['matches'][z]["t1"]) == team:

                    if int(x['matches'][z]["r1"]) == 1:
                        continue
                    elif int(x['matches'][z]["r1"]) == 2:
                        if int(x['matches'][z]["r2"]) == 3:
                            self.list.append(node(x['matches'][z]["t3"]))
                        else:
                            self.list.append(node(x['matches'][z]["t1"]))
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
    def generate_other_list(self):
        team = self.team
        with open('match2.json') as f:
            x = json.load(f)
            for y in range(1, 301):
                z = "match" + str(y)
                if int(x['matches'][z]["t1"]) == team:

                    if int(x['matches'][z]["r1"]) == 3:
                        continue
                    elif int(x['matches'][z]["r1"]) == 2:
                        if int(x['matches'][z]["r2"]) == 1:
                            self.list.append(x['matches'][z]["t3"])
                        else:
                            self.list.append(x['matches'][z]["t1"])
                    else:
                        self.list.append(x['matches'][z]["t2"])
                        self.list.append(x['matches'][z]["t3"])
                elif int(x['matches'][z]["t2"]) == team:
                    if int(x['matches'][z]["r2"]) == 1:
                        continue
                    elif int(x['matches'][z]["r2"]) == 2:
                        if int(x['matches'][z]["r3"]) == 3:
                            self.list.append(x['matches'][z]["t1"])
                        else:
                            self.list.append(x['matches'][z]["t3"])
                    else:
                        self.list.append(x['matches'][z]["t1"])
                        self.list.append(x['matches'][z]["t3"])
                elif int(x['matches'][z]["t3"]) == team:
                    if int(x['matches'][z]["r3"]) == 1:
                        continue
                    elif int(x['matches'][z]["r3"]) == 2:
                        if int(x['matches'][z]["r2"]) == 3:
                            self.list.append(x['matches'][z]["t1"])
                        else:
                            self.list.append(x['matches'][z]["t2"])
                    else:
                        self.list.append(x['matches'][z]["t1"])
                        self.list.append(x['matches'][z]["t2"])
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
        for y in range(1,101):
            b = "match" + str(y)
            for z in range(1,4):
                c = "t" + str(z)
                a = node(int(x['matches'][b][c]))
                a.generate_list()
                node_list.append(a)
    return node_list
def find_duplicates(data_list):

  counts = Counter(data_list)

  duplicates = {item: count for item, count in counts.items() if count > 1}

  return duplicates
def check_sublist_presence(larger_list, sublist):


  # Use list comprehension for efficient comparison
  return any(sublist[:2] == inner_list[:2] for inner_list in larger_list)

def find_third_value(larger_list, target_sublist):


  for inner_list in larger_list:
    if inner_list[:2] == target_sublist:
      if len(inner_list) >= 3:
        return inner_list[2]
      else:
        return None
  return None
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
        for outperformed_team in outperformed_teams:

            if outperformed_team in dupes:
                # amount of times team outranked other team
                temp1 = dupes[outperformed_team]
                if [node, outperformed_team, temp1] in edge_list:
                    continue
                edge_list.append([int(node.team), int(outperformed_team.team), temp1])
            else:
                edge_list.append([int(node.team), int(outperformed_team.team), 1])
    for x in seen_nodes:
        G.add_node(x)
    for edge in edge_list:
        if G.has_edge(find_node_by_team(seen_nodes,edge[0]), find_node_by_team(seen_nodes,edge[1])):
            continue
        else:
            if check_sublist_presence(edge_list, [edge[1], edge[0]]):
                #print("hi")
                weight = find_third_value(edge_list, [edge[0],edge[1]])
                other_weight = find_third_value(edge_list, [edge[1],edge[0]])
                total = find_third_value(edge_list, [edge[0],edge[1]]) + find_third_value(edge_list, [edge[1],edge[0]])
                G.add_edge(find_node_by_team(seen_nodes,edge[0]),find_node_by_team(seen_nodes,edge[1]),weight=weight/total)
                G.add_edge(find_node_by_team(seen_nodes,edge[1]),find_node_by_team(seen_nodes,edge[0]),weight=other_weight/total)

# Example usage (replace with your actual data)
    #print(G.edges(data=True))
    remove = []
    for x in G.edges:
        if x[0] == x[1]:
            remove.append(x[0])
    for x in range(len(remove)):
        G.remove_edge(remove[x],remove[x])
    print(G)
    currTeam = find_node_by_team(seen_nodes,2468)

    def R(A, B, currTeam, G, seen_nodes):
        node = G[currTeam]
        print(A)
        print(B)
        print(currTeam)
        # print(G.has_node(currTeam))
        if G.has_edge(find_node_by_team(seen_nodes, A), find_node_by_team(seen_nodes, B)):
            weight = G.edges[node(A), node(B)]['weight']
            return {'prob': weight, 'dist': 1}
        found = []
        # print(node)
        # print(G.out_edges(node))
        if len(G.out_edges(node)) == 0:
            print("No edges")
            return None
        for edge in G.out_edges(node):
            temp = R(currTeam.team, B, edge[1], G, seen_nodes)
            found.append({'prob': temp.weight * edge.weight, 'dist': temp.dist + 1})
        lowest = None
        if len(found) == 0:
            print("No found")
            return lowest
        for x in found:
            temp = x['dist']
            if temp < lowest:
                lowest = temp
            else:
                continue
        if lowest != None:
            return find_matching_dictionary(found, lowest)
    print(R(2468, 3310, currTeam, G, seen_nodes))
#def ask_questions(G):

weighed_graph()
#turn it into nodes

def find_matching_dictionary(data, target_value):

    for item in data:
        for value in item.values():
            if isinstance(value, int) and value == target_value:
                return item
            elif isinstance(value, str) and value.isdigit() and int(value) == target_value:
                return item








