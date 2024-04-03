import streamlit as st
import pandas as pd
import requests
import json
from dotenv import load_dotenv
import os
dotenv_path = '.env'
load_dotenv(dotenv_path)
tba_key = os.getenv('X_TBA_Auth_Key')
from pathlib import Path
st.title("RLD Data")
url = "https://www.thebluealliance.com/api/v3/event/2024txfor/teams/keys"
headers = {'X-TBA-Auth-Key': tba_key}
response = requests.get(url, headers)
req = response.json()
teams = []
for x in req:
    y = x.replace('frc','')
    teams.append(int(y))
teams.sort()
options = st.multiselect("What team are you selecting?", teams)

edict = {'Match Number': [], 'Auto Speaker': [], 'Auto Speaker Miss': [], 'Tele Speaker': [], "Tele Speaker Miss": [], 'Tele Amp': [], 'Tele Amp Miss': [], 'Drops': [], 'Endgame Stage': [], 'DC': []}
if options:
    for x in options:
        edict = {'Match Number': [], 'Auto Speaker': [], 'Auto Speaker Miss': [], 'Tele Speaker': [],
                 "Tele Speaker Miss": [], 'Tele Amp': [], 'Tele Amp Miss': [], 'Drops': [], 'Endgame Stage': [],
                 'DC': [], 'Avg': 0, 'Min': 0, 'Max': 0}
        with open("Fort Worth.json", 'r') as f:
            g = json.load(f)
            for y in g:
                if int(y['team_#']) == int(x):
                    edict['Match Number'].append(y['match_#'])
                    edict['Auto Speaker'].append(y['auto_spk_scored'])
                    edict['Auto Speaker Miss'].append(y['auto_spk_miss'])
                    if isinstance(y['tele_spk_scored'], list):
                        edict['Tele Speaker'].append(len(y['tele_spk_scored']))
                    elif isinstance(y['tele_spk_scored'], int):
                        edict['Tele Speaker'].append(1)
                    else:
                        edict['Tele Speaker'].append(0)
                    if isinstance(y['tele_spk_miss'], list):
                        edict['Tele Speaker Miss'].append(len(y['tele_spk_miss']))
                    elif isinstance(y['tele_spk_miss'], int):
                        edict['Tele Speaker Miss'].append(1)
                    else:
                        edict['Tele Speaker Miss'].append(0)
                    if isinstance(y['tele_amp_scored'], list):
                        edict['Tele Amp'].append(len(y['tele_amp_scored']))
                    elif isinstance(y['tele_amp_scored'], int):
                        edict['Tele Amp'].append(1)
                    else:
                        edict['Tele Amp'].append(0)
                    if isinstance(y['tele_amp_miss'], list):
                        edict['Tele Amp Miss'].append(len(y['tele_amp_miss']))
                    elif isinstance(y['tele_amp_miss'], int):
                        edict['Tele Amp Miss'].append(1)
                    else:
                        edict['Tele Amp Miss'].append(0)
                    edict['Drops'].append(y['Drops'])
                    if y['endgame_stage_actions'] == 'None':
                        count = (y["endgame_trap_scored"] + y['tele_trap_scored']) * 5
                        edict['Endgame Stage'].append(count)
                    elif y['endgame_stage_actions'] == 'Onstage':
                        count = (y["endgame_trap_scored"] + y['tele_trap_scored']) * 5
                        edict['Endgame Stage'].append(count + 3)
                    elif y['endgame_stage_actions'] == 'Onstage Spotlit':
                        count = (y["endgame_trap_scored"] + y['tele_trap_scored']) * 5
                        edict['Endgame Stage'].append(count + 4)
                    elif y['endgame_stage_actions'] == 'Park':
                        count = (y["endgame_trap_scored"] + y['tele_trap_scored']) * 5
                        edict['Endgame Stage'].append(count + 1)
                    if y['disconnect'] == 'Yes':
                        edict['DC'].append(1)
                    else:
                        edict['DC'].append(0)

            for x in range(len(edict.keys())-3):
                total = 0
                klist = list(edict.keys())
                for y in edict[klist[x]]:
                    if y == 'Match Number':
                        continue
                    else:
                        min = 9999
                        max = -9999
                        if y < min:
                            min = y
                        elif y > max:
                            max = y
                        total += y
                avg = total / len(edict[klist[x]])
                edict['Avg'] = avg
                edict['Max'] = max
                edict['Min'] = min
            for y in g:
                if int(y['team_#']) == int(x):
                    edict['Endgame Stage'] = []
                    edict['DC'] = []
                    edict['DC'].append(y['disconnect'])
                    edict['Endgame Stage'].append(y['endgame_stage_actions'])

        st.subheader("Team #" + str(x))
        match_table = pd.DataFrame.from_dict(edict)
        st.table(match_table)
