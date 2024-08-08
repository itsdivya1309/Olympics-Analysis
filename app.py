import streamlit as st
import pandas as pd
import preprocessor, helper

medals = pd.read_csv('archive/Olympic_Games_Medal_Tally.csv')

df = preprocessor.preprocess(medals)

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

    years, countries = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', countries)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Medal Tally')

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally of '+ selected_country)

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally of '+ str(selected_year)+ ' Olympics')

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' performance in '+str(selected_year)+ ' Olympics')

    st.table(medal_tally)