import pandas as pd
import numpy as np
import seaborn.apionly as sns
import matplotlib.pyplot as plt

# Read in Squad List Data Frame

squad_list_df = pd.read_csv("squad_list_df.csv", header=0, encoding='ISO-8859-1')
outfield_players_df = pd.read_csv("outfield_players_df.csv", header=0, encoding='ISO-8859-1')

# Johan Cryuff Desired Skills and Attributes
# as a lot of these stats aren't applicable to goalkeepers they've been ruled out for this set of averages
anticipation_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Anticipation'].mean()
decisions_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Decisions'].mean()
off_the_ball_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Off The Ball'].mean()
positioning_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Positioning'].mean()
nat_fitness_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Nat Fitness'].mean()
stamina_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Stamina'].mean()
work_rate_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Work Rate'].mean()
#
# Merge Mean stats
cryuff_df = pd.concat([anticipation_df, decisions_df['Decisions'], off_the_ball_df['Off The Ball'],
                       positioning_df['Positioning'], nat_fitness_df['Nat Fitness'], stamina_df['Stamina'],
                       work_rate_df['Work Rate']], axis=1, join='outer')
cryuff_df['all_stats'] = cryuff_df[['Anticipation', 'Decisions', 'Off The Ball', 'Positioning',
                                    'Nat Fitness', 'Stamina', 'Work Rate']].mean(axis=1)

# Save to csv
cryuff_df.to_csv('cryuff_attributes_df.csv', header=True, encoding='ISO-8859-1', index=False)

# Update dataset to make it graph ready (reduce number of columns, remove decimal places from whole numbers)
cryuff_graph = cryuff_df[['rank', 'all_stats']]
cryuff_graph['rank'] = cryuff_graph['rank'].astype(np.int64)

# Build and display our graph - a bar chart and a regplot to show linear regression
fig, ax = plt.subplots(sharey=True, sharex=True)

sns.set_theme(style="whitegrid")
sns.regplot(x=np.arange(0, len(cryuff_graph)), y=cryuff_graph['all_stats'], marker='x', fit_reg=True)
sns.barplot(x=cryuff_graph['rank'], y=cryuff_graph['all_stats'], ax=ax, alpha=0.6)
plt.title("How do Johan Cryuff's Desired Attributes for a Team Compare to Current FIFA Rankings")
plt.xlabel('FIFA Ranking')
plt.ylabel('Cryuff Attributes')
plt.show()