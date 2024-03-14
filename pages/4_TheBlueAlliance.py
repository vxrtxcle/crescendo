import statbotics
import statbotics as sb
import streamlit as st
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import requests
load_dotenv()
tba_key = os.getenv('X_TBA_Auth_Key')

st.subheader("The Blue Alliance")
pit_data_path = Path(__file__).parents[1] / 'pit.csv'
pit_data = pd.read_csv(pit_data_path)
team_number = st.selectbox("Select Team", pit_data["Team Number"].unique(), format_func=lambda x: f"{x}")
if team_number:
    st.markdown("[To see more information about this team, click here](https://www.thebluealliance.com/team/" + str(team_number) + ")")
    st.markdown("[To see more about the Fort Worth Event, click here](https://www.thebluealliance.com/event/2024txfor)")
