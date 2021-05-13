# Program 03 Manager Comparisons
# ------------------------------
# Take all the mean rating files out of the manager programs, produce linear regression scores for each manager
# and display those scores in a bar chart. This'll give us an idea which manager's ideals correlate most closely to
# successful teams.
#
# Inputs
# ------
# 1) cryuff_attributes_df.csv       : A table of the mean ratings per squad for each of Johan Cryuff's
#                                     desired attributes.
# 2) ferguson_attributes_df.csv  :    A table of the mean ratings per squad for each of Alex Fergusons's
#                                     desired attributes.
# 3) brian_clough_attributes_df.csv : A table of the mean ratings per squad for each of Brian Clough's
#                                     desired attributes.
# 4) keegan_attributes_df.csv       : A table of the mean ratings per squad for each of Kevin Keegan's
#                                     desired attributes.
#
# Outputs
# -------
# None
#
# Dependencies
# ------------
# 02a Johan Cryuff Attributes
# 02b Alex Ferguson Attributes
# 02d Brian Clough Attributes
# 02e Kevin Keegan Attributes
#
# Dependent Programs
# ------------------
# None
#
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Read in the results of each manager's desired attributes vs FIFA ranking
clough_df = pd.read_csv('brian_clough_attributes_df.csv', header=0, encoding='ISO-8859-1')
keegan_df = pd.read_csv('keegan_attributes_df.csv', header=0, encoding='ISO-8859-1')
ferguson_df = pd.read_csv('ferguson_attributes_df.csv', header=0, encoding='ISO-8859-1')
cryuff_df = pd.read_csv('cryuff_attributes_df.csv', header=0, encoding='ISO-8859-1')

# Determine the linear coefficient for each manager
slope, intercept, r_value, p_value, std_err = stats.linregress(clough_df['rank'], clough_df['all_stats'])
clough_r_value = r_value

slope, intercept, r_value, p_value, std_err = stats.linregress(keegan_df['rank'], keegan_df['all_stats'])
keegan_r_value = r_value

slope, intercept, r_value, p_value, std_err = stats.linregress(ferguson_df['rank'], ferguson_df['all_stats'])
ferguson_r_value = r_value

slope, intercept, r_value, p_value, std_err = stats.linregress(cryuff_df['rank'], cryuff_df['all_stats'])
cryuff_r_value = r_value

# Store the results in a data frame
names_list = ['Clough', 'Keegan', 'Ferguson', 'Cryuff']
r_value_list = [clough_r_value, keegan_r_value, ferguson_r_value, cryuff_r_value]

r_value_array = np.array(list(zip(names_list, r_value_list)))
r_value_df = pd.DataFrame(r_value_array, columns=['manager', 'r_value'])

# Convert the r value to a number that'll look nice on a graph (for example from -0.77 to 77)
# Sort the dataframe from highest r value to lowest
r_value_df['r_value'] = r_value_df['r_value'].astype('float64')
r_value_df['r_value'] = r_value_df['r_value'].apply(lambda x: x*-100)
r_value_df = r_value_df.sort_values('r_value', ascending=False)

sns.set_theme(style='darkgrid')
sns.barplot(x=r_value_df['r_value'], y=r_value_df['manager'], orient='h')

plt.title("How Do The Quotes Stack Up?")
plt.xlabel('Linear Correlation Coefficient')
plt.ylabel('Manager')
plt.show()