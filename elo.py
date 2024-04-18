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
import os
from dotenv import load_dotenv
load_dotenv()
tba_key = os.getenv('X_TBA_Auth_Key')

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
            if team == int(x):
                self.list.remove(x)
    def find_average_rating(self):
        self.average_rating = sum(self.rating_array) / len(self.rating_array)
    def generate_list(self):
        team = self.team
        with open('match2.json') as f:
            x = json.load(f)
            for y in range(1,101):
                z = "match" + str(y)
                if int(x['matches'][z]["t1"]) == team:

                    if int(x['matches'][z]["r1"]) == 1:
                        continue
                    elif int(x['matches'][z]["r1"]) == 2:
                        if int(x['matches'][z]["r2"]) == 3:
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
    def generate_other_list(self):
        team = self.team
        with open('match2.json') as f:
            x = json.load(f)
            for y in range(1, 101):
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





def initialize_teams_and_epas(event):
    sb = statbotics.Statbotics()
    teams = []
    epas = []
    print("Initializing teams and epas")
    url = "https://www.thebluealliance.com/api/v3/event/" + event + "/teams/keys"
    headers = {'X-TBA-Auth-Key': tba_key}
    response = requests.get(url, headers)
    req = response.json()
    team_elo = []
    for a in req:
        b = a.replace('frc', '')
        teams.append(int(b))
    for c in teams:
        try:
            print(sb.get_team(c))
            epas.append(sb.get_team(c).get("norm_epa_mean"))
        except:
            epas.append(1450)
            continue
    for x in range(0, len(teams)):
        team_elo.append([teams[x], epas[x]])
    return sorted(team_elo, key=lambda x: x[1], reverse=True)
def match_difficulty():
    array_1 = []
    sb = statbotics.Statbotics()
    #x = input("Which team? ")
    y = input("Which event? ")
    url = "https://www.thebluealliance.com/api/v3/event/" + y + "/matches/keys"
    headers = {'X-TBA-Auth-Key': tba_key}
    response = requests.get(url, headers)
    req = response.json()
    match_keys = []
    normalized_epas = []
    url2 = "https://www.thebluealliance.com/api/v3/event/" + y + "/teams/keys"
    blue = 0
    red = 0
    diff = []
    response2 = requests.get(url2, headers)
    req2 = response2.json()
    teams = []
    for a in req2:
        b = a.replace('frc', '')
        teams.append(int(b))
    schedule_difficulty = 0
    schedule_array = []
    for z in teams:
        print(z)
        #print(z)
        schedule_difficulty = 0
        for i in sb.get_team_matches(team=int(z), event=y):
            # Check if the team is red or blue
            blue = sb.get_match(i.get('match')).get('blue_epa_sum')
            #print(blue)
            red = sb.get_match(i.get('match')).get('red_epa_sum')
            #print(red)
            if sb.get_match(i.get('match')).get('blue_1') == int(z) or sb.get_match(i.get('match')).get('blue_2') == int(z) or sb.get_match(i.get('match')).get('blue_3') == int(z):
                diff.append(-(blue - red))
            else:
                diff.append(-(red-blue))
        for j in diff:
            #print(j)
            schedule_difficulty += j
        #print(schedule_difficulty)
        schedule_array.append(schedule_difficulty)
    mean = 0
    stdev = 0
    for k in schedule_array:
        mean += k
    mean = mean / len(schedule_array)
    for l in schedule_array:
        stdev += (float(l) - float(mean)) ** 2.0
    stdev = stdev / len(schedule_array)
    stdev = stdev ** 0.5
    for m in range(0,len(schedule_array)):
        schedule_array[m] = (schedule_array[m] - mean) / stdev
    for x in range(0,len(schedule_array)):
        print(str(schedule_array[x]) + " " + str(teams[x]))

def raw_skill(event):
    x = initialize_teams_and_epas(event)
    teams = []
    epas = []
    for i in x:
        teams.append(i[0])
        epas.append(i[1])
    generate_matches(teams)


def actual_skill():
    y = input("Write the Event Code: ")
    string1 = ""
    url = "https://www.thebluealliance.com/api/v3/event/" + y + "/rankings"
    headers = {'X-TBA-Auth-Key': tba_key}
    response = requests.get(url, headers)
    req = response.json()
    for x in req.get('rankings'):
        z = x.get('team_key')
        z = z.replace('frc', '')
        string1 += str(z) + " "
    print("Rankings:")
    print(string1)
def generate_matches(teams):
    print("Generating matches")
    matches = []
    sb = statbotics.Statbotics()
    i = 0
    red = []
    blue = []
    sum_red = 0
    sum_blue = 0
    node_teams = []
    temp3 = []
    team_list = []
    for x in range(len(teams)):
        node_teams.append(node(teams[x]))
    for x in range(len(node_teams)):
        node_teams[x].add(find_teams_worse(teams, node_teams[x].team))
    while i < 2000:
        red = []
        blue = []
        sum_red = 0
        sum_blue = 0
        temp = node_teams
        a = random.choice(temp)
        temp.remove(a)
        b = random.choice(temp)
        temp.remove(b)
        c = random.choice(temp)
        temp.remove(c)
        d = random.choice(temp)
        temp.remove(d)
        e = random.choice(temp)
        temp.remove(e)
        f = random.choice(temp)
        temp.remove(f)
        red.append(a)
        red.append(b)
        red.append(c)
        blue.append(d)
        blue.append(e)
        blue.append(f)
        matches.append(red)
        matches.append(blue)
        temp.append(a)
        temp.append(b)
        temp.append(c)
        temp.append(d)
        temp.append(e)
        temp.append(f)
        temp = random.shuffle(temp)
        i += 1
    rate(matches)
    string1 = ""
    for x in node_teams:
        x.find_average_rating()
        temp3.append([x.team,x.average_rating])
    team_list = sorted(temp3, key=lambda x: x[1], reverse=True)
    for x in range(len(team_list)):
        string1 += str(team_list[x][0]) + " "
    actual_skill()
    print("Simulated Rankings:")
    print(string1)



def find_teams_worse(teams, team):
    index = teams.index(team)
    list = []
    for x in range(index + 1, len(teams)):
        list.append(teams[x])
    return list
def rate(matches):
    a = 0
    b = 0
    c = 0
    for x in matches:
        if len(x[0].list) > len(x[1].list) and len(x[1].list) > len(x[2].list) and len(x[0].list) > len(x[2].list): # 0 1 2
            x[0].add_rating(3)
            x[1].add_rating(2)
            x[2].add_rating(1)
        elif len(x[0].list) > len(x[1].list) and len(x[1].list) < len(x[2].list) and len(x[0].list) > len(x[2].list):  # 0 2 1
            x[0].add_rating(3)
            x[1].add_rating(1)
            x[2].add_rating(2)
        elif len(x[0].list) < len(x[1].list) and len(x[1].list) > len(x[2].list) and len(x[2].list) < len(x[0].list):  # 1 0 2
            x[0].add_rating(2)
            x[1].add_rating(3)
            x[2].add_rating(1)
        elif len(x[0].list) < len(x[1].list) and len(x[1].list) > len(x[2].list) and len(x[2].list) > len(x[0].list):  # 1 2 0
            x[0].add_rating(1)
            x[1].add_rating(3)
            x[2].add_rating(2)
        elif len(x[0].list) > len(x[1].list) and len(x[1].list) < len(x[2].list) and len(x[2].list) > len(x[0].list):  # 2 0 1
            x[0].add_rating(2)
            x[1].add_rating(1)
            x[2].add_rating(3)
        else:
            x[0].add_rating(1)
            x[1].add_rating(2)
            x[2].add_rating(3)

#raw_skill()
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
    print(y)
    x = nx.MultiDiGraph()
    for a in y:
        x.add_node(a.team)
        if len(a.list) > 0:
            for b in a.list:

                x.add_edge(a.team,b, weight=1)

    print(x.number_of_nodes())
    print(x.number_of_edges())
    print(x.edges)
    print(x.nodes)

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
    print(len(teams))
    temp = teams
    rating = [1,2,3]
    match_dict.update({"matches": {}})
    for l in range(1,6):
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
    teamsandepas = initialize_teams_and_epas(x)
    teams = []
    epas = []
    for y in teamsandepas:
        teams.append(y[0])
        epas.append(y[1])
    print(epas)
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
        #print(sb.get_match(y))
        if b1 == 2468:
            color = "blue"
        elif b2 == 2468:
            color = "blue"
        elif b3 == 2468:
            color = "blue"
        elif r1 == 2468:
            color = "red"
        elif r2 == 2468:
            color = "red"
        elif r3 == 2468:
            color = "red"
        else:
            continue
        if color == "red":
            diff = -(epas[teams.index(r1)] + epas[teams.index(r2)] + epas[teams.index(r3)]) + (epas[teams.index(b1)] + epas[teams.index(b2)] + epas[teams.index(b3)])
            print(diff)
            print("Match Number: " + str(sb.get_match(y).get('match_number')))
            print("Win Probability: " + str(round(1 / (1 + 10 ** (diff / 400)), 2) * 100) + "%")
        elif color == "blue":
            diff = (epas[teams.index(r1)] + epas[teams.index(r2)] + epas[teams.index(r3)]) - (epas[teams.index(b1)] + epas[teams.index(b2)] + epas[teams.index(b3)])
            print(diff)
            print("Match Number: " + str(sb.get_match(y).get('match_number')))
            print("Win Probability: " + str(round(1 / (1 + 10 ** (diff / 400)), 2) * 100) + "%")
        else:
            continue



def stand_dev():
    #x = input('Write the event code: ')
    url = "https://www.thebluealliance.com/api/v3/event/2024isde1/matches/simple"
    headers = {'X-TBA-Auth-Key': tba_key}
    response = requests.get(url, headers)
    req = response.json()
    total = 0
    scores = []
    for x in req:
        scores.append(x['alliances']['blue']['score'])
        scores.append(x['alliances']['red']['score'])
    for y in scores:
        total += y
    temp1 = total / len(scores)
    print("Mean: " + str(temp1))
    temp = 0
    for z in scores:
        temp += abs(z - temp1)
        #print(z - temp1)
    a = (temp / len(scores)) ** 0.5
    print("Standard Deviation: " + str(a))
    count = 0
    b = 8 * a
    for z in scores:
        if abs(z-temp1) < b:
            count += 1
        else:
            print("Outlier: " + str(z))
    print("Percentage covered between " + str(temp1 - b) + " and " + str(temp1 + b) + " is " + str(count/len(scores)))



def auto_paths():
    url = "https://www.thebluealliance.com/api/v3/event/2024week0/matches"
    headers = {'X-TBA-Auth-Key': tba_key}
    response = requests.get(url, headers)
    req = response.json()
    for x in req:
        print(x)

# opr calcs

def convert_rld_to_tpw():
    with open("Trainings.json", "r") as file1, open("tpw_testing.json", "w") as file2:
        open('tpw_testing.json', 'w').close()

        f1 = json.load(file1)
        for x in f1:
            if x['auto_leave'] == 'No':
                auto_leave = False
            else:
                auto_leave = True
            if x['disconnect'] == 'No':
                bricked = False
            else:
                bricked = True
            if x['field-2'] == 'No':
                defense = False
            else:
                defense = True
            if x['tele_ground_pickup'] == None:
                ground_pickup = False
            else:
                ground_pickup = True
            if x['tele_source_pickup'] == None:
                source_pickup = False
            else:
                source_pickup = True
            if x['auto_note_4_pickup'] == None and x['auto_note_5_pickup'] == None and x['auto_note_6_pickup'] == None and x['auto_note_7_pickup'] == None and x['auto_note_8_pickup'] == None:
                auto_center = False
            else:
                auto_center = True
            if x['endgame_stage_actions'] == 'Onstage Spotlit':
                spotlit = True
            else:
                spotlit = False
            if x['endgame_stage_actions'] == 'Onstage':
                hang = 2
            elif x['endgame_stage_actions'] == 'Park':
                hang = 1
            elif x['endgame_stage_actions'] == 'None':
                hang = 0
            elif (x['endgame_stage_actions'] == 'Onstage' or x['endgame_stage_actions'] == 'Onstage Spotlit') and x['harmony'] == 'Part of 2 bots':
                hang = 3
            elif (x['endgame_stage_actions'] == 'Onstage' or x['endgame_stage_actions'] == 'Onstage Spotlit') and x['harmony'] == 'Part of 3 bots':
                hang = 4
            if x['tele_amp_scored'] == None:
                teleamp = 0
            elif isinstance(x['tele_amp_scored'], int):
                teleamp = 1
            else:
                teleamp = len(x['tele_amp_scored'])
            if x['tele_spk_scored'] == None:
                telespk = 0
            elif isinstance(x['tele_spk_scored'], int):
                telespk = 1
            else:
                telespk = len(x['tele_spk_scored'])
            if x['speaker_scored_amped'] == None:
                teleaspk = 0
            elif isinstance(x['speaker_scored_amped'], int):
                teleaspk = 1
            else:
                teleaspk = len(x['speaker_scored_amped'])
            temp = {
                                "metadata": {
                                    "scouter": {
                                        "team": 2468,
                                        "app": 'rld'
                                        },
                                   "event": '',
                                   "bot": 0,
                                   'match': {
                                       'level': 0,
                                       'number': 0
                                   },
                                   'timestamp': 0
                                   },
                                "abilities": {
                                    "auto-leave-starting-zone": False,
                                    'bricked': False,
                                    "ground-pick-up": False,
                                    "source-pick-up": False,
                                    "auto-center-line-pick-up": False,
                                    "teleop-spotlight-2024": False,
                                    'defense': False,
                                    "teleop-stage-level-2024": 0,
                                },
                                "counters": {
                                    "auto-scoring-amp-2024": x['auto_amp_scored'],
                                    "teleop-scoring-amp-2024": teleamp,
                                    "auto-scoring-speaker-2024": x['auto_spk_scored'],
                                    "teleop-scoring-speaker-2024": telespk,
                                    "teleop-scoring-trap-2024": x['tele_trap_scored'],
                                    "teleop-scoring-amplified-speaker-2024": teleaspk,
                                },
                                "data": {
                                    "notes": x['comments'],
                                },
                                "ratings": {

                                },
                                "timers": {

                                }}
            temp['metadata']['scouter']['team'] = 2468
            temp['metadata']['scouter']['app'] = 'rld'
            temp['metadata']['event'] = x['event']
            temp['metadata']['bot'] = x['team_#']
            temp['metadata']['match']['level'] = x['level']
            temp['metadata']['match']['number'] = x['match_#']
            temp['metadata']['timestamp'] = x['Record Time Client']
            temp['abilities']['auto-leave-starting-zone'] = auto_leave
            temp['abilities']['bricked'] = bricked
            temp['abilities']['ground-pick-up'] = ground_pickup
            temp['abilities']['source-pick-up'] = source_pickup
            temp['abilities']['auto-center-line-pick-up'] = auto_center
            temp['abilities']['teleop-spotlight-2024'] = spotlit
            temp['abilities']['defense'] = defense
            temp['abilities']['teleop-stage-level-2024'] = hang
            temp['counters']["auto-scoring-amp-2024"] = x['auto_amp_scored']
            temp['counters']["teleop-scoring-amp-2024"] = teleamp
            temp['counters']["auto-scoring-speaker-2024"] = x['auto_spk_scored']
            temp['counters']["teleop-scoring-speaker-2024"] = telespk
            temp['counters']["teleop-scoring-trap-2024"] = x['tele_trap_scored']
            temp['counters']["teleop-scoring-amplified-speaker-2024"] = teleaspk
            temp['data']['notes'] = x['comments']
            temp['ratings'] = {}
            temp['timers'] = {}
            with open('tpw_testing.json', 'w') as f:
                print(temp, file=f)
                '''
            temp['entries'] += {
                                "metadata": {
                                    "scouter": {
                                        "team": 2468,
                                        "app": 'rld'
                                        },
                                   "event": x['event'],
                                   "bot": x['team_#'],
                                   'match': {
                                       'level': x['level'],
                                       'number': x['match_#']
                                   },
                                   'timestamp': x['Record Time Client']
                                   },
                                "abilities": {
                                    "auto-leave-starting-zone": auto_leave,
                                    'bricked': bricked,
                                    "ground-pick-up": ground_pickup,
                                    "source-pick-up": source_pickup,
                                    "auto-center-line-pick-up": auto_center,
                                    "teleop-spotlight-2024": spotlit,
                                    'defense': defense,
                                    "teleop-stage-level-2024": 2,
                                },
                                "counters": {
                                    "auto-scoring-amp-2024": x['auto_amp_scored'],
                                    "teleop-scoring-amp-2024": teleamp,
                                    "auto-scoring-speaker-2024": x['auto_spk_scored'],
                                    "teleop-scoring-speaker-2024": telespk,
                                    "teleop-scoring-trap-2024": x['tele_trap_scored'],
                                    "teleop-scoring-amplified-speaker-2024": teleaspk,
                                },
                                "data": {
                                    "notes": x['comments'],
                                },
                                "ratings": {

                                },
                                "timers": {

                                }
            }

    print(temp)'''

    #with open("tpw_test.json", "x") as f:
     #   file_data

def qualitative_assignment():
    url = "https://www.thebluealliance.com/api/v3/event/2024gal/teams/keys"
    headers = {'X-TBA-Auth-Key': tba_key}
    response = requests.get(url, headers)
    req = response.json()
    teams = []
    teams2 = []
    arrays = ["Akash", "Arjun", "Ani", "Bjorn", "Ivy", "Sanaya", "Sara", "Shikhar"]
    for x in req:
        y = x.replace('frc', '')
        url = "https://www.thebluealliance.com/api/v3/team/" + x + "/events/2024/simple"
        headers = {'X-TBA-Auth-Key': tba_key}
        response = requests.get(url, headers)
        req = response.json()
        z = y + "\t" + arrays[random.randint(0, 7)] + "\t"

        for a in req:
            if a['event_code'] != "cmptx" or a['event_code'] != "gal":
                try:
                    #print(a)
                    z += a['city'] + " + "
                except Exception as e:
                    print(a)
        teams.append(z)
    teams.sort()
    for x in teams:
        print(x)
    url = "https://www.thebluealliance.com/api/v3/event/2024gal/teams/keys"
    response = requests.get(url,headers)
    req = response.json()
    common = []
    for x in req:
        url = "https://www.thebluealliance.com/api/v3/team/" + x +"/events/simple"
        #print(x['city'])

    #print(teams)


#actual_skill()
#raw_skill('2024txwac')
#match_difficulty()
qualitative_assignment()
'''
{
	"entries": [
			{
				"metadata": {
					"scouter": {
						"name": "omkar",
						"team": "1072",
						"app": "tpw",
					},
					"event": "2024camb",
					"bot": "9999",
					"match": {
						"level": "qm",
						"number": 1,
						"set": 1,
					},
					"timestamp": 1704604894,
				},
				"abilities": {
					"auto-leave-starting-zone": true,
					"ground-pick-up": false,
					"auto-center-line-pick-up": false,
					"teleop-spotlight-2024": false,
					"teleop-stage-level-2024": 2,
				},
				"counters": {

				},
				"data": {
					"auto-scoring-2024": ["as", "sm"],
					"teleop-scoring-2024": ["ss", "as", "am", "as", "sa", "sm", "tm", "ts"],
					"notes": "Overall bot was good and had cool RGB :)",
				},
				"ratings": {
					"driver-skill": 4,
					"defense-skill": 0,
					"speed": 3,
					"stability": 2,
					"intake-consistency": 5,
				},
				"timers": {
					"stage-time-2024": 6023,
					"brick-time": 0,
					"defense-time": 0,
				},
			},
			{
				"metadata": {
					"scouter": {
						"name": "kabir",
						"team": "1072",
						"app": "tpw",
					},
					"event": "2024camb",
					"bot": "9998",
					"match": {
						"level": "qm",
						"number": 1,
						"set": 1,
					},
					"timestamp": 1704605632,
				},
				"abilities": {
					"auto-leave-starting-zone": true,
					"ground-pick-up": true,
					"auto-center-line-pick-up": true,
					"teleop-spotlight-2024": true,
					"teleop-stage-level-2024": 3,
				},
				"counters": {

				},
				"data": {
					"auto-scoring-2024": ["as", "ss", "as"],
					"teleop-scoring-2024": ["as", "as", "as", "sa", "sm", "ss", "as", "am", "as", "sa", "ts", "ts"],
					"notes": "fast, scored consistently, low cycle times, good alliance partner strategies",
				},
				"ratings": {
					"driver-skill": 5,
					"defense-skill": 0,
					"speed": 4,
					"stability": 3,
					"intake-consistency": 5,
				},
				"timers": {
					"stage-time-2024": 2864,
					"brick-time": 0,
					"defense-time": 0,
				},
			},
			{
				"metadata": {
					"event": "2024camb",
					"match": {
						"level": "qm",
						"number": 3,
						"set": 1,
					},
					"bot": "9999",
					"timestamp": 1711729092182,
					"scouter": {
						"name": "kabir",
						"team": "1072",
						"app": "tpw"
					},
				},
				"abilities": {
					"auto-center-line-pick-up": false,
					"ground-pick-up": true,
					"auto-leave-starting-zone": true,
					"teleop-spotlight-2024": false,
					"teleop-stage-level-2024": 3
				},
				"counters": {

				},
				"data": {
					"auto-scoring-2024": ["ss", "sm"],
					"teleop-scoring-2024": ["ss", "as", "am", "as", "sa", "ts"],
					"notes": "decent defense and intake always worked smoothly\ncycles were relatively slow though"
				},
				"ratings": {
					"defense-skill": 3,
					"driver-skill": 3,
					"intake-consistency": 4,
					"speed": 2,
					"stability": 3
				},
				"timers": {
					"brick-time": 1500,
					"defense-time": 6745,
					"stage-time-2024": 12815
				}
		}
	]
}
'''