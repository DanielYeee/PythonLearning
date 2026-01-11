# Python 中 openpyxl 库核心使用：向 Excel 提交数据

你想学习 Python 中 `openpyxl` 库的核心使用方法，尤其是如何向 Excel 表格中**提交/写入数据**（类比 requests 库中表单用 `data`、JSON 用 `json` 的传参逻辑）。`openpyxl` 是处理 Excel 2007+（.xlsx 格式）的主流库，我会按「基础写入→批量写入→不同格式数据写入」的逻辑，结合示例讲解，让你能直接上手提交数据到 Excel。

### 一、前置准备：安装 openpyxl 库

`openpyxl` 不是 Python 内置库，需先安装：

```Bash

pip install openpyxl
```

### 二、openpyxl 核心概念（先理解再用）

- **Workbook**：工作簿（整个 Excel 文件）；

- **Worksheet**：工作表（Excel 中的单个 sheet）；

- **Cell**：单元格（工作表中的单个格子，如 A1、B2）；

- 写入数据的核心逻辑：打开/创建工作簿 → 选择工作表 → 定位单元格 → 写入数据 → 保存文件。

### 三、基础写入：单个/多个单元格提交数据

#### 1. 创建新 Excel 文件，写入单个单元格数据

```Python

from openpyxl import Workbook

# 1. 创建新的工作簿（默认会创建一个名为 "Sheet" 的工作表）
wb = Workbook()

# 2. 选择要操作的工作表（两种方式）
# 方式1：获取活跃工作表（默认的 Sheet）
ws = wb.active
# 方式2：重命名工作表（可选）
ws.title = "用户数据"

# 3. 向单元格提交数据（类比表单 data 传参，直接赋值）
# 方式1：按单元格名称（A1、B1）赋值
ws["A1"] = "用户名"
ws["B1"] = "年龄"
ws["C1"] = "注册时间"

# 方式2：按行列号（row, column）赋值（row=行，column=列，从 1 开始）
ws.cell(row=2, column=1, value="张三")  # A2 = 张三
ws.cell(row=2, column=2, value=25)      # B2 = 25
ws.cell(row=2, column=3, value="2026-01-10")  # C2 = 2026-01-10

# 4. 保存文件（必须保存才会生效）
wb.save("用户信息.xlsx")
print("数据提交成功，文件已保存！")
```

#### 2. 向已有 Excel 文件追加数据

```Python

from openpyxl import load_workbook

# 1. 加载已有的 Excel 文件（注意：文件不能被其他程序打开，否则报错）
wb = load_workbook("用户信息.xlsx")

# 2. 选择工作表（按名称选择）
ws = wb["用户数据"]

# 3. 追加一行数据（在已有数据后写入）
# 先获取当前工作表的最大行数，避免覆盖
max_row = ws.max_row
ws.cell(row=max_row + 1, column=1, value="李四")
ws.cell(row=max_row + 1, column=2, value=30)
ws.cell(row=max_row + 1, column=3, value="2026-01-11")

# 4. 保存文件（覆盖原文件）
wb.save("用户信息.xlsx")
print("数据追加成功！")
```

### 四、批量提交数据（类比 JSON 传参，批量传字典/列表）

实际开发中常需批量写入结构化数据（如列表、字典），对应 requests 中 JSON 批量传参的场景，`openpyxl` 提供高效的批量写入方式：

#### 1. 批量写入列表数据（按行提交）

适合提交一维/二维列表（如表单批量提交的多条数据）：

```Python

from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "批量数据"

# 模拟批量数据（表头 + 多条记录，类比 JSON 数组）
batch_data = [
    ["商品名称", "价格", "库存"],  # 表头
    ["手机", 2999, 100],
    ["电脑", 5999, 50],
    ["平板", 1999, 80]
]

# 批量写入（逐行提交，比单个 cell 赋值高效）
for row_num, row_data in enumerate(batch_data, start=1):
    for col_num, cell_value in enumerate(row_data, start=1):
        ws.cell(row=row_num, column=col_num, value=cell_value)

# 保存文件
wb.save("商品数据.xlsx")
print("批量列表数据提交成功！")
```

#### 2. 批量写入字典数据（按键值对提交）

适合提交结构化字典（如 JSON 对象），按指定列名匹配数据：

```Python

from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "字典数据"

# 1. 先写入表头（对应字典的键）
headers = ["姓名", "性别", "邮箱"]
for col_num, header in enumerate(headers, start=1):
    ws.cell(row=1, column=col_num, value=header)

# 2. 模拟 JSON 格式的批量数据
json_style_data = [
    {"姓名": "王五", "性别": "男", "邮箱": "wangwu@test.com"},
    {"姓名": "赵六", "性别": "女", "邮箱": "zhaoliu@test.com"},
    {"姓名": "孙七", "性别": "男", "邮箱": "sunqi@test.com"}
]

# 3. 按字典键匹配表头，批量提交数据
for row_num, data_dict in enumerate(json_style_data, start=2):
    for col_num, header in enumerate(headers, start=1):
        # 按表头取字典值，类比 JSON 传参时按 key 取值
        ws.cell(row=row_num, column=col_num, value=data_dict.get(header, ""))

# 保存文件
wb.save("用户字典数据.xlsx")
print("批量字典数据提交成功！")
```

### 五、进阶：提交数据时设置单元格样式（可选）

提交数据后，可对单元格做简单样式美化（如表头加粗、调整列宽）：

```Python

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

wb = Workbook()
ws = wb.active
ws.title = "带样式的数据"

# 1. 写入表头并设置样式
headers = ["订单号", "金额", "状态"]
for col_num, header in enumerate(headers, start=1):
    cell = ws.cell(row=1, column=col_num, value=header)
    # 表头加粗、居中
    cell.font = Font(bold=True, size=12)
    cell.alignment = Alignment(horizontal="center")

# 2. 提交订单数据
order_data = [
    ["OD20260101", 999, "已支付"],
    ["OD20260102", 1999, "待发货"],
    ["OD20260103", 299, "已取消"]
]

for row_num, row_data in enumerate(order_data, start=2):
    for col_num, value in enumerate(row_data, start=1):
        ws.cell(row=row_num, column=col_num, value=value)

# 3. 调整列宽（适配内容）
ws.column_dimensions["A"].width = 12
ws.column_dimensions["B"].width = 8
ws.column_dimensions["C"].width = 10

# 保存文件
wb.save("带样式的订单数据.xlsx")
print("带样式的数据提交成功！")
```

### 六、注意事项（避免踩坑）

1. **文件格式**：`openpyxl` 仅支持 `.xlsx` 格式，不支持 `.xls`（老格式），若需处理 `.xls` 需用 `xlrd/xlwt`；

2. **文件锁定**：写入/保存时，Excel 文件不能被其他程序（如 Excel 客户端）打开，否则会报权限错误；

3. **数据类型**：`openpyxl` 会自动识别数据类型（字符串、数字、日期），日期建议用字符串格式（如 "2026-01-10"）提交；

4. **超大文件**：若需写入十万级以上数据，建议用 `openpyxl` 的 `IterableWorksheet` 或分批次写入，避免内存溢出；

5. **保存覆盖**：`wb.save("文件名.xlsx")` 会直接覆盖原有文件，建议先备份或检查文件是否存在。

### 总结

1. `openpyxl` 提交数据的核心流程：创建/加载工作簿 → 选择工作表 → 定位单元格 → 写入数据 → 保存文件；

2. 数据提交方式（类比 requests 传参）：

    - 单个/少量数据：直接给单元格赋值（类比表单 `data` 传参，逐个字段提交）；

    - 批量结构化数据：列表/字典批量写入（类比 JSON `json` 传参，批量提交）；

3. 关键方法：

    - 创建工作簿：`Workbook()`；加载已有文件：`load_workbook()`；

    - 定位单元格：`ws["A1"]` 或 `ws.cell(row, column, value)`；

    - 保存文件：`wb.save("文件名.xlsx")`；

4. 避坑要点：仅支持 `.xlsx`、写入时文件不能被占用、批量写入优先用循环而非单个赋值。
> （注：文档部分内容可能由 AI 生成）