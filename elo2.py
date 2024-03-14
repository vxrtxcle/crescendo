import operator
import statbotics
import urllib
import requests
import numpy as np
import random
import json
import operator
import networkx as nx
'''
sb = statbotics.Statbotics()
y = sb.get_team_event(2468,'2024txwac')
print("Team Event")
for x in y:
    print(f"{x}: {y[x]}")
y = sb.get_team(2468)
print("Team")
for x in y:
    print(f"{x}: {y[x]}")
y = sb.get_team_year(2468,2024)
print("Team Year")
for x in y:
    print(f"{x}: {y[x]}")
y = sb.get_match('2024txwac_sf7m1')
print("Match")
for x in y:
    print(f"{x}: {y[x]}")
y = sb.get_team_match(2468,'2024txwac_sf7m1')
print("Team Match")
for x in y:
    print(f"{x}: {y[x]}")
y = sb.get_team_matches(2468,2024)
print("Team Matches")
print(y)
'''
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

def weighed_graph():
    y = generate_better_than_list()
    x = nx.Graph()
    for a in y:
        x.add_node(a.team)
        if len(a.list) > 0:
            for b in a.list:
                x.add_edge(a.team,b)
    print(x.number_of_nodes())
    print(x.number_of_edges())

def generate_json():
    teams = []
    y = input("Which event? ")
    url = "https://www.thebluealliance.com/api/v3/event/" + y + "/teams/keys"
    headers = {'X-TBA-Auth-Key': tba_key}
    response = requests.get(url, headers)
    req = response.json()
    for j in req:
        k = j.replace("frc","")
        teams.append(k)
    match_dict = {}
    temp = teams
    rating = [1,2,3]
    match_dict.update({"matches": {}})
    for l in range(1,101):
        z = "match" + str(l)
        match_dict['matches'].update({z: {}})
        match_dict["matches"][z].update({"match": l})
        match_dict["matches"][z].update({"t1": random.choice(temp)})
        temp.remove(match_dict["matches"][z]["t1"])
        match_dict["matches"][z]["t2"] = random.choice(temp)
        temp.remove(match_dict["matches"][z]["t2"])
        match_dict["matches"][z]["t3"] = random.choice(temp)
        temp.remove(match_dict["matches"][z]["t3"])
        match_dict["matches"][z]["r1"] = random.choice(rating)
        rating.remove(match_dict["matches"][z]["r1"])
        match_dict["matches"][z]["r2"] = random.choice(rating)
        rating.remove(match_dict["matches"][z]["r2"])
        match_dict["matches"][z]["r3"] = random.choice(rating)
        rating.remove(match_dict["matches"][z]["r3"])
        temp.append(match_dict["matches"][z]["t1"])
        temp.append(match_dict["matches"][z]["t2"])
        temp.append(match_dict["matches"][z]["t3"])
        rating.append(1)
        rating.append(2)
        rating.append(3)
    open("match2.json", "w").close()
    with open('match2.json', 'w') as f:
        json.dump(match_dict, f,
                  indent=4,
                  separators=(',', ': '))


def get_real_cycle_time():
    with open("Week 0 Testing.json", "r") as f:
        z = []
        time_diff = []
        x = json.load(f)
        for y in x:
            if y['tele_amp_scored'] or y['tele_spk_scored'] != None:
                amp = []
                spk = []
                comb = []
                print(f'Team Number: {y["team_#"]}')
                print(f'Match Number: {y["match_#"]}')
                if isinstance(y['tele_amp_scored'], list):
                    for a in y['tele_amp_scored']:
                        #print("adding1")
                        amp.append(a)
                        comb.append(a)
                if isinstance(y['tele_amp_scored'], int):
                    #print("adding3")
                    amp.append(y['tele_amp_scored'])
                    comb.append(y['tele_amp_scored'])
                if isinstance(y['tele_spk_scored'], list):
                    for a in y['tele_spk_scored']:
                        #print("adding2")
                        spk.append(a)
                        comb.append(a)
                if isinstance(y['tele_spk_scored'], int):
                    #print("adding4")
                    spk.append(y['tele_spk_scored'])
                    comb.append(y['tele_spk_scored'])
                if amp != []:
                    time_diff = []
                    amp.sort()
                    total = 0
                    for b in range(len(amp)-1):
                        time_diff.append(amp[b+1]-amp[b])
                    for c in time_diff:
                        #print(c)
                        total += c
                    if len(time_diff) == 0:
                        print("Only had 1 Amp scoring cycle!")
                    else:
                        cycle_time = total / len(time_diff)
                        print(f'Amp Cycle Time: {cycle_time/1000}')
                if spk != []:
                    time_diff = []
                    spk.sort()
                    total = 0
                    for b in range(len(spk)-1):
                        time_diff.append(spk[b+1]-spk[b])
                    for c in time_diff:
                        #print(c)
                        total += c
                    if len(time_diff) == 0:
                        print("Only had 1 non-amped scoring cycle!")
                    else:
                        cycle_time = total / len(time_diff)
                        print(f'Non-Amped Speaker Cycle Time: {cycle_time/1000}')
                if comb != []:
                    time_diff = []
                    comb.sort()
                    total = 0
                    for b in range(len(comb)-1):
                        time_diff.append(comb[b+1]-comb[b])
                    for c in time_diff:
                        #print(c)
                        total += c
                    if len(time_diff) == 0:
                        print("Only had 1 non-amped cycle!")
                    else:
                        cycle_time = total / len(time_diff)
                        print(f'Non-Amped Total Cycle Time: {cycle_time/1000}')


def elo_match_calculations():
    sb = statbotics.Statbotics()
    x = input("Write the event code: ")
    teams = initialize_teams_and_epas(x)
    url = "https://www.thebluealliance.com/api/v3/event/" + x + "/matches/keys"
    headers = {'X-TBA-Auth-Key': tba_key}
    response = requests.get(url, headers)
    req = response.json()
    for y in req:
        r1 = sb.get_match(y).get('red_1')
        r2 = sb.get_match(y).get('red_2')
        r3 = sb.get_match(y).get('red_3')
        b1 = sb.get_match(y).get('blue_1')
        b2 = sb.get_match(y).get('blue_2')
        b3 = sb.get_match(y).get('blue_3')

elo_match_calculations()
#for x in generate_better_than_list():
 #   print(x)
