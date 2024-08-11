import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import preprocessor, helper

medals = pd.read_csv('archive/Olympic_Games_Medal_Tally.csv')
games = pd.read_csv('archive/Olympics_Games.csv')
results = pd.read_csv('archive/Olympic_Results.csv')
athletes = pd.read_csv('archive/Olympic_Athlete_Event_Results.csv')
country = pd.read_csv('archive/Olympics_Country.csv')
bio = pd.read_csv('archive/Olympic_Athlete_Bio.csv')

medals = preprocessor.preprocess(medals)
games = preprocessor.preprocess(games).loc[games['competition_date'] != '—']
results = preprocessor.preprocess(results)
athletes = preprocessor.preprocess(athletes)
athletes = pd.merge(athletes, country, 
                    left_on='country_noc', right_on='noc', how='left')
athletes = pd.merge(athletes, games, on='edition_id', how='left')

st.sidebar.image('archive/download.png')
st.sidebar.title('Summer Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 
     'Overall Analysis', 
     'Country-wise Analysis'
    )
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    years, countries = helper.country_year_list(medals)

    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', countries)

    medal_tally = helper.fetch_medal_tally(medals, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Medal Tally')

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally of '+ selected_country)

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally of '+ str(selected_year)+ ' Olympics')

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' performance in '+str(selected_year)+ ' Olympics')

    st.table(medal_tally)

if user_menu == 'Overall Analysis':

    editions = medals['year'].nunique()
    cities = games['city'].nunique()
    sports = results['sport'].nunique()
    events = results['event_title'].nunique()
    nations = medals['country'].nunique()
    n_athletes = athletes['athlete'].nunique()


    st.title('Quick Statistics')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader(editions)
        st.header('Editions')    
    with col2:
        st.subheader(cities)
        st.header('Host cities')    
    with col3:
        st.subheader(sports)
        st.header('Sports')

    st.divider()      
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader(events)
        st.header('Events')   
    with col2:
        st.subheader(nations)
        st.header('Participating Nations')   
    with col3:
        st.subheader(n_athletes)
        st.header('Total Athletes')

    st.divider()

    st.title('Participating Nations over the Years')
    nations_over_time = helper.participating_nations_over_time(medals)
    fig = px.line(nations_over_time, x='Edition', y='No of Countries')
    st.plotly_chart(fig)

    st.divider()

    st.title('No of Sports over the Years')
    events_over_years = helper.events_over_time(games, results)
    fig = px.line(events_over_years, x='Edition', y='No of Sports')
    st.plotly_chart(fig)

    st.divider()

    st.title('No of Athletes over the Years')
    athletes_over_time = helper.athletes_over_time(athletes)
    fig = px.line(athletes_over_time, x='Edition', y='No of Athletes')
    st.plotly_chart(fig)

    st.divider()

    st.title('Men vs Women Participation over the Years')
    df = helper.males_vs_females(athletes, bio)
    fig = px.line(df, x='year', y=['Males','Females'])
    st.plotly_chart(fig)

    st.divider()

    st.title('No of Events over the Years (in every Sport)')
    fig, ax = plt.subplots(figsize=(20,20))
    x = athletes.pivot_table(index='sport', columns='year', 
        values='event', aggfunc=pd.Series.nunique).fillna(0).astype('int')
    ax = sns.heatmap(x, annot=True)
    st.pyplot(fig)

    st.divider()

    st.title('Most Successful Athletes')
    sport_list = athletes['sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.sidebar.header('Overall Athletes Analysis')
    selected_sport = st.sidebar.selectbox('Select a Sport', sport_list)
    candidates = helper.most_successful(athletes, selected_sport)
    st.table(candidates)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Most Successful Analysis')

    countries = country['country'].unique().tolist()
    selected_country = st.sidebar.selectbox('Select Country', countries)

    st.header(selected_country+' Medal Tally over the years')

    temp_df = helper.yearwise_medals(medals, selected_country)
    fig = px.line(temp_df, x='year', y=['total', 'gold', 'silver', 'bronze'])
    st.plotly_chart(fig)

    st.divider()

    st.header(selected_country+ ' Performance in different sports')
    x = helper.sportswise_performance(athletes, selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(x, annot=True)
    st.pyplot(fig)

    st.divider()
    st.header('Most Successful Athletes of '+selected_country)
    players = helper.country_athletes(athletes, selected_country)
    st.table(players)
