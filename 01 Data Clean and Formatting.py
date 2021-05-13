# Program 01 Data Clean and Formatting
# ------------------------------------
# In this program we'll do the following...
#    * Use the FIFA rankings to select the top 50 countries in the world at at April 2021.
#    * Create 23 man squads for each of those countries based on the "Scout Rating" score
#      from the Football Manager database.
#
# Inputs
# ------
# 1) Football Manager March 20 Full Attribute Database.csv : Attributes and statistics for 150,000 players as at
#                                                            March 2020.
# 2) fifa_ranking-2021-04-07.csv                           : An historical list of each nation's FIFA ranking up to
#                                                            April 2021.
# Outputs
# -------
# 1) squad_list_df._csv        : The top 50 teams and 23 man squads for each of them.
# 2) outfield_players_df.csv   : A version of the squad list data frame without goalkeepers.
#
# Dependencies
# ------------
# None
#
# Dependent Programs
# ------------------
# 02 Scout Rating Boxplot
# 02 Johan Cryuff Attributes
# 02 Alex Ferguson Attributes
# 02 Brian Clough Attributes
# 02 Kevin Keegan Attributes
#
import numpy as np
import pandas as pd

# Simplified Position Dictionary - to be used to convert the various midfield positions a generic midfield role
simple_position_dict = {'A': '4: FWD', 'AM': '3: MID', 'G': '1: GK', 'D': '2: DEF', 'DM': '3: MID', 'M': '3: MID', 'W': '3: MID'}

fifa_country_list = ['Netherlands', 'USA', 'IR Iran', 'Korea Republic', 'Republic of Ireland',
                     'Northern Ireland', 'Bosnia and Herzegovina', 'Côte dIvoire', 'Congo DR', 'Cabo Verde',
                     'United Arab Emirates', 'China PR', 'Kyrgyz Republic', 'Trinidad and Tobago',
                     'Korea DPR', 'Central African Republic', 'Antigua and Barbuda', 'St. Kitts and Nevis',
                     'Suriname', 'Swaziland', 'St. Vincent / Grenadines', 'St. Lucia', 'Brunei Darussalam',
                     'Timor-Leste', 'Turks and Caicos Islands', 'US Virgin Islands', 'British Virgin Islands']
master_country_list = ['Holland', 'U.S.A.', 'Iran', 'South Korea', 'Ireland', 'N.Ireland', 'Bosnia', 'Ivory Coast',
                       'Congo', 'Cape Verde', 'U.A.E.', 'China', 'Kyrgyzstan', 'Trinidad & Tobago', 'North Korea',
                       'Central African Rep.', 'Antigua & Barbuda', 'St Kitts & Nevis', 'Surinam', 'eSwatini',
                       'St Vincent', 'St Lucia', 'Brunei', 'Timor', 'Turks and Caicos Is.', 'US Virgin Is.',
                       'British Virgin Is.']

#                           ----- Import and Format Current FIFA World Rankings File -----
fifa_rankings_db = pd.read_csv("fifa_ranking-2021-04-07.csv", header=0)

# Check for null values
total_fifa_nulls = fifa_rankings_db.isna().sum().sum()
if total_fifa_nulls > 0:
    fifa_nulls = fifa_rankings_db.isnull().sum(axis=0)
    print("FIFA Rankings Columns Null Value Count")
    print(fifa_nulls)
else:
    print("No null values in the FIFA Rankings Database")

# Convert to a Data Frame
fifa_rankings_df = pd.DataFrame(fifa_rankings_db)
# Sort by Ranking Date (most recent first) and then world ranking (highest first)
fifa_rankings_df['rank_date'] = pd.to_datetime(fifa_rankings_df['rank_date'])
fifa_rankings_df = fifa_rankings_df.sort_values(['rank_date', 'rank'], ascending=[False, True])
fifa_rankings_df = fifa_rankings_df.rename(columns={'country_full': 'Nation'})

# Select the FIFA Rankings closest to the date on the Football Manager Database
closest_rank_date = '2020-04-09 00:00:00'
fifa_rankings_df = fifa_rankings_df[fifa_rankings_df['rank_date'] == closest_rank_date]

# Create a list of just the countries, their ranking and short_name
fifa_countries_df = fifa_rankings_df[['Nation', 'rank', 'country_abrv']]

#                                 ------ Import and Format Player Data File -----
# Import CSV File and set the first row as the header. Store as a Pandas Data Frame
master_football_db = pd.read_csv("Football Manager March 20 Full Attribute Database.csv", header=0,
                                 encoding='ISO-8859-1')
master_football_df = pd.DataFrame(master_football_db)

# Check for null values
total_master_nulls = master_football_df.isna().sum().sum()
if total_master_nulls > 0:
    master_nulls = master_football_df.isnull().sum(axis=0)
    print("Null Values from Football Manager Database as follows...")
    print(master_nulls)
else:
    print("No null values in the Master Football Database")

# Split the Scout Rating Column into 2 columns and remove the % element to leave a score out 100
master_football_df[['Scout Rating', 'Best Position']] = master_football_df['Scout Rating'].str.split('%', 1,
                                                                                                     expand=True)
# Split the Nation column into two where players have a 2nd nationality
master_football_df[['Nation', '2nd Nation']] = master_football_df['Nation'].str.split('/', 1, expand=True)

# Remove tabs from the Best Position Column
master_football_df['Best Position'] = master_football_df['Best Position'].replace("\t", " ", regex=True)

# Remove leading spaces and brackets from the Best Position Column
master_football_df['Best Position'] = master_football_df['Best Position'].apply(lambda x: x.strip())
master_football_df['Best Position'] = master_football_df['Best Position'].map(lambda x: x.lstrip('(').rstrip(')'))

# Change Scout Rating from type Object to type Float
master_football_df['Scout Rating'] = pd.to_numeric(master_football_df['Scout Rating'])

# Remove tabs from the Player Name column
master_football_df['Name'] = master_football_df['Name'].replace("\t", " ", regex=True)

# Simplify the positions so Wingers, Defensive Midfielders and Attacking Midfielders are all grouped as Midfielders
master_football_df['Simple Position'] = master_football_df['Best Position'].map(simple_position_dict)

# Split the Simple Position column to produce a position order column. So "1: GK" becomes "1" and "GK"
master_football_df[['position order', 'Simple Position']] = master_football_df['Simple Position'].str.split(':', 1, expand=True)
master_football_df['Simple Position'] = master_football_df['Simple Position'].apply(lambda x: x.strip())

# Change the names of Nations in the Master Football Data Frame to match those on the FIFA World Rankings Data Frame
i = len(master_country_list)
for country in range(i):
    master_football_df['Nation'] = master_football_df['Nation'].replace(master_country_list[country],
                                                                        fifa_country_list[country])
# Add the FIFA rankings column onto the Master Football Data Frame
master_football_df = master_football_df.merge(fifa_countries_df, how='left')

# Sort the dataframe into Nation (A-Z), Simple Position (A-Z) and Scout Rating (Highest to Lowest)
master_football_df = master_football_df.sort_values(['rank', 'Nation', 'position order', 'Scout Rating'],
                                                    ascending=[True, True, True, False])

# Produce a subset of the Master Football DF based on player position
goalkeepers_df = master_football_df[(master_football_df['Simple Position'] == 'GK')]
defenders_df = master_football_df[(master_football_df['Simple Position'] == 'DEF')]
midfielders_df = master_football_df[(master_football_df['Simple Position'] == 'MID')]
attackers_df = master_football_df[(master_football_df['Simple Position'] == 'FWD')]

# Create a new dataframe to hold my squad lists for the top 50 teams based on current FIFA World Rankings
squad_list_df = pd.DataFrame()
ave_rating_df = pd.DataFrame([['rank', 'country_abrv','position order', 'Simple Position', 'Scout Rating', 'Ave Rating']])

# Loop through our position based dataframes and for each team in the FIFA top 50, produce a squad based on
for team in range(51):
    temp_goalkeepers_df = goalkeepers_df[(goalkeepers_df['rank'] == team)]
    temp_goalkeepers_df = temp_goalkeepers_df.head(3)
    squad_list_df = squad_list_df.append(temp_goalkeepers_df)
    temp_defenders_df = defenders_df[(defenders_df['rank'] == team)]
    squad_list_df = squad_list_df.append(temp_defenders_df.head(8))
    temp_midfielders_df = midfielders_df[(midfielders_df['rank'] == team)]
    squad_list_df = squad_list_df.append(temp_midfielders_df.head(7))
    temp_attackers_df = attackers_df[(attackers_df['rank'] == team)]
    squad_list_df = squad_list_df.append(temp_attackers_df.head(5))
#
# This data frame is the basis of all the dataframes that will be used to produce our graphs
squad_list_df = squad_list_df.sort_values(['rank', 'country_abrv', 'position order', 'Scout Rating'],
                                          ascending=[True, True, True, False])
# as a lot of these stats aren't applicable to goalkeepers they've been ruled out for this set of averages
outfield_players_df = squad_list_df[(squad_list_df['Simple Position'] != 'GK')]

# Create csv files for our graph data
squad_list_df.to_csv('squad_list_df.csv', header=True, encoding='ISO-8859-1', index=False)
outfield_players_df.to_csv('outfield_players_df.csv', header=True, encoding='ISO-8859-1', index=False)