import pandas as pd

# Load the Excel file
file_path = 'your_excel_file.xlsx'
sheet1_name = 'Sheet1'
sheet2_name = 'Sheet2'

# Read the sheets into DataFrames
df1 = pd.read_excel(file_path, sheet_name=sheet1_name)
df2 = pd.read_excel(file_path, sheet_name=sheet2_name)

# Find differences
diff = df1.compare(df2)

# Print differences in a readable format
def print_differences(diff_df):
    print("Differences between the sheets:")
    for row in range(len(diff_df)):
        for col in diff_df.columns.levels[0]:
            if not pd.isna(diff_df.loc[row, (col, 'self')]) or not pd.isna(diff_df.loc[row, (col, 'other')]):
                print(f"Row {row + 1}, Column '{col}':")
                print(f"  {sheet1_name}: {diff_df.loc[row, (col, 'self')]}")
                print(f"  {sheet2_name}: {diff_df.loc[row, (col, 'other')]}")

print_differences(diff)
