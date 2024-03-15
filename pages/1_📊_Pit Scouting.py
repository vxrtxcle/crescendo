import streamlit as st
import pandas as pd
import requests
from pathlib import Path
import os

pit_data_path = Path(__file__).parents[1] / 'pit.csv'
pit_ftw_path = Path(__file__).parents[1] / 'pit-fort-worth.csv'
data_path = Path(__file__).parents[1] / "Data Set.csv"

pit_data = pd.read_csv('pit.csv')
pit_ftw_data = pd.read_csv('pit-fort-worth.csv')
dataset_data = pd.read_csv('Data Set.csv')

y = pit_ftw_data["Team Number (of the team you're scouting)"].unique()

team_number = st.selectbox("Select Team", y, format_func=lambda x: f"{x}")
image_column_name = "Photo (clear view; no people blocking please; MAKE SURE THE ROBOT MATCHES WITH THE NUMBER YOU PUT ABOVE)"


st.subheader("Pit Scouting")
filtered_pit_data = pit_ftw_data[pit_ftw_data["Team Number (of the team you're scouting)"] == team_number]  # Placeholder for team selection, adapt if needed
st.write("General")
st.table(filtered_pit_data[["Height (from the ground) (in)", "Width (in respect to climb; without bumpers) (in)",
                                "Drivebase", "Programming Language", "Camera Usage? (to assist drivers)",
                                'Over/Under Bumper Ground Pickup']])
st.write("Auto")
st.table(filtered_pit_data[["Leave Zone Auto?", "Scoring Ability (in auto)"]])
st.write("TeleOP")
st.table(filtered_pit_data[["Scoring Preference (in teleop)","Scoring Ability (in teleop)","Pickup Ability", 'Pickup Preference']])
st.write("Abilities")
st.table(filtered_pit_data[['Can they score in trap?', 'Can they get onstage (hang)?']])
st.write("Comments")
st.table(filtered_pit_data[['Final Comments', 'Comments (about auto)', 'Comments?']])

df = pd.read_csv('pit-photos-fort-worth.csv')
image_column_name = "Photo (clear view; no people blocking please; MAKE SURE THE ROBOT MATCHES WITH THE NUMBER YOU PUT ABOVE)"

filtered_df = df[df["Team Number (OF THE TEAM YOU'RE TAKING THE PICTURE OF)"] == team_number]

if team_number:
    image_link = filtered_df[image_column_name].values[0]
    if len(image_link.split(',')) >= 2:
        for x in image_link.split(','):
            st.markdown("[View image of robot](" + x+ ")")
    else:
        st.markdown("[View image of robot](" + image_link + ")")

