import streamlit as st
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import requests
load_dotenv('.env')
tba_key = os.getenv('X_TBA_Auth_Key')
st.subheader("The Blue Alliance")
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
    st.markdown("[To see more information about this team, click here](https://www.thebluealliance.com/team/" + str(team_number) + ")")
    st.markdown("[To see more about the Fort Worth Event, click here](https://www.thebluealliance.com/event/2024txfor)")
