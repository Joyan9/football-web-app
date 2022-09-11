import streamlit as st
import pandas as pd
from soccerplots.radar_chart import Radar

st.title(":dart: Radar Charts")

@st.cache
def get_data():
    df = pd.read_csv('ISL_league_stage.csv')
    return df

def convert_df(df):
     return df.to_csv().encode('utf-8')

def make_radar(df,params,color_1='red',color_2='white'):
    df.reset_index(inplace=True)
    ranges = []
    params = params[1:]
    a_values = []
    b_values = []
    # Team_name_1 = df.iloc[0][0]
    # Team_name_2 = df.iloc[1][0]

    for x in params:
        a = min(df[params][x])
        a = a - (a*0.15)

        b = max(df[params][x])
        b = b + (b*0.15)

        ranges.append((a,b))

    for x in range(len(df['team'])):
        if df['team'][x] == df['team'][0]:
            a_values = df.iloc[x].values.tolist()
        if df['team'][x]== df['team'][1]:
            b_values = df.iloc[x].values.tolist()

    a_values = a_values[2:]
    b_values = b_values[2:]

    values = [a_values,b_values]


    title = dict(
    title_name=df['team'][0],
    title_color = color_1,
    title_name_2= df['team'][1],
    title_color_2 = color_2,
    title_fontsize = 18)

    endnote = '@BhathenaJoyan\ndata via Fotmob.com'
    radar = Radar(background_color='#000000', 
                  patch_color='#000000', 
                  fontfamily='Liberation Serif', 
                  label_fontsize=15, 
                  range_fontsize=7, 
                  label_color='#FFFFFF', 
                  range_color='#FFFFFF')

    fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,
                             radar_color=[color_1,color_2],
                             alphas=[.75,.60],title=title,endnote=endnote,
                             compare=True)

    
    return fig




df = get_data()
#----SIDEBAR----
st.sidebar.header("Please select 2 teams for comparision:")
team = st.sidebar.multiselect(
    "Select teams:",
    options=df["team"].unique(),
    default=['Hyderabad FC','ATK Mohun Bagan FC']
)
st.sidebar.header("Team 1 will be the team which comes first alphabetically, refer data table for reference")
color_1 = st.sidebar.color_picker('Pick Color for team 1', '#ffffff')
color_2 = st.sidebar.color_picker('Pick Color for team 2', '#ffff00')


df_team_selection = df.query("team == @team")

st.sidebar.header("Please select the parameters (optimum value 9):")
params = st.sidebar.multiselect(
    "Select params (Please do not unselect 'team'):",
    options=df.columns,
    default = ['team','goals','xG','goals_conceded','xGA','shots',
               'shots_against','xPoints','xG_Open_Play','xG_Set_Play']
)

df_param_selection = df_team_selection[params]
# ---- MAINPAGE ----
#st.title(":bar_chart: ISL 2021-22 Team Comparision App")
st.markdown("##")
st.dataframe(df_team_selection)

#st.title(":dart: Radar Plot")
st.write('Right click and press "Save image as..." to download image')
col = st.columns(1)
if len(team) == 2:
    st.pyplot(fig=make_radar(df_team_selection,params,color_1,color_2))

st.title("Full database")
st.dataframe(df)

st.write("Made by Joyan Bhathena, joyansbhathena@gmail.com")