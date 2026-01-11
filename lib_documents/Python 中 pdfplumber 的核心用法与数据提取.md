# Python 中 pdfplumber 的核心用法与数据提取

你想了解 Python 中 `pdfplumber` 库的核心用途和常见用法，尤其关注它如何“提取数据”（类比 requests 提交数据的 `data`/`json` 逻辑，pdfplumber 是反向的——从 PDF 中解析出结构化/非结构化数据）。`pdfplumber` 是处理 PDF 文本/表格提取的高性能库，比 PyPDF2 更精准，支持提取文本、表格、页面属性等，我会按「核心用途+常见用法+数据提取（文本/表格）」的逻辑讲解，附可直接运行的示例。

### 一、pdfplumber 是什么？核心用途

`pdfplumber` 是专门用于**解析 PDF 文件内容**的 Python 库，核心优势是：

1. 精准提取 PDF 中的**文本**（支持定位文本位置、字体、大小）；

2. 智能识别 PDF 中的**表格**（还原表格结构，输出为列表/字典等结构化数据）；

3. 可获取页面属性（页码、尺寸、旋转角度）、单个字符/行的信息；

4. 支持逐页解析、指定区域解析，灵活性远超普通 PDF 库。

简单来说：`requests` 是“提交数据到服务器”（data/json 传参），而 `pdfplumber` 是“从 PDF 中提取数据”（把 PDF 里的文本/表格转成列表、字典等可处理的结构化数据）。

### 二、前置准备：安装 pdfplumber

```Bash

pip install pdfplumber
```

### 三、pdfplumber 核心用法（按数据类型分类）

#### 核心逻辑

```Plain Text

打开 PDF 文件 → 遍历/选择页面 → 提取文本/表格 → 转换为结构化数据（列表/字典）
```

---

### 1. 基础用法：提取 PDF 文本（类比提取表单 `data` 字符串）

适用于从 PDF 中提取纯文本内容，可整页提取、指定区域提取，对应 requests 中提取响应 `text` 的逻辑。

#### 示例 1：提取整页文本

```Python

import pdfplumber

# 1. 打开 PDF 文件（上下文管理器，自动关闭文件）
with pdfplumber.open("测试文件.pdf") as pdf:
    # 2. 选择页面（pdf.pages 是页面列表，索引从 0 开始）
    page = pdf.pages[0]  # 提取第 1 页
    
    # 3. 提取整页文本（类比 response.text）
    text = page.extract_text()
    
    # 4. 输出文本（可进一步处理，如按行拆分）
    print("第 1 页文本内容：")
    print(text)
    
    # 可选：按行拆分文本（结构化处理）
    text_lines = text.split("\n")
    print("\n按行拆分后的文本：")
    for line in text_lines:
        print(line.strip())
```

#### 示例 2：提取指定区域的文本（精准定位）

PDF 页面的坐标系：左上角为 (0,0)，向右为 x 轴，向下为 y 轴，可通过 `crop()` 裁剪区域提取：

```Python

import pdfplumber

with pdfplumber.open("测试文件.pdf") as pdf:
    page = pdf.pages[0]
    
    # 定义提取区域：(x0, top, x1, bottom) → 左、上、右、下
    # 示例：提取页面中 100≤x≤500，50≤y≤200 的区域文本
    crop_area = (100, 50, 500, 200)
    cropped_page = page.crop(crop_area)
    
    # 提取裁剪区域的文本
    area_text = cropped_page.extract_text()
    print("指定区域文本：")
    print(area_text)
```

---

### 2. 核心用法：提取 PDF 表格（类比提取 JSON 结构化数据）

这是 `pdfplumber` 最实用的功能，能自动识别表格并转换为**二维列表**（类比 requests 中 `response.json()` 得到的结构化数据），支持复杂表格（合并单元格、跨行跨列）。

#### 示例 1：提取单页所有表格（输出列表格式）

```Python

import pdfplumber

with pdfplumber.open("测试表格.pdf") as pdf:
    page = pdf.pages[0]
    
    # 提取页面中所有表格（返回列表，每个表格是二维列表）
    tables = page.extract_tables()
    
    # 遍历每个表格并输出
    for idx, table in enumerate(tables, start=1):
        print(f"\n第 {idx} 个表格：")
        # 表格是二维列表，每行是一个子列表（类比 JSON 数组）
        for row in table:
            # 清理空值，替换为 ""
            cleaned_row = [cell.strip() if cell else "" for cell in row]
            print(cleaned_row)
```

#### 示例 2：提取表格并转换为字典（结构化 JSON 格式）

将表格的第一行作为表头（key），后续行作为值（value），转换为字典列表（类比接口返回的 JSON 数组）：

```Python

import pdfplumber

def table_to_json(table):
    """将表格（二维列表）转换为字典列表（JSON 格式）"""
    if not table:
        return []
    # 第一行作为表头（key）
    headers = [h.strip() if h else "" for h in table[0]]
    # 后续行作为数据行（value）
    data_list = []
    for row in table[1:]:
        cleaned_row = [cell.strip() if cell else "" for cell in row]
        # 表头和行数据配对成字典
        row_dict = dict(zip(headers, cleaned_row))
        data_list.append(row_dict)
    return data_list

# 主逻辑
with pdfplumber.open("测试表格.pdf") as pdf:
    page = pdf.pages[0]
    tables = page.extract_tables()
    
    # 转换第一个表格为 JSON 格式
    if tables:
        json_style_data = table_to_json(tables[0])
        print("表格转换为 JSON 格式：")
        for item in json_style_data:
            print(item)  # 输出示例：{"姓名": "张三", "年龄": "25", "地址": "北京"}
```

#### 示例 3：提取所有页面的表格并保存为 CSV/JSON

```Python

import pdfplumber
import json
import csv

# 1. 提取所有表格
all_tables = []
with pdfplumber.open("多页表格.pdf") as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        tables = page.extract_tables()
        for table in tables:
            all_tables.append(table)
            print(f"提取第 {page_num} 页表格，共 {len(table)} 行")

# 2. 保存为 CSV（类比表单 data 提交的格式）
with open("表格数据.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    for table in all_tables:
        writer.writerows(table)

# 3. 转换为 JSON 并保存（类比 JSON 提交格式）
json_data = []
for table in all_tables:
    json_data.extend(table_to_json(table))  # 复用上面的 table_to_json 函数

with open("表格数据.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print("表格数据已保存为 CSV 和 JSON 文件！")
```

---

### 3. 进阶用法：获取页面/文本的详细信息

`pdfplumber` 可提取文本的位置、字体、大小等元信息，适用于精准解析：

```Python

import pdfplumber

with pdfplumber.open("测试文件.pdf") as pdf:
    page = pdf.pages[0]
    
    # 1. 获取页面属性
    print("页面尺寸：", page.width, page.height)  # 宽度、高度（像素）
    print("页面旋转角度：", page.rotation)
    
    # 2. 获取文本的详细信息（每个字符/单词的位置、字体）
    chars = page.chars  # 所有字符的信息
    for char in chars[:10]:  # 只看前 10 个字符
        print(f"字符：{char['text']}，位置：({char['x0']}, {char['top']})，字体：{char['fontname']}")
    
    # 3. 获取文本行信息
    lines = page.lines  # 文本行的坐标和尺寸
    words = page.extract_words()  # 提取单词（带位置）
    print("\n提取的单词示例：", words[:5])
```

### 四、常见场景与注意事项

#### 1. 常见应用场景

- 解析 PDF 报表，提取表格数据并入库/分析；

- 提取 PDF 合同中的关键文本（如金额、日期）；

- 批量处理 PDF，转换为结构化数据（CSV/JSON）；

- 校验 PDF 中的文本/表格格式是否符合要求。

#### 2. 避坑要点

- **PDF 类型**：仅支持可编辑的 PDF（非图片扫描件），扫描件需先 OCR（如 `pytesseract`）；

- **合并单元格**：`extract_tables()` 会自动填充合并单元格的内容，无需额外处理；

- **编码问题**：提取文本时指定 `encoding="utf-8"`，避免中文乱码；

- **大文件处理**：用上下文管理器 `with` 打开，逐页处理，避免内存溢出。

### 总结

1. `pdfplumber` 核心用途：从 PDF 中提取**文本**（类比 `response.text`）和**表格**（类比 `response.json()`），转换为结构化数据；

2. 核心用法对应两种数据格式：

    - 文本提取：`page.extract_text()` → 字符串（表单 `data` 格式）；

    - 表格提取：`page.extract_tables()` → 二维列表 → 可转换为字典列表（JSON 格式）；

3. 关键优势：表格识别精准、支持区域提取、可获取文本元信息；

4. 核心流程：`open()` 打开 PDF → 选择 `pages` → `extract_text()`/`extract_tables()` 提取数据 → 转换为列表/字典（结构化）。
> （注：文档部分内容可能由 AI 生成）