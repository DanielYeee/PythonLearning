import pandas as pd

# 读取 Excel 文件到 DataFrame
df1 = pd.read_excel('file1.xlsx', sheet_name='Sheet1')
df2 = pd.read_excel('file2.xlsx', sheet_name='Sheet1')

# 指定要比较的列
column_to_compare_df1 = 'Column1'  # 根据需要调整列名
column_to_compare_df2 = 'Column2'  # 根据需要调整列名

# 提取特定的列并重置索引以基于行位置对齐
df1_col = df1[[column_to_compare_df1]].reset_index(drop=True)
df2_col = df2[[column_to_compare_df2]].reset_index(drop=True)

# 使用 NaN 填充较短的 DataFrame 以对齐行数
max_len = max(len(df1_col), len(df2_col))
df1_col = df1_col.reindex(range(max_len))
df2_col = df2_col.reindex(range(max_len))

# 将两个 DataFrame 并排组合，方便比较
combined_df = pd.concat([df1_col, df2_col], axis=1, keys=['File1', 'File2'])

# 识别差异，keep_shape=True 保持原始形状，keep_equal=True 保留相同的值
comparison = combined_df['File1'].compare(combined_df['File2'], keep_shape=True, keep_equal=True)

# 将比较结果保存到一个新的 Excel 文件中
comparison.to_excel('comparison_result.xlsx')

# 显示比较结果
print(comparison)
