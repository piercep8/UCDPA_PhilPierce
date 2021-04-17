# Read the file

import pandas as pd

# Simplified Position Dictionary - to be used to convert the various midfield positions a generic midfield role
simple_position_dict = {'A': 'A', 'AM': 'M', 'G': 'G', 'D': 'D', 'DM': 'M', 'M': 'M', 'W': 'M'}

# Import CSV File and set the first row as the header. Store as a Pandas Data Frame
master_football_db = pd.read_csv("Football Manager March 20 Full Attribute Database.csv", header=0)
master_football_df = pd.DataFrame(master_football_db)

# Split the Scout Rating Column into 2 columns and remove the % element to leave a score out 100
master_football_df[['Scout Rating', 'Best Position']] = master_football_df['Scout Rating'].str.split('%', 1,
                                                                                                     expand=True)

# Where players have two nationalities
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

# Sort the dataframe into Nation (A-Z), Simple Position (A-Z) and Scout Rating (Highest to Lowest)
master_football_df = master_football_df.sort_values(['Nation', 'Simple Position', 'Scout Rating'],
                                                    ascending=[True, True, False])

goalkeepers_df = master_football_df[(master_football_df['Simple Position'] == 'G')]
defenders_df = master_football_df[(master_football_df['Simple Position'] == 'D')]
midfielders_df = master_football_df[(master_football_df['Simple Position'] == 'M')]
attackers_df = master_football_df[(master_football_df['Simple Position'] == 'A')]

squad_list_df = goalkeepers_df.groupby(['Nation'])['Scout Rating'].nlargest(3)

#squad_lists = master_football_df.loc[master_football_df['Nation'].isin(['Argentina'])
#                                     & master_football_df['Simple Position'].isin(['M'])]
#squad_lists = squad_lists.nlargest(3, ['Scout Rating'])

# Get a list of all nations and a list of all positions
best_pos_values = master_football_df['Best Position'].unique()
nation = master_football_df['Nation'].unique()
# print(master_football_df.info())

print(squad_list_df)
# print(type(best_pos_values))
