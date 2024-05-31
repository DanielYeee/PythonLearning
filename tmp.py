import pandas as pd

# Sample dataframes
df1 = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': ['a', 'b', 'c', 'd', 'e'],
    'C': [10, 20, 30, 40, 50]
})

df2 = pd.DataFrame({
    'A': [3, 4, 5, 6, 7],
    'B': ['f', 'g', 'h', 'i', 'j'],
    'C': [60, 70, 80, 90, 100]
})

# Print original dataframes
print("Original df1:")
print(df1)
print("\nOriginal df2:")
print(df2)

# Merge dataframes on column 'A' to find common rows
common_rows = df1.merge(df2, on='A', how='inner')

# Filter out common rows from df1 and df2
df1_filtered = df1[~df1['A'].isin(common_rows['A'])]
df2_filtered = df2[~df2['A'].isin(common_rows['A'])]

# Print filtered dataframes
print("\nFiltered df1:")
print(df1_filtered)
print("\nFiltered df2:")
print(df2_filtered)
