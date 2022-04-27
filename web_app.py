import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
# import matplotlib.pyplot as plt
from soccerplots.radar_chart import Radar

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="ISL 2021-22", page_icon=":soccer:", layout="wide")

@st.cache
def get_data():
    df = pd.read_csv('ISL_league_stage.csv')
    return df

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
        a = a - (a*.25)

        b = max(df[params][x])
        b = b + (b*0.25)

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
                  range_fontsize=8, 
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

color_1 = st.sidebar.color_picker('Pick Color for team 1', '#00f900')
color_2 = st.sidebar.color_picker('Pick Color for team 2', '#00f999')

df_team_selection = df.query("team == @team")

st.sidebar.header("Please select the parameters (optimum value 9):")
params = st.sidebar.multiselect(
    "Select params:",
    options=df.columns,
    default = ['team','goals','xG','goals_conceded','xGA','shots',
               'shots_against','xPoints','xG_per_shot','xGA_per_shot']
)

df_param_selection = df_team_selection[params]
# ---- MAINPAGE ----
st.title(":bar_chart: ISL 2021-22 Team Comparision App")
st.markdown("##")
st.dataframe(df_team_selection)

st.title(":dart: Radar Plot")
st.write('Right click and press "Save image as..." to download image')
st.markdown("""---""")
col = st.columns(1)
st.pyplot(fig=make_radar(df_team_selection,params))
st.dataframe(get_data())
st.write("Made by Joyan Bhathena, joyansbhathena@gmail.com")
