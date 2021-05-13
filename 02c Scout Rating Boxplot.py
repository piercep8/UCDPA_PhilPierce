# Program 02c Scout Rating Boxplot
# --------------------------------
# Produce a box plot showing the average rating of players in each 23 man squad for the FIFA top 50 ranked teams.
#
# Inputs
# ------
# 1) squad_list_df._csv        : The top 50 teams and 23 man squads for each of them.
# 2) outfield_players_df.csv   : A version of the squad list data frame without goalkeepers.# Outputs
#
# Outputs
# 1) Scout Rating.pdf          : Boxplot graph
#
# Dependencies
# ------------
# 01 Data Clean and Formatting
#
# Dependent Programs
# ------------------
# None
#

import numpy as np
import pandas as pd
import seaborn as sns

squad_list_df = pd.read_csv("squad_list_df.csv", header=0, encoding='ISO-8859-1')
graph_fields = squad_list_df[['rank', 'Scout Rating']]
graph_fields['FIFA Ranking'] = graph_fields['rank'].astype(np.int64)

ax = sns.boxplot(x='FIFA Ranking', y='Scout Rating', data=graph_fields)