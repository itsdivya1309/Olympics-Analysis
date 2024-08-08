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
        ['total', 'gold','silver','bronze'],ascending=False).reset_index()
        
    return medal_tally