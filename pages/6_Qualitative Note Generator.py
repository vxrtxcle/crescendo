import requests
import re
import json
import streamlit as st
import os
from pathlib import Path
import pandas as pd
import time
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
dotenv_path = '.env'
load_dotenv(dotenv_path)
tba_key = os.getenv('X_TBA_Auth_Key')
scopes = os.getenv("SCOPES")
document_id = os.getenv("DOCUMENT_ID")

#pit_ftw_path = 'pit-fort-worth.csv'
#pit_data = pd.read_csv(pit_ftw_path)

#data_path = "Data Set.csv"
#dataset_data = pd.read_csv(data_path)

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
DOCUMENT_ID = document_id

url = "https://www.thebluealliance.com/api/v3/event/2024txcmp1/teams/keys"
headers = {'X-TBA-Auth-Key': tba_key}
response = requests.get(url, headers)
req = response.json()
teams2 = []
for x in req:
    y = x.replace('frc','')
    teams2.append(int(y))
teams2.sort()
for x in range(len(teams2)):
    teams2[x] = str(teams2[x]) + " - "
teams2.remove("2468 - ")

creds = None

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
        token.write(creds.to_json())

try:
    service = build("docs", "v1", credentials=creds)

    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    notes = ""
    for x in document.get('body')['content']:
        if x.get('paragraph') == None:
            continue
        else:
            z = x.get('paragraph').get('elements')[0].get('textRun').get('content')
            if z == '\n':
                continue
            else:
                #print(z)
                notes += z + '\n'


except HttpError as err:
    print(err)

parsed_values = teams2
temp_array = teams2
string_length = len(notes)
array_length = len(teams2)
i = 0
temp = teams2[0]
count = 0
team_notes = []
temp = ""
#st.write(notes)
for x in range(len(teams2)):
    y = notes.split(teams2[x])
    if x != len(teams2) - 1:
        #st.write(teams2[x])
        z = y[1].split(teams2[x+1])
        #st.write(z)
        team_notes.append(z[0])
    else:
        team_notes.append(y[1])

url = "https://www.thebluealliance.com/api/v3/event/2024txcmp1/teams/keys"
headers = {'X-TBA-Auth-Key': tba_key}
response = requests.get(url, headers)
req = response.json()
arr = []
for x in req:
    y = x.replace('frc','')
    arr.append(int(y))
arr.sort()
team_number = st.selectbox("Select Team", arr, format_func=lambda x: f"{x}")

if team_number:
    st.title("Team #" + str(team_number))
    st.write("Qualitative Notes for Matches")
    url = "https://www.thebluealliance.com/api/v3/team/" + "frc" + str(team_number) + "/event/2024txcmp1/matches/simple"
    response = requests.get(url, headers)
    req = response.json()
    matches = []
    for x in req:
        if str(x['comp_level']) == 'sf':
            matches.append(str(x['comp_level']) + "_" + str(x['set_number']) + "m" + str(x['match_number']))
            continue
        matches.append(str(x['comp_level']) + "_" + str(x['match_number']))
    match_number = st.selectbox("Select Match", matches, format_func=lambda x: f"{x}")
    if match_number:
        for x in req:
            if str(x['comp_level']) + "_" + str(x['match_number']) == match_number or str(x['comp_level']) + "_" + str(x['set_number']) + "m" + str(x['match_number']) == match_number:
                if str(x['comp_level']) + "_" + str(x['set_number']) + "m" + str(x['match_number']) == match_number:
                    st.write("Semis Match " + str(x['set_number']))
                elif x['comp_level'] == "f":
                    st.write("Finals Match " + str(x['match_number']))
                else:
                    st.write("Qualification Match " + str(x['match_number']))
                teams = x['alliances']['red']['team_keys'] + x['alliances']['blue']['team_keys']
                for y in x['alliances']['red']['team_keys']:
                    z = y.replace('frc','')
                    if z != "2689" and z != "2687" and z != "2468":
                        index = teams2.index(str(z) + " - ")
                        st.write(z + " - " + team_notes[index])
                    elif z == "2687" or z == "2689":
                        st.write(z + " - :)")
                    else:
                        continue
                for y in x['alliances']['blue']['team_keys']:
                    z = y.replace('frc','')
                    if z != "2689" and z != "2687" and z != "2468":
                        index = teams2.index(str(z) + " - ")
                        st.write(z + " - " + team_notes[index])
                    elif z == "2687" or z == "2689":
                        st.write(z + " - :)")
                    else:
                        continue

if team_number:
    st.title("Team #" + str(team_number))
    key = str(team_number) + " - "
    index = teams2.index(key)
    st.write(team_notes[index])


