# 03 Manager Pairplot
# ------------------------------------
# I didn't end up using this, the results didn't display the data in a usable way.
#

import pandas as pd
import seaborn as sns

# Read in the results of each manager's desired attributes vs FIFA ranking
clough_df = pd.read_csv('brian_clough_attributes_df.csv', header=0, encoding='ISO-8859-1')
keegan_df = pd.read_csv('keegan_attributes_df.csv', header=0, encoding='ISO-8859-1')
ferguson_df = pd.read_csv('ferguson_attributes_df.csv', header=0, encoding='ISO-8859-1')
cryuff_df = pd.read_csv('cryuff_attributes_df.csv', header=0, encoding='ISO-8859-1')

# Determine the linear coefficient for each manager
clough_df['clough_stats'] = clough_df['all_stats']
keegan_df['keegan_stats'] = keegan_df['all_stats']
ferguson_df['ferguson_stats'] = ferguson_df['all_stats']
cryuff_df['cryuff_stats'] = cryuff_df['all_stats']

all_managers = pd.concat([clough_df[['rank', 'clough_stats']], keegan_df['keegan_stats'], ferguson_df['ferguson_stats'],
                         cryuff_df['cryuff_stats']], axis=1, join='outer')

sns.set_theme(style='darkgrid')
sns.pairplot(all_managers, x_vars=['rank'], y_vars=['clough_stats', 'keegan_stats', 'ferguson_stats', 'cryuff_stats'],
             kind='reg', aspect=0.3, height=2.5)
