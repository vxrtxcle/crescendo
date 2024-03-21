import streamlit as st
import pandas as pd
import requests
from pathlib import Path
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

pit_data_path = Path(__file__).parents[1] / 'pit.csv'
pit_ftw_path = Path(__file__).parents[1] / 'pit-fort-worth.csv'
data_path = Path(__file__).parents[1] / "Data Set.csv"

pit_data = pd.read_csv('pit.csv')
pit_ftw_data = pd.read_csv('pit-fort-worth.csv')
dataset_data = pd.read_csv('Data Set.csv')

y = pit_ftw_data["Team Number (of the team you're scouting)"].unique()

team_number = st.selectbox("Select Team", y, format_func=lambda x: f"{x}")


if team_number:
    st.title("Team #: " + str(team_number))
