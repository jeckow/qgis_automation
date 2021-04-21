'''
simple function for average null values contained in the dataset
'''

import pandas as pd

df = pd.read_csv('file path here')

# select related columns
time_columns = df.columns[4:]

for column in time_columns:
    for i in range(len(df)):

        # if the first index is has no value
        if i == 0 and (df[column][i] == 0 or df[column][i] == None):
            df.at[i, column] = df[column][i + 1] / 2

        # if the last index is has no value
        elif i == len(df) - 1 and (df[column][i] == 0 or df[column][i] == None):
            df.at[i, column] = df[column][i - 1] / 2

        elif df[column][i] == 0 and 0 < i < len(df) - 1:
            df.at[i, column] = (df[column][i - 1] + df[column][i + 1]) / 2

df.to_csv('file path here')