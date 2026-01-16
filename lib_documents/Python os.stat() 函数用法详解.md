# Python os.stat() 函数用法详解

这个函数是 Python `os` 库中用于获取文件/目录**详细属性信息**的核心函数，比如文件大小、创建/修改时间、权限等，返回的是一个包含各类文件元数据的对象。

### 一、os.stat() 基本用法

#### 1. 函数语法

```Python

os.stat(path, *, dir_fd=None, follow_symlinks=True)
```

- `path`：必填，文件/目录的路径（字符串/字节串）；

- `dir_fd`：可选，文件描述符（进阶用法，新手暂不用关注）；

- `follow_symlinks`：可选，默认 `True`，表示跟随软链接；设为 `False` 时，直接获取软链接本身的信息而非目标文件。

#### 2. 基础示例（获取文件属性）

```Python

import os
import time

# 目标文件路径（替换成你自己的文件路径）
file_path = "test.txt"

# 1. 获取文件属性对象
stat_info = os.stat(file_path)

# 2. 打印原始的 stat 对象（包含所有属性）
print("原始 stat 对象：", stat_info)
print("-" * 80)

# 3. 提取常用属性（重点）
# 核心属性说明：stat_info.属性名 或 os.stat_result 的索引（如 stat_info[6] = st_size）
print(f"📁 文件大小（字节）: {stat_info.st_size}")
print(f"🔐 文件权限（十进制）: {stat_info.st_mode}")
print(f"🆔 文件Inode号（Linux/Mac）: {stat_info.st_ino}")
print(f"👤 所属用户ID（UID）: {stat_info.st_uid}")
print(f"👥 所属组ID（GID）: {stat_info.st_gid}")

# 时间相关属性（原始是时间戳，需转换为可读格式）
print(f"🕒 最后访问时间: {time.ctime(stat_info.st_atime)}")  # st_atime: access time
print(f"🕒 最后修改时间: {time.ctime(stat_info.st_mtime)}")  # st_mtime: modify time
print(f"🕒 状态更改时间: {time.ctime(stat_info.st_ctime)}")  # st_ctime: change time（Windows=创建时间）
```

#### 3. 输出示例（Linux/Mac）

```Plain Text

原始 stat 对象： os.stat_result(st_mode=33188, st_ino=123456, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=128, st_atime=1736543210, st_mtime=1736543200, st_ctime=1736543190, st_birthtime=1736543180)
--------------------------------------------------------------------------------
📁 文件大小（字节）: 128
🔐 文件权限（十进制）: 33188
🆔 文件Inode号（Linux/Mac）: 123456
👤 所属用户ID（UID）: 501
👥 所属组ID（GID）: 20
🕒 最后访问时间: Fri Jan 16 10:06:50 2026
🕒 最后修改时间: Fri Jan 16 10:06:40 2026
🕒 状态更改时间: Fri Jan 16 10:06:30 2026
```

### 二、关键属性详解（新手必记）

`os.stat()` 返回的 `stat_info` 是 `os.stat_result` 类型的对象，核心属性如下（跨平台通用）：

|属性名|含义|备注|
|---|---|---|
|`st_size`|文件/目录的大小（字节）|目录的大小通常是4096字节|
|`st_mode`|文件类型和权限（十进制）|需转换为八进制看权限|
|`st_mtime`|最后修改时间（时间戳，秒）|最常用的时间属性|
|`st_atime`|最后访问时间（时间戳）|Windows可能不精准|
|`st_ctime`|状态更改时间（Linux/Mac）/ 创建时间（Windows）|跨平台注意区分|
|`st_ino`|Inode编号（Linux/Mac）|Windows无实际意义|
|`st_uid`/`st_gid`|文件所属用户/组ID（Linux/Mac）|Windows返回0|
### 三、实用进阶用法

#### 1. 转换文件权限（十进制→八进制）

`st_mode` 是十进制，需转八进制才能直观看到权限（如 `0o644`）：

```Python

# 提取权限部分（按位与 0o777）
file_perm = stat_info.st_mode & 0o777
print(f"文件权限（八进制）: {oct(file_perm)}")  # 输出示例: 0o644
```

#### 2. 判断文件类型（通过 st_mode）

`os` 库提供辅助函数判断文件类型，基于 `st_mode`：

```Python

# 判断是否是普通文件
is_file = os.path.isfile(file_path)  # 等价于 stat.S_ISREG(stat_info.st_mode)
# 判断是否是目录
is_dir = os.path.isdir(file_path)    # 等价于 stat.S_ISDIR(stat_info.st_mode)
# 判断是否是软链接（需 os.lstat()，不跟随链接）
link_stat = os.lstat(file_path)
is_link = os.path.islink(file_path)  # 等价于 stat.S_ISLNK(link_stat.st_mode)

print(f"是否是普通文件: {is_file}")
print(f"是否是目录: {is_dir}")
print(f"是否是软链接: {is_link}")
```

#### 3. 批量获取文件信息

结合 `os.walk()` 遍历目录，批量获取所有文件的大小和修改时间：

```Python

import os
import time

# 遍历目录，打印所有文件的大小和修改时间
for root, dirs, files in os.walk("."):
    for file in files:
        full_path = os.path.join(root, file)
        stat_info = os.stat(full_path)
        # 转换文件大小为KB（更易读）
        file_size_kb = round(stat_info.st_size / 1024, 2)
        modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat_info.st_mtime))
        print(f"文件: {full_path} | 大小: {file_size_kb} KB | 修改时间: {modify_time}")
```

### 四、注意事项

1. **跨平台差异**：`st_ino`/`st_uid`/`st_gid` 仅在 Linux/Mac 有效；`st_ctime` 在 Windows 是创建时间，Linux/Mac 是属性修改时间；

2. **软链接处理**：`os.stat()` 会跟随软链接获取目标文件信息，若要获取软链接本身的信息，用 `os.lstat()`；

3. **性能**：`os.stat()` 会访问文件系统，批量调用时注意性能（比如遍历大量文件时避免重复调用）。

### 总结

`os.stat()` 的核心用法可归纳为 3 点：

1. 核心作用：获取文件/目录的**详细元数据**（大小、时间、权限等）；

2. 常用属性：`st_size`（大小）、`st_mtime`（修改时间）、`st_mode`（权限/类型）是新手最需掌握的；

3. 进阶技巧：结合 `time` 模块转换时间戳、按位与 `0o777` 转换权限、用 `os.lstat()` 处理软链接。

这个函数常用来做文件筛选（比如按大小/修改时间过滤）、权限检查、文件元数据统计等场景。
> （注：文档部分内容可能由 AI 生成）