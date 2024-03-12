import json

import pandas as pd
import streamlit as st
import requests
from dotenv import load_dotenv
import os
load_dotenv()
from googleapiclient.discovery import build
access_env = os.getenv('access_token')
df = pd.read_csv('photos.csv')
image_column_name = "Photo (clear view; no people blocking please)"
team_numbers = df["Team Number"].unique().tolist()

selected_team_number = st.selectbox("Choose Team Number:", team_numbers)

filtered_df = df[df["Team Number"] == selected_team_number]

if selected_team_number:
    image_link = filtered_df[image_column_name].values[0]

if ',' in image_link:
    file_ids = image_link.split(', ')
    for x in file_ids:
        y = x.split('=')
        print(y[1])
        download_url = f"https://www.googleapis.com/drive/v3/files/{y[1]}?alt=media&access_token={access_env}"
        image_response = requests.get(download_url)
        if image_response.status_code == 200:
            st.image(image_response.content, width=600)
        else:
            st.error(f"Error downloading image: {image_response.status_code}")
else:
    file_id = image_link.split('=')
    print(file_id[1])
    download_url = f"https://www.googleapis.com/drive/v3/files/{file_id[1]}?alt=media&access_token={access_env}"
    image_response = requests.get(download_url)
    if image_response.status_code == 200:
        st.image(image_response.content, width=600)
    else:
        st.error(f"Error downloading image: {image_response.status_code}")
'''
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