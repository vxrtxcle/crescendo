import requests
import re
import json
import streamlit as st
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path

load_dotenv()
tba_key = os.getenv('X_TBA_Auth_Key')
scopes = os.getenv("SCOPES")
document_id = os.getenv("DOCUMENT_ID")

pit_data_path = 'pit.csv'
pit_ftw_path = 'pit-fort-worth.csv'
data_path = "Data Set.csv"

pit_data = pd.read_csv(pit_data_path)
pit_ftw_data = pd.read_csv(pit_ftw_path)
dataset_data = pd.read_csv(data_path)

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
DOCUMENT_ID = document_id

url = "https://www.thebluealliance.com/api/v3/event/2024txfor/teams/keys"
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
teams2.remove("2687 - ")
teams2.remove("2689 - ")

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
                notes += z


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
for x in range(len(teams2)):
    y = notes.split(teams2[x])
    if x != len(teams2) - 1:
        z = y[1].split(teams2[x+1])
        team_notes.append(z[0])
    else:
        team_notes.append(y[1])


team_number = st.text_input("What team are you selecting?")

if team_number:
    st.title("Team #: " + str(int(team_number)))
    url = "https://www.thebluealliance.com/api/v3/team/" + "frc" + str(int(team_number)) + "/events/simple"
    headers = {'X-TBA-Auth-Key': tba_key}
    response = requests.get(url, headers)
    req = response.json()
    events = []
    for x in req:
        if x['year'] == 2024:
            events.append(str(x['year']) + str(x['event_code']))
    st.write("Qualitative Notes for Matches")
    event = st.selectbox("Select an event: ", events, format_func=lambda x: f"{x}")
    url = "https://www.thebluealliance.com/api/v3/team/" + "frc" + str(int(team_number)) + "/event/" + event + "/matches/simple"
    response = requests.get(url, headers)
    req = response.json()
    for x in req:
        st.write("Match " + str(x['comp_level']) + "_" + str(x['match_number']))
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




