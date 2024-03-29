import streamlit as st
import pandas as pd
import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()
tba_key = os.getenv('X_TBA_Auth_Key')
from pathlib import Path
st.title("RLD Data")
url = "https://www.thebluealliance.com/api/v3/event/2024txfor/teams/keys"
headers = {'X-TBA-Auth-Key': tba_key}
response = requests.get(url, headers)
req = response.json()
os.write(1, f'{req}'.encode())
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
                 'DC': []}
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
                    edict['Endgame Stage'].append(y['endgame_stage_actions'])
                    edict['DC'].append(y['disconnect'])
        st.subheader("Team #" + str(x))
        match_table = pd.DataFrame.from_dict(edict)
        st.table(match_table)
