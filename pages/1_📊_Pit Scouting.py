import streamlit as st
import pandas as pd
import requests
from pathlib import Path
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from PIL import Image

pit_data_path = Path(__file__).parents[1] / 'pit.csv'
pit_ftw_path = Path(__file__).parents[1] / 'pit-fort-worth.csv'
data_path = Path(__file__).parents[1] / "Data Set.csv"

pit_data = pd.read_csv('pit.csv')
pit_ftw_data = pd.read_csv('pit-fort-worth.csv')
dataset_data = pd.read_csv('Data Set.csv')

y = pit_ftw_data["Team Number (of the team you're scouting)"].unique()
y.sort()

team_number = st.selectbox("Select Team", y, format_func=lambda x: f"{x}")
# Make it select for a tournament
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

# Make image viewable
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
DOCUMENT_ID = ""
creds = None

if os.path.exists("token2.json"):
    creds = Credentials.from_authorized_user_file("token2.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

    with open("token2.json", "w") as token:
        token.write(creds.to_json())

try:
    service = build("drive", "v3", credentials=creds)
    if team_number:
        image_link = filtered_df[image_column_name].values[0]
        if len(image_link.split(',')) >= 2:
            for x in image_link.split(','):
                file_id = x.split('id=')[-1]
                file = service.files().get(fileId=file_id, fields='id, name, mimeType').execute()
                if file['mimeType'].startswith('image/'):
                    image_data = service.files().get_media(fileId=file_id).execute()
                    team_string = "Team #" + str(team_number)
                    image = st.image(image_data, caption=team_string)

                else:
                    st.error("The selected file is not an image.")
        else:
            file_id = image_link.split('id=')[-1]
            file = service.files().get(fileId=file_id, fields='id, name, mimeType').execute()
            if file['mimeType'].startswith('image/'):
                image_data = service.files().get_media(fileId=file_id).execute()
                team_string = "Team #" + str(team_number)
                image = st.image(image_data, caption=team_string)
            else:
                st.error("The selected file is not an image.")

except HttpError as err:
    print(err)






