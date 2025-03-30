import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from itertools import combinations

# def load_data(data):
#     return pd.read_csv(data)

# df = load_data("data/ff25test.csv")


url = "https://docs.google.com/spreadsheets/d/1Qk1A-UVgPKnoGDnP4ZNtri0ucLn-cf2hmiIv41LdLPE/edit?usp=sharing"

conn = st.connection("gsheets", type = GSheetsConnection)
dfLeaderboard = conn.read(spreadsheet = url, worksheet = "1405471253")
dfLeaderboard.index += 1
dfLeaderboard.index.name = "Rank"

dfPlayers = dfLeaderboard[['Player','Rating']].copy()

## 

def make_teams(activePlayers):
    players = activePlayers
    
    closest_difference = None
    all_players_set = set(players.keys())
    team_size = int(len(players)/2)
    
    for team_a in combinations(players.keys(), team_size):
        team_a_set = set(team_a)
        team_b_set = all_players_set - team_a_set
    
        team_a_total = sum([players[x] for x in team_a_set])
        team_b_total = sum([players[x] for x in team_b_set])
    
        score_difference = abs(team_a_total - team_b_total)
    
        if not closest_difference or score_difference < closest_difference:
            closest_difference = score_difference
            best_team_a = team_a_set     
            best_team_b = team_b_set  
    
    team1 = pd.DataFrame(list(best_team_a))
    team2 = pd.DataFrame(list(best_team_b))
    
    score1 = sum(players[x] for x in best_team_a)
    score2 = sum(players[x] for x in best_team_b)
    
    return team1, team2, score1, score2
    
def display_teams(team1, team2, score1, score2):
    st.header("Suggested teams")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Team 1")
        st.caption(f"Total rating: {score1}")
        st.dataframe(team1)
    with col2:
        st.subheader("Team 2")
        st.caption(f"Total rating: {score2}")
        st.dataframe(team2)
    st.divider()




    
##

def home_page():
    st.title("Leaderboard")
    
    # st.dataframe(df)
    
    st.dataframe(dfLeaderboard)
    
def match_page():
    st.title("Match History")
    
def matchmaking():
    st.title("Matchmaking tool")
    
    st.subheader("Players coming on Friday")
    
    allPlayerList = dfPlayers['Player'].tolist()
    
    activePlayers = st.multiselect(
        "Players coming",
        allPlayerList,
        [],
        )
    
    st.divider()
    
    st.write("We have " + str(len(activePlayers)) + " players coming:")
    st.session_state['activePlayers'] = activePlayers
    
    dfActive = dfPlayers[dfPlayers['Player'].isin(activePlayers)]
    playersToMatch = dict(zip(dfActive['Player'],dfActive['Rating']))
    
    st.dataframe(dfActive)
    
    st.divider()
    
    # team_size_label = "Players per team"
    # team_size = st.number_input(
    #     label = team_size_label,
    #     value = 5,
    #     min_value = 3,
    #     max_value = 6,
    #     step = 1,
    #     format = "%i",
    #     disabled=False,
    #     label_visibility = "visible")
    
    matchmaking_label = "Create teams"
    if st.button(
            label = matchmaking_label,
            type = "primary",
            use_container_width=False):
       team1, team2, score1, score2 = make_teams(playersToMatch)
       display_teams(team1, team2, score1, score2) 
        
        
        
    
    
leaderboard = st.Page(home_page, title = "Leaderboard", icon = ":material/leaderboard:")
matchHistory = st.Page(match_page, title = "Match History", icon = ":material/history:")
matchmaker = st.Page(matchmaking, title = "Matchmaking tool", icon = ":material/group:")


# Navbar
pg = st.navigation({"Ranking": [leaderboard],
                    "Tools": [matchmaker],
                    "Stats": [matchHistory]})

pg.run()

# st.sidebar.markdown("# This is an empty space across all pages")