'''
import streamlit as st
import pandas as pd
import requests
import os

# read in data
df = pd.read_json('comp.json')

#for x in df.head():
 #   print(x)

# Select the column to print
#selected_column = st.multiselect("Select Column", df.columns)

# Print the selected column
#st.write(df[selected_column])
#print(len(list(df.head())))

pit_df = pd.read_csv('pit.csv')
grouped_data = pit_df.groupby("Team Number")

# Extract unique team names
team_names = list(grouped_data.groups.keys())

# Multiselect widget with options grouped by "Team Name"
selected_teams = st.select(
    "Select A Team", team_names, format_func=lambda x: f"Team: {x}"
)
for team_name, team_data in grouped_data:
  if team_name in selected_teams:
    st.write(f"## Team: {team_name}")
    st.dataframe(team_data)
# determine team numbers
seen = set()
unique_data = []
for item in list(df['team_#']):
    if item not in seen:
      seen.add(item)
      unique_data.append(item)
url = "https://www.thebluealliance.com/api/v3/event/2024txwac/teams/keys"
headers = {'X-TBA-Auth-Key': tba_key}
response = requests.get(url, headers)
req = response.json()
teams = []
for x in req:
    y = x.replace('frc', '')
    teams.append(int(y))
z = list(set(teams).symmetric_difference(set(unique_data)))
a = list(set(teams).symmetric_difference(set(unique_data)))
for x in range(0,3):
    if z[x] == 3082:
        a[x] = 3802
    elif z[x] == 8764:
        a[x] = 8769
    elif z[x] == 6376:
        a[x] = 6377
for x in z:
    unique_data.remove(x)
for y in a:
    unique_data.append(y)
print(unique_data)


# Qual data can be manually put in from the doc
#df['team_#'] = unique_data
st.title("Competition Data")
team = st.multiselect("Choose teams: ", unique_data)
team_df = df.groupby("team_#")
if team:
    filtered_data = df.get(team)
    st.write(f"Statistics for Team {team[0]}:")
    st.dataframe(filtered_data.describe())
else:
    st.write("Select a team number")



'''


import pandas as pd
import streamlit as st
st.title("Team Dashboard")
st.write("Hello, welcome to the team dashboard!")
st.write("Select a team on the sidebar and travel throughout the pages to get started!")
