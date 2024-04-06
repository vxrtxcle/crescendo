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
                 'DC': [], 'Rings Fed': []}
        with open("State.json", 'r') as f:
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
                    if y['tele_pass_source'] == None and y['tele_pass_midfield'] == None:
                        edict['Rings Fed'].append(0)
                    elif y['tele_pass_source'] == None and y['tele_pass_midfield'] != None:
                        if isinstance(y['tele_pass_midfield'], int):
                            edict['Rings Fed'].append(1)
                        else:
                            edict['Rings Fed'].append(len(y['tele_pass_midfield']))
                    elif y['tele_pass_midfield'] == None and y['tele_pass_source'] != None:
                        if isinstance(y['tele_pass_source'], int):
                            edict['Rings Fed'].append(1)
                        else:
                            edict['Rings Fed'].append(len(y['tele_pass_source']))
                    else:
                        temp7 = 0
                        if isinstance(y['tele_pass_source'], int):
                            temp7 += 1
                        else:
                            temp7 += len(y['tele_pass_source'])
                        if isinstance(y['tele_pass_midfield'], int):
                            temp7 += 1
                        else:
                            temp7 += len(y['tele_pass_midfield'])
                        edict['Rings Fed'].append(temp7)

        st.subheader("Team #" + str(x))
        match_table = pd.DataFrame.from_dict(edict)
        st.table(match_table)
        st.write("For endgame stage, 4 is onstage spotlit, 3 is onstage, 1 is park, and 5 points for a trap")
