# Program 02e Kevin Keegan Attributes
# -----------------------------------
# Use the squad list file to produce a graph comparing Kevin Keegan's desired attributes to players in the top 50 FIFA
# ranked teams.
#
# Inputs
# ------
# 1) squad_list_df._csv        : The top 50 teams and 23 man squads for each of them.
# 2) outfield_players_df.csv   : A version of the squad list data frame without goalkeepers.# Outputs
#
# Outputs
# 1) keegan_attributes_df.csv  : A table of the mean ratings per squad for each of Kevin Keegan's desired attributes
#
# Dependencies
# ------------
# 01 Data Clean and Formatting
#
# Dependent Programs
# ------------------
# 03 Manager Comparisions
#
import pandas as pd
import numpy as np
import seaborn.apionly as sns
import matplotlib.pyplot as plt

# Read in Squad List Data Frame
squad_list_df = pd.read_csv("squad_list_df.csv", header=0, encoding='ISO-8859-1')
outfield_players_df = pd.read_csv("outfield_players_df.csv", header=0, encoding='ISO-8859-1')

# Kevin Keegan Desired Skills and Attributes
# as a lot of these stats aren't applicable to goalkeepers they've been ruled out for this set of averages
attack_minded_players_df = outfield_players_df[(outfield_players_df['Simple Position'] != 'DEF')]
sportsmanship_df = squad_list_df.groupby(['rank', 'country_abrv'], as_index=False)['Sportsmanship'].mean()
technique_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Technique'].mean()
creativity_df = attack_minded_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Creativity'].mean()
flair_df = attack_minded_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Flair'].mean()

#
# Merge Mean stats
keegan_df = pd.concat([sportsmanship_df, technique_df['Technique'], creativity_df['Creativity'],flair_df['Flair']],
                      axis=1, join='outer')
keegan_df['all_stats'] = keegan_df[['Technique', 'Creativity', 'Flair', 'Sportsmanship']].mean(axis=1)

# Save to csv
keegan_df.to_csv('keegan_attributes_df.csv', header=True, encoding='ISO-8859-1', index=False)

# Update dataset to make it graph ready (reduce number of columns, remove decimal places from whole numbers)
keegan_graph = keegan_df[['rank', 'all_stats']]
keegan_graph['rank'] = keegan_graph['rank'].astype(np.int64)

# Build and display our graph - a bar chart and a regplot to show linear regression
fig, ax = plt.subplots(sharey=True, sharex=True)

sns.set_theme(style="whitegrid")
sns.regplot(x=np.arange(0, len(keegan_graph)), y=keegan_graph['all_stats'], marker='x', fit_reg=True)
sns.barplot(x=keegan_graph['rank'], y=keegan_graph['all_stats'], ax=ax, alpha=0.6)
plt.title("How do Kevin Keegan's Desired Attributes for a Team Compare to Current FIFA Rankings")
plt.xlabel('FIFA Ranking')
plt.ylabel('Keegan Attributes')
plt.show()