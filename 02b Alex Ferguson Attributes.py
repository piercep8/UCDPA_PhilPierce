# Program 02b Alex Ferguson Attributes
# ------------------------------------
# Use the squad list file to produce a graph comparing Alex Ferguson's desired attributes to players in the top 50 FIFA
# ranked teams.
#
# Inputs
# ------
# 1) squad_list_df._csv          : The top 50 teams and 23 man squads for each of them.
# 2) outfield_players_df.csv     : A version of the squad list data frame without goalkeepers.# Outputs
#
# Outputs
# 1) ferguson_attributes_df.csv  : A table of the mean ratings per squad for each of Alex Fergusons's desired attributes
#
# Dependencies
# ------------
# 01 Data Clean and Formatting
#
# Dependent Programs
# ------------------
# 03 Manager Comparisons
#
import pandas as pd
import numpy as np
import seaborn.apionly as sns
import matplotlib.pyplot as plt

# Read in Squad List Data Frame
squad_list_df = pd.read_csv("squad_list_df.csv", header=0, encoding='ISO-8859-1')
outfield_players_df = pd.read_csv("outfield_players_df.csv", header=0, encoding='ISO-8859-1')

# Alex Ferguson Desired Skills and Attributes
# as a lot of these stats aren't applicable to goalkeepers they've been ruled out for this set of averages
ambition_df = squad_list_df.groupby(['rank', 'country_abrv'], as_index=False)['Ambition'].mean()
determination_df = squad_list_df.groupby(['rank', 'country_abrv'], as_index=False)['Determination'].mean()
pressure_df = squad_list_df.groupby(['rank', 'country_abrv'], as_index=False)['Pressure'].mean()
professionalism_df = squad_list_df.groupby(['rank', 'country_abrv'], as_index=False)['Professionalism'].mean()
stamina_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Stamina'].mean()
work_rate_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Work Rate'].mean()

#
# Merge Mean stats
ferguson_df = pd.concat([ambition_df, determination_df['Determination'], pressure_df['Pressure'],
                         professionalism_df['Professionalism'], stamina_df['Stamina'],work_rate_df['Work Rate']],
                        axis=1, join='outer')
ferguson_df['all_stats'] = ferguson_df[['Ambition', 'Determination', 'Pressure', 'Professionalism',
                                        'Stamina', 'Work Rate']].mean(axis=1)

# Save to csv
ferguson_df.to_csv('ferguson_attributes_df.csv', header=True, encoding='ISO-8859-1', index=False)

# Update dataset to make it graph ready (reduce number of columns, remove decimal places from whole numbers)
ferguson_graph = ferguson_df[['rank', 'all_stats']]
ferguson_graph['rank'] = ferguson_graph['rank'].astype(np.int64)

# Build and display our graph - a bar chart and a regplot to show linear regression
fig, ax = plt.subplots(sharey=True, sharex=True)

sns.set_theme(style="whitegrid")
sns.regplot(x=np.arange(0, len(ferguson_graph)), y=ferguson_graph['all_stats'], marker='x', fit_reg=True)
sns.barplot(x=ferguson_graph['rank'], y=ferguson_graph['all_stats'], ax=ax, alpha=0.6)
plt.title("How do Alex Ferguson's Desired Attributes for a Team Compare to Current FIFA Rankings")
plt.xlabel('FIFA Ranking')
plt.ylabel('Ferguson Attributes')
plt.show()