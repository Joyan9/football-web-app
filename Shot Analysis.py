import streamlit as st
from mplsoccer import VerticalPitch
from statsbombpy import sb
st.title("Shot Analysis")

@st.experimental_memo
def get_teams_name():
    # get match teams name
    matches = sb.matches(competition_id = 1238, season_id = 108)
    teams = matches.home_team.unique()
    return teams

def get_events(home_team, away_team):
    matches = sb.matches(competition_id = 1238, season_id = 108)
    match_id = matches[(matches.home_team == home_team)&(matches.away_team == away_team)].match_id.values[0]
    events = sb.events(match_id = match_id)
    return events

def get_shot_df(home_team, away_team, team_req):
    events = get_events(home_team, away_team)
    if team_req == 'home':
        team_name = home_team
    else:
        team_name = away_team
    
    shots_team_name = events[(events.type == 'Shot') & (events.team == team_name)].copy()
    shots_team_name = shots_team_name[['location','player', 'player_id','shot_end_location',
                                       'shot_freeze_frame', 'shot_outcome','shot_statsbomb_xg']]
    x_coordinates,y_coordinates = [],[]
    for i in range(len(shots_team_name)):
        x_coordinates.append(shots_team_name['location'].iloc[i][0])
        y_coordinates.append(shots_team_name['location'].iloc[i][1])
        
    shot_end_x_coordinates,shot_end_y_coordinates = [],[]
    for i in range(len(shots_team_name)):
        shot_end_x_coordinates.append(shots_team_name['shot_end_location'].iloc[i][0])
        shot_end_y_coordinates.append(shots_team_name['shot_end_location'].iloc[i][1])

    shots_team_name['x'], shots_team_name['y'] = x_coordinates, y_coordinates
    shots_team_name['end_x'], shots_team_name['end_y'] = shot_end_x_coordinates, shot_end_y_coordinates
    
    df_goals_team_name = shots_team_name[shots_team_name.shot_outcome == 'Goal'].copy()
    df_non_goal_shots_team_name = shots_team_name[shots_team_name.shot_outcome != 'Goal'].copy()
    
    return df_goals_team_name, df_non_goal_shots_team_name

def shot_map(home_team, away_team, team_req):
    goals_df, no_goals_df = get_shot_df(home_team, away_team, team_req)
    if team_req == 'home':
        team_name = home_team
    else:
        team_name = away_team
    pitch = VerticalPitch(pitch_color="grass",pad_bottom=0.5,  # pitch extends slightly below halfway line
                          half=True,  # half of a pitch
                          goal_type='box',
                          goal_alpha=0.8) 
    fig, ax = pitch.draw(figsize=(12, 10))
    # plot non-goal shots with hatch
    sc1 = pitch.scatter(no_goals_df.x, no_goals_df.y,
                        # size varies between 100 and 1900 (points squared)
                        s=(no_goals_df.shot_statsbomb_xg * 1900) + 100,
                        edgecolors='#600000',  # give the markers a charcoal border
                        c='None',  # no facecolor for the markers
                        hatch='///',  # the all important hatch (triple diagonal lines)
                        # for other markers types see: https://matplotlib.org/api/markers_api.html
                        marker='o',
                        ax=ax)

    # plot goal shots with a color
    sc2 = pitch.scatter(goals_df.x, goals_df.y,
                        # size varies between 100 and 1900 (points squared)
                        s=(goals_df.shot_statsbomb_xg * 1900) + 100,
                        edgecolors='gray',  # give the markers a charcoal border
                        c='orange',  # color for scatter in hex format
                        # for other markers types see: https://matplotlib.org/api/markers_api.html
                        marker='football',
                        ax=ax)

    txt = ax.text(x=40, y=128, s=f'{home_team} versus {away_team} \n {team_name} shots',
                  size=30, va='center', ha='center')





teams = get_teams_name()
#----SIDEBAR----
st.sidebar.header("First Select Home Team and then Select Away team")
teams = st.sidebar.multiselect(
    "Select teams (max 2):",
    options=teams,
    default = ['Goa','Mumbai City']
)
home_team, away_team = teams[0], teams[1]
st.sidebar.write("Home Team --> ",home_team)
st.sidebar.write("Away Team --> ",away_team)   
team_req = st.radio("Home or Away", options = ['home','away'])

col = st.columns(1)
if len(teams) == 2:
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(fig=shot_map(home_team, away_team, team_req))

st.write("Made by Joyan Bhathena, joyansbhathena@gmail.com")