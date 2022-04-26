import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
# import matplotlib.pyplot as plt
from soccerplots.radar_chart import Radar

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="ISL 2021-22 Dashboard", page_icon=":soccer:", layout="wide")

@st.cache
def get_data():
    df = pd.read_csv('C:/Users/joyan/ISL_league_stage.csv')
    return df

def make_radar(df,params):
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
    title_color = 'red',
    title_name_2= df['team'][1],
    title_color_2 = 'blue',
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
                             radar_color=['red','blue'],
                             alphas=[.75,.60],title=title,endnote=endnote,
                             compare=True)
    return fig




df = get_data()
#----SIDEBAR----
st.sidebar.header("Please select 2 teams for comparision:")
team = st.sidebar.multiselect(
    "Select the teams:",
    options=df["team"].unique(),
    default=['Hyderabad FC','ATK Mohun Bagan FC']
)

df_team_selection = df.query("team == @team")

st.sidebar.header("Please select the parameters(optimum value = 9):")
params = st.sidebar.multiselect(
    "Select the params:",
    options=df.columns,
    default = ['team','goals','xG','goals_conceded','xGA','shots',
               'shots_against','xPoints','xG_per_shot','xGA_per_shot']
)

df_param_selection = df_team_selection[params]
# ---- MAINPAGE ----
st.title(":bar_chart: ISL Dashboard")
st.markdown("##")
st.dataframe(df_team_selection)
# # # TOP KPI's
# total_goals = int(df_team_selection["goals"].sum())
# parameter = df_param_selection.values
# average_xG = round(df_team_selection["xG"].mean()/20, 2)

# left_column, middle_column, right_column = st.columns(3)
# with left_column:
#     st.subheader("Total Goals:")
#     st.subheader(f"{total_goals:,}")
# with middle_column:
#     st.subheader(f"{params}")
#     st.subheader(f"{parameter}")
# with right_column:
#     st.subheader("Average xG per match:")
#     st.subheader(f"{average_xG}")
st.title(":dart: Radar Plot")
st.markdown("""---""")
col = st.columns(1)
st.pyplot(fig=make_radar(df_team_selection,params))