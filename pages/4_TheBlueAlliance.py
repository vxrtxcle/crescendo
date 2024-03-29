import streamlit as st
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import requests
load_dotenv()
tba_key = os.getenv('X_TBA_Auth_Key')
os.write(1,f'{tba_key}'.encode())
st.subheader("The Blue Alliance")
pit_data_path = Path(__file__).parents[1] / 'pit-fort-worth.csv'
pit_data = pd.read_csv(pit_data_path)
team_number = st.selectbox("Select Team", pit_data["Team Number (of the team you're scouting)"].unique(), format_func=lambda x: f"{x}")
if team_number:
    st.markdown("[To see more information about this team, click here](https://www.thebluealliance.com/team/" + str(team_number) + ")")
    st.markdown("[To see more about the Fort Worth Event, click here](https://www.thebluealliance.com/event/2024txfor)")
