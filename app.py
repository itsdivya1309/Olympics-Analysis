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

medals = preprocessor.preprocess(medals)
games = preprocessor.preprocess(games).loc[games['competition_date'] != '—']
results = preprocessor.preprocess(results)
athletes = preprocessor.preprocess(athletes)
athletes = pd.merge(athletes, country, 
                    left_on='country_noc', right_on='noc', how='left')

st.sidebar.title('Summer Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 
     'Overall Analysis', 
     'Country-wise Analysis', 
     'Athlete-wise Analysis')
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
    athletes_over_time = helper.athletes_over_time(games, athletes)
    fig = px.line(athletes_over_time, x='Edition', y='No of Athletes')
    st.plotly_chart(fig)

    st.divider()

    st.title('No of Events over the Years (in every Sport)')
    fig, ax = plt.subplots(figsize=(20,20))
    events = pd.merge(athletes, games, on='edition_id')
    x = events.pivot_table(index='sport', columns='year', 
        values='event', aggfunc=pd.Series.nunique).fillna(0).astype('int')
    ax = sns.heatmap(x, annot=True)
    st.pyplot(fig)

    st.divider()

    st.title('Most Successful Athletes')
    sport_list = athletes['sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.sidebar.selectbox('Select a Sport', sport_list)
    candidates = helper.most_successful(athletes, selected_sport)
    st.table(candidates)