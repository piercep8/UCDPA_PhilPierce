# Program 02d Brian Clough Attributes
# -----------------------------------
# Use the squad list file to produce a graph comparing Brian Clough's desired attributes to players in the top 50 FIFA
# ranked teams.
#
# Inputs
# ------
# 1) squad_list_df._csv             : The top 50 teams and 23 man squads for each of them.
# 2) outfield_players_df.csv        : A version of the squad list data frame without goalkeepers.# Outputs
#
# Outputs
# 1) brian_clough_attributes_df.csv : A table of the mean ratings per squad for each of Brian Clough's
#    desired attributes
#
# Dependencies
# ------------
# 01 Data Clean and Formatting
#
# Dependent Programs
# ------------------
# None
#
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read in Squad List Data Frame

squad_list_df = pd.read_csv("squad_list_df.csv", header=0, encoding='ISO-8859-1')

# 1) Defenders Who Can Head and Tackle
#    Produce the mean score for heading for all defenders per national team
#    Produce the mean score for tackling for  all defenders per national team
#    Combine the two to get a mean score for heading and tackling
defenders_who_can_head_df = squad_list_df[(squad_list_df['Simple Position'] == 'DEF')]
defenders_who_can_head_df = defenders_who_can_head_df.groupby(['rank', 'country_abrv', 'Simple Position'],
                                                              as_index=False)['Heading'].mean()
defenders_who_can_tackle_df = squad_list_df[(squad_list_df['Simple Position'] == 'DEF')]
defenders_who_can_tackle_df = defenders_who_can_tackle_df.groupby(['rank', 'country_abrv', 'Simple Position'],
                                                                  as_index=False)['Tackling'].mean()
defenders_who_can_head_and_tackle_df = defenders_who_can_head_df.merge(defenders_who_can_tackle_df, how='left')
defenders_who_can_head_and_tackle_df['head_and_tackle'] = defenders_who_can_head_and_tackle_df[['Heading', 'Tackling']]\
    .mean(axis=1)
#
# 2) Midfielders Who Can Pass
#    Produce the mean score for passing for all midfielders per national team
midfielders_who_can_pass_df = squad_list_df[(squad_list_df['Simple Position'] == 'MID')]
midfielders_who_can_pass_df = midfielders_who_can_pass_df.groupby(['rank', 'country_abrv', 'Simple Position'],
                                                                  as_index=False)['Passing'].mean()
#
# 3) Forwards Who Can Score
#    Produce the mean score for sticking the ball in the net for all forwards per national team
forwards_who_can_score_df = squad_list_df[(squad_list_df['Simple Position'] == 'FWD')]
forwards_who_can_score_df = forwards_who_can_score_df.groupby(['rank', 'country_abrv', 'Simple Position'],
                                                              as_index=False)['Finishing'].mean()

# Merge all the datasets together
clough_df = pd.concat([defenders_who_can_head_and_tackle_df[['rank', 'country_abrv', 'head_and_tackle']],
                       midfielders_who_can_pass_df['Passing'], forwards_who_can_score_df['Finishing']],
                      axis=1, join='outer')

# Produce the mean value of the three statistics
clough_df['all_stats'] = clough_df[['head_and_tackle', 'Passing', 'Finishing']].mean(axis=1)

# Pop it on a csv
clough_df.to_csv('brian_clough_attributes_df.csv', header=True, encoding='ISO-8859-1', index=False)

sns.set_theme(style="darkgrid")
sns.regplot(clough_df['rank'], clough_df['all_stats']).\
    set_title("How do Brian Clough's Attributes for a High Performing Team Match to Current FIFA Rankings")
plt.xlabel('FIFA Ranking')
plt.ylabel('Heading, Tackling, Passing and Finishing Mean Score')