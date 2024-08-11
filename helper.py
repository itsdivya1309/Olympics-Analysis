import pandas as pd

def medal_tally(medals):
    country_medals = medals.groupby('country').sum()[['gold','silver','bronze','total']].sort_values(
        ['total', 'gold','silver','bronze'],ascending=False).reset_index()
    return country_medals

def country_year_list(medals):

    # All the years in which Olympics was held
    years = medals['year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    # All the countries that ever participated in Olympics
    countries = medals['country'].unique().tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries

def fetch_medal_tally(medals,year, country):

    flag = 0
    # Medal tally of all countries across the years
    if year=='Overall' and country=='Overall':
        medal_tally = medals

    # Medal tally of a particular country across the years
    if year=='Overall' and country!='Overall':
        flag = 1
        medal_tally = medals[medals['country']==country]

    # Medal tally of all countries for a particular year
    if year!='Overall' and country=='Overall':
        medal_tally = medals[medals['year']==year]

    # Medal count of a country in a given year
    if year!='Overall' and country!='Overall':
        medal_tally = medals[(medals['year']==year) & (medals['country']==country)]

    if flag == 1:
        medal_tally = medal_tally.groupby('year').sum()[['gold','silver','bronze','total']].sort_values(
            'year', ascending=False).reset_index()
    else:
        medal_tally = medal_tally.groupby('country').sum()[['gold','silver','bronze','total']].sort_values(
        ['gold','silver','bronze', 'total'],ascending=False).reset_index()
        
    return medal_tally

def participating_nations_over_time(df):
    nations_over_time = pd.DataFrame(df.groupby('year')['country'].nunique()).reset_index()
    nations_over_time.rename(columns={'year': 'Edition', 'country': 'No of Countries'}, inplace=True)
    return nations_over_time

def events_over_time(games, results):
    summer_events = pd.merge(results, games, on='edition_id')
    events_over_time = pd.DataFrame(summer_events.groupby('year')['sport'].nunique()).reset_index()
    events_over_time.rename(columns={'year':'Edition', 'sport':'No of Sports'}, inplace=True)
    return events_over_time

def athletes_over_time(athletes):
    athletes_over_time = pd.DataFrame(athletes.groupby('year')['athlete'].nunique()).reset_index()
    athletes_over_time.rename({'year':'Edition', 'athlete': 'No of Athletes'}, axis=1, inplace=True)
    return athletes_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['medal'])
    if sport != 'Overall':
        temp_df = temp_df.loc[temp_df['sport']==sport]
    temp_df = temp_df['athlete'].value_counts().reset_index().head(15)
    temp_df = pd.merge(temp_df, df, on='athlete', how='left')[['athlete','count','sport','country']]
    temp_df.rename({'count': 'medal count'}, axis=1, inplace=True)
    temp_df.drop_duplicates(subset=['athlete'],inplace=True)
    return temp_df

def yearwise_medals(df, country='India'):
    temp_df = df.loc[df['country']==country]
    return temp_df

def sportswise_performance(df, country='India'):
    temp_df = df.dropna(subset=['medal'])
    temp_df = df.loc[df['country']==country]
    temp_df.drop_duplicates(subset=['edition_id','country_noc_x',
                                    'sport','event','result_id','pos',
                                    'medal','isTeamSport'], inplace=True)
    performance = temp_df.pivot_table(index='sport', columns='year', 
                                      values='medal', aggfunc='count').fillna(0).astype('int')
    return performance

def country_athletes(df, country='India'):
    temp_df = df.dropna(subset=['medal'])
    temp_df = temp_df.loc[temp_df['country']==country]
    temp_df = temp_df['athlete'].value_counts().reset_index().head(15)
    temp_df = pd.merge(temp_df, df, on='athlete', how='left')[['athlete','count','sport','country']]
    temp_df.drop_duplicates(subset=['athlete'],inplace=True)
    return temp_df   