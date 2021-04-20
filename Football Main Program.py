# Read the file
import numpy as np
import pandas as pd

# Simplified Position Dictionary - to be used to convert the various midfield positions a generic midfield role
simple_position_dict = {'A': 'A', 'AM': 'M', 'G': 'G', 'D': 'D', 'DM': 'M', 'M': 'M', 'W': 'M'}

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
# Convert to a Data Frame
fifa_rankings_df = pd.DataFrame(fifa_rankings_db)
# Sort by Ranking Date (most recent first) and then world ranking (highest first)
fifa_rankings_df['rank_date'] = pd.to_datetime(fifa_rankings_df['rank_date'])
fifa_rankings_df = fifa_rankings_df.sort_values(['rank_date', 'rank'], ascending=[False, True])
fifa_rankings_df = fifa_rankings_df.rename(columns={'country_full': 'Nation'})

# Limit to only the most recent rank date
latest_rank_date = fifa_rankings_df['rank_date'].max()
fifa_rankings_df = fifa_rankings_df[fifa_rankings_df['rank_date'] == latest_rank_date]

# Create a list of just the countries and their ranking
fifa_countries_df = fifa_rankings_df[['Nation', 'rank']]

#                                 ------ Import and Format Player Data File -----
# Import CSV File and set the first row as the header. Store as a Pandas Data Frame
master_football_db = pd.read_csv("Football Manager March 20 Full Attribute Database.csv", header=0,
                                 encoding='ISO-8859-1')
master_football_df = pd.DataFrame(master_football_db)

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

# Change the names of Nations in the Master Football Data Frame to match those on the FIFA World Rankings Data Frame
i = len(master_country_list)
for country in range(i):
    master_football_df['Nation'] = master_football_df['Nation'].replace(master_country_list[country],
                                                                        fifa_country_list[country])

# Add the FIFA rankings column onto the Master Football Data Frame
master_football_df = master_football_df.merge(fifa_countries_df, how='left')

# Sort the dataframe into Nation (A-Z), Simple Position (A-Z) and Scout Rating (Highest to Lowest)
master_football_df = master_football_df.sort_values(['rank', 'Nation', 'Simple Position', 'Scout Rating'],
                                                    ascending=[True, True, True, False])

# Produce a subset of the Master Football DF based on player position
goalkeepers_df = master_football_df[(master_football_df['Simple Position'] == 'G')]
defenders_df = master_football_df[(master_football_df['Simple Position'] == 'D')]
midfielders_df = master_football_df[(master_football_df['Simple Position'] == 'M')]
attackers_df = master_football_df[(master_football_df['Simple Position'] == 'A')]

# Create a new dataframe to hold my squad lists for the top 50 teams based on current FIFA World Rankings
squad_list_df = pd.DataFrame()

# Loop through our position based dataframes and for each team in the FIFA top 50, produce a squad based on
for team in range(51):
    temp_goalkeepers_df = goalkeepers_df[(goalkeepers_df['rank'] == team)]
    squad_list_df = squad_list_df.append(temp_goalkeepers_df.head(3))
    temp_defenders_df = defenders_df[(defenders_df['rank'] == team)]
    squad_list_df = squad_list_df.append(temp_defenders_df.head(8))
    temp_midfielders_df = midfielders_df[(midfielders_df['rank'] == team)]
    squad_list_df = squad_list_df.append(temp_midfielders_df.head(7))
    temp_attackers_df = attackers_df[(attackers_df['rank'] == team)]
    squad_list_df = squad_list_df.append(temp_attackers_df.head(5))

ave_rating_df = temp_defenders_df.head(3)
ave_rating_df = ave_rating_df[['Nation', 'Simple Position', 'Scout Rating']]
ave_rating_df['ave rating'] = ave_rating_df.groupby(['Nation', 'Simple Position'])['Scout Rating'].transform("mean")

# Get a list of all nations and a list of all positions
best_pos_values = master_football_df['Best Position'].unique()
nation = master_football_df['Nation'].unique()
#print(master_football_df.info())

#print(squad_list_df[['Name', 'Nation', 'Simple Position', 'Scout Rating']])
# print(type(best_pos_values))
