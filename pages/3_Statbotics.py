import requests
import json

import statbotics
import streamlit as st
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
st.subheader("Statbotics")
sb = statbotics.Statbotics()
load_dotenv('.env')
tba_key = os.getenv('X_TBA_Auth_Key')
url = "https://www.thebluealliance.com/api/v3/event/2024txfor/teams/keys"
headers = {'X-TBA-Auth-Key': tba_key}
response = requests.get(url, headers)
req = response.json()
teams = []
for x in req:
    y = x.replace('frc','')
    teams.append(int(y))
teams.sort()
team_number = st.selectbox("Select Team", teams, format_func=lambda x: f"{x}")
if team_number:
    for x in sb.get_team_matches(team_number,2024):
        st.write(x)
    st.markdown("[To see more information about this team, click here](https://www.statbotics.io/team/" + str(int(team_number)) + ")")
    st.markdown("[To see more about the Fort Worth Event, click here](https://www.statbotics.io/event/2024txfor)")




