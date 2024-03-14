import requests
import json
import streamlit as st
import os
from pathlib import Path
import pandas as pd
st.subheader("Statbotics")
pit_data_path = Path(__file__).parents[1] / 'pit.csv'
print(pit_data_path)
pit_data = pd.read_csv(pit_data_path)
team_number = st.selectbox("Select Team", pit_data["Team Number"].unique(), format_func=lambda x: f"{x}")
if team_number:
    st.markdown("[To see more information about this team, click here](https://www.statbotics.io/team/" + str(team_number))
    st.markdown("[To see more about the Fort Worth Event, click here](https://www.statbotics.io/event/2024txfor)")




