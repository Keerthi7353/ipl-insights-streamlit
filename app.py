import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


st.set_page_config(layout="wide", page_title="IPL Data Dashboard")

matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

st.title("🏏 IPL Data Analytics Dashboard")

st.header("Overall Insights")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Matches", matches.shape[0])
with col2:
    st.metric("Total Seasons", matches["season"].nunique())
with col3:
    st.metric("Total Teams", pd.concat([matches['team1'], matches['team2']]).nunique())
with col4:
    st.metric("Player of the Match Awards", matches['player_of_match'].nunique())




st.subheader("Top Run Scorer")
top_scorer = deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(1)
batter_name = top_scorer.index[0]
total_runs = top_scorer.iloc[0]

st.metric("Top Run Scorer", f"{batter_name}", f"{total_runs} Runs")








st.subheader("Most Sixes by a Player")


sixes = deliveries[deliveries['batsman_runs'] == 6]


most_sixes = sixes.groupby('batter').size().sort_values(ascending=False).head(1)

six_hitter_name = most_sixes.index[0]
six_count = most_sixes.iloc[0]

st.metric("Most Sixes", six_hitter_name, f"{six_count} Sixes")





st.subheader("Top Wicket Taker")

wickets = deliveries[deliveries['dismissal_kind'].notnull()]

top_wicket_taker = wickets.groupby('bowler').size().sort_values(ascending=False).head(1)

bowler_name = top_wicket_taker.index[0]
wicket_count = top_wicket_taker.iloc[0]


st.metric("Most Wickets", bowler_name, f"{wicket_count} Wickets")













st.subheader("Most Match Wins")
team_wins = matches['winner'].value_counts().head(10)
st.bar_chart(team_wins)

st.subheader("Top Run Scorers")
top_runs = deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_runs)

st.subheader("Top Wicket Takers")
wickets = deliveries[deliveries['dismissal_kind'].notnull()]
top_wickets = wickets['bowler'].value_counts().head(10)
st.bar_chart(top_wickets)


if 'win_by_wickets' in matches.columns:
    result = matches['win_by_wickets'].apply(lambda x: 'Chasing' if x > 0 else 'Batting First')
    result_counts = result.value_counts()
    st.subheader("Batting First vs Chasing")
    st.bar_chart(result_counts)
else:
    st.warning("This dataset does not contain information about 'win_by_runs' or 'win_by_wickets', so batting/chasing stats cannot be displayed.")

st.subheader("Head-to-Head Comparison Between Teams")

teams = sorted(matches['team1'].unique())
team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", teams)

if team1 != team2:
    head_to_head = matches[((matches['team1'] == team1) & (matches['team2'] == team2)) | 
                           ((matches['team1'] == team2) & (matches['team2'] == team1))]
    
    if not head_to_head.empty:
        win_counts = head_to_head['winner'].value_counts()
        st.bar_chart(win_counts)
    else:
        st.info("No matches played between selected teams.")

st.subheader("Win Trend Based on Toss Decision")

if 'toss_decision' in matches.columns and 'winner' in matches.columns:
    toss_win = matches[matches['toss_winner'] == matches['winner']]
    toss_loss = matches[matches['toss_winner'] != matches['winner']]
    
    toss_stats = pd.DataFrame({
        'Result': ['Won After Toss', 'Lost After Toss'],
        'Matches': [toss_win.shape[0], toss_loss.shape[0]]
    })
    st.bar_chart(toss_stats.set_index('Result'))
else:
    st.warning("Toss data is missing from the dataset.")

st.subheader("Top Venues by Match Count")

venue_counts = matches['venue'].value_counts().head(10)
st.bar_chart(venue_counts)

st.subheader("Venue-wise Win Distribution")

selected_venue = st.selectbox("Select Venue for Win Distribution", matches['venue'].dropna().unique())

venue_data = matches[matches['venue'] == selected_venue]
venue_wins = venue_data['winner'].value_counts()
st.bar_chart(venue_wins)

