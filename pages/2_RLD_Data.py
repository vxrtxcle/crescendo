import streamlit as st
import pandas as pd
import requests
import json
from dotenv import load_dotenv
import os
from decimal import Decimal
dotenv_path = '.env'
load_dotenv(dotenv_path)
tba_key = os.getenv('X_TBA_Auth_Key')
from pathlib import Path
st.title("RLD Data")
url = "https://www.thebluealliance.com/api/v3/event/2024txcmp1/teams/keys"
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
                 'DC': [], 'Rings Fed': [], 'Effective Cycles': []}
        with open("State.json", 'r') as f:
            g = json.load(f)
            for y in g:
                if int(y['team_#']) == int(x):
                    edict['Match Number'].append(y['match_#'])
                    edict['Auto Speaker'].append(y['auto_spk_scored'])
                    edict['Auto Speaker Miss'].append(y['auto_spk_miss'])
                    if isinstance(y['tele_spk_scored'], list):
                        edict['Tele Speaker'].append(len(y['tele_spk_scored']))
                        spk_score = len(y['tele_spk_scored'])
                    elif isinstance(y['tele_spk_scored'], int):
                        edict['Tele Speaker'].append(1)
                        spk_score = 1
                    else:
                        edict['Tele Speaker'].append(0)
                        spk_score = 0
                    if isinstance(y['tele_spk_miss'], list):
                        edict['Tele Speaker Miss'].append(len(y['tele_spk_miss']))
                        spk_miss = len(y['tele_spk_miss'])
                    elif isinstance(y['tele_spk_miss'], int):
                        edict['Tele Speaker Miss'].append(1)
                        spk_miss = 1
                    else:
                        edict['Tele Speaker Miss'].append(0)
                        spk_miss = 0
                    if isinstance(y['tele_amp_scored'], list):
                        edict['Tele Amp'].append(len(y['tele_amp_scored']))
                        amp_score = len(y['tele_amp_scored'])
                    elif isinstance(y['tele_amp_scored'], int):
                        edict['Tele Amp'].append(1)
                        amp_score = 1
                    else:
                        edict['Tele Amp'].append(0)
                        amp_score = 0
                    if isinstance(y['tele_amp_miss'], list):
                        edict['Tele Amp Miss'].append(len(y['tele_amp_miss']))
                        amp_miss = len(y['tele_amp_miss'])
                    elif isinstance(y['tele_amp_miss'], int):
                        edict['Tele Amp Miss'].append(1)
                        amp_miss = 1
                    else:
                        edict['Tele Amp Miss'].append(0)
                        amp_miss = 0
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
                    if y['tele_pass_source'] == None and y['tele_pass_midfield'] == None:
                        edict['Rings Fed'].append(0)
                        tele_pass = 0
                    elif y['tele_pass_source'] == None and y['tele_pass_midfield'] != None:
                        if isinstance(y['tele_pass_midfield'], int):
                            edict['Rings Fed'].append(1)
                            tele_pass = 1
                        else:
                            edict['Rings Fed'].append(len(y['tele_pass_midfield']))
                            tele_pass = len(y['tele_pass_midfield'])
                    elif y['tele_pass_midfield'] == None and y['tele_pass_source'] != None:
                        if isinstance(y['tele_pass_source'], int):
                            edict['Rings Fed'].append(1)
                            tele_pass = 1
                        else:
                            edict['Rings Fed'].append(len(y['tele_pass_source']))
                            tele_pass = len(y['tele_pass_source'])
                    else:
                        tele_pass = 0
                        if isinstance(y['tele_pass_source'], int):
                            tele_pass += 1
                        else:
                            tele_pass += len(y['tele_pass_source'])
                        if isinstance(y['tele_pass_midfield'], int):
                            tele_pass += 1
                        else:
                            tele_pass += len(y['tele_pass_midfield'])
                        edict['Rings Fed'].append(tele_pass)
                    edict['Effective Cycles'].append(tele_pass+amp_score+spk_score)
        for key, values in edict.items():
            min_val = min(values)
            max_val = max(values)
            avg_val = sum(values) / len(values)
            values.extend([min_val, max_val, avg_val])
        st.subheader("Team #" + str(x))
        match_table = pd.DataFrame.from_dict(edict)
        st.table(match_table)
        st.write("The last three rows are minimum, maximum, and average respectively")
        st.write("For endgame stage, 4 is onstage spotlit, 3 is onstage, 1 is park, and 5 points for a trap")
