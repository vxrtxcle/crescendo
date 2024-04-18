import statbotics
import streamlit as st
sb = statbotics.Statbotics()
print(sb.get_team_matches(9692,2024))
print(sb.get_match('2024txfor_f1m1'))