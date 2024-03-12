import streamlit as st
import pandas as pd
import requests
from pathlib import Path

pit_data_path = Path(__file__).parents[1] / 'pit.csv'
data_path = Path(__file__).parents[1] / "Data Set.csv"
pit_data = pd.read_csv('pit.csv')
dataset_data = pd.read_csv('Data Set.csv')
team_number = st.selectbox("Select Team", pit_data["Team Number"].unique(), format_func=lambda x: f"{x}")
filtered_data = dataset_data[dataset_data["team_#"] == team_number]

if filtered_data.empty:
    st.write("")
else:
    st.write(filtered_data.to_string(index=False))

st.subheader("Pit Scouting")
filtered_pit_data = pit_data[pit_data["Team Number"] == team_number]  # Placeholder for team selection, adapt if needed
st.write("General")
st.table(filtered_pit_data[["Height (in)", "Width (in)",
                                "Drivebase", "Programming Language", "Camera Usage?",
                                'Over/Under Bumper Ground Pickup', 'Over-Bumper or Under-Bumper Ground Pickup']])
st.write("Auto")
st.table(filtered_pit_data[["Leave Zone", "Scoring Ability", ]])
st.write("TeleOP")
st.table(filtered_pit_data[["Scoring Preference", "Pickup Ability", 'Pickup Preference']])
st.write("Abilities")
st.table(filtered_pit_data[['Can they score in trap?', 'Can they get onstage?']])
st.write("Comments")
st.table(filtered_pit_data[['Final Comments', 'Comments (about auto)', 'Comments?']])

