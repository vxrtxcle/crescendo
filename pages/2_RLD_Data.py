import streamlit as st
import streamlit as st
import pandas as pd
import requests
from pathlib import Path
st.subheader("RLD Data")
data_path = Path(__file__).parents[1] / "Data Set.csv"
df = pd.read_csv('Data Set.csv')
st.markdown("[To see the alliance comparison dashboard, click this link](https://view.reallifedata.net/dashboard/?vid=93)")
st.markdown("[To see other visualizations, click here](https://view.reallifedata.net/home/)")
st.markdown("[To access the editor, click here](https://editor.reallifedata.net/)")
team_number = st.selectbox("Select a team: ", df['team_#'], format_func=lambda x: f"{x}")
filtered_pit_data = df[df["team_#"] == team_number]
for x in range(len(filtered_pit_data['auto_leave'])):
    print(filtered_pit_data['auto_leave'][x])
    if filtered_pit_data['auto_leave'][x] == 'Yes':
        x = 2
    else:
        x = 0
st.table(filtered_pit_data[['match_#', 'auto_leave']])
