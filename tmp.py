import pandas as pd

# Create the dataframes
df1 = pd.DataFrame({'A': ['a', 'c']})
df2 = pd.DataFrame({'A': ['a', 'b', 'c']})

# Display the dataframes
print("DataFrame 1:")
print(df1)
print("\nDataFrame 2:")
print(df2)

# Find rows in df1 not in df2
rows_in_df1_not_in_df2 = df1[~df1.apply(tuple, 1).isin(df2.apply(tuple, 1))]

# Find rows in df2 not in df1
rows_in_df2_not_in_df1 = df2[~df2.apply(tuple, 1).isin(df1.apply(tuple, 1))]

print("\nRows in df1 not in df2:")
print(rows_in_df1_not_in_df2)
print("\nRows in df2 not in df1:")
print(rows_in_df2_not_in_df1)
