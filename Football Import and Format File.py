# Read the file

import pandas as pd

# Import CSV File and set the first row as the header. Store as a Pandas Data Frame
master_football_db = pd.read_csv("Football Manager March 20 Full Attribute Database.csv", header=0)
master_football_df = pd.DataFrame(master_football_db)

# Split the Scout Rating Column into 2 columns and remove the % element to leave a score out 100
master_football_df[['Scout Rating', 'Best Position']] = master_football_df['Scout Rating'].str.split('%', 1, expand=True)

# Remove leading spaces and brackets from the Best Position Column
master_football_df['Best Position'] = master_football_df['Best Position'].apply(lambda x: x.strip())
master_football_df['Best Position'] = master_football_df['Best Position'].map(lambda x: x.lstrip('(').rstrip(')'))


# Test Output
first_ten = master_football_df.head(10)
print(first_ten[['Name', 'Scout Rating', 'Best Position']])




