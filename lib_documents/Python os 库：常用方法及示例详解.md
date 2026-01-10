# Python os 库：常用方法及示例详解

`os` 库是处理操作系统相关功能的核心模块，主要用于文件/目录操作、路径处理、系统信息获取等。

### 一、`os` 库核心常用方法（按场景分类）

`os` 库的方法可分为 6 大类，覆盖日常开发 90% 的场景，下面逐个讲解核心方法、作用和示例。

#### 1. 路径处理（最常用）

用于拼接、拆分路径，获取当前工作目录等，是文件操作的基础。

|方法|作用|
|---|---|
|`os.getcwd()`|获取当前工作目录（CWD），即脚本运行的目录|
|`os.chdir(path)`|切换当前工作目录到指定路径|
|`os.path.join(path1, path2, ...)`|拼接路径（自动适配系统分隔符：Windows 用 `\`，Linux/Mac 用 `/`）|
|`os.path.abspath(path)`|获取路径的绝对路径|
|`os.path.basename(path)`|获取路径的“文件名/目录名”部分（最后一级）|
|`os.path.dirname(path)`|获取路径的“目录”部分（去掉最后一级）|
|`os.path.split(path)`|拆分路径为 (目录, 文件名/目录名) 元组|
|`os.path.exists(path)`|判断路径（文件/目录）是否存在|
|`os.path.isfile(path)`|判断路径是否为**文件**|
|`os.path.isdir(path)`|判断路径是否为**目录**|
**示例**：

```Python

import os

# 1. 获取/切换当前工作目录
print("当前工作目录：", os.getcwd())  # 输出示例：/Users/xxx/Documents
os.chdir("/tmp")  # 切换到 tmp 目录（Windows 可写 "C:\\tmp"）
print("切换后工作目录：", os.getcwd())

# 2. 路径拼接（推荐用这个，避免手动拼分隔符）
path = os.path.join("data", "logs", "app.log")
print("拼接后的路径：", path)  # Linux/Mac: data/logs/app.log；Windows: data\logs\app.log

# 3. 路径拆分/提取
abs_path = os.path.abspath(path)  # 获取绝对路径
print("绝对路径：", abs_path)
print("文件名：", os.path.basename(abs_path))  # app.log
print("目录部分：", os.path.dirname(abs_path))  # /tmp/data/logs
print("拆分路径：", os.path.split(abs_path))  # ('/tmp/data/logs', 'app.log')

# 4. 路径判断
print("路径是否存在：", os.path.exists(abs_path))  # False（示例路径不存在）
print("是否为文件：", os.path.isfile("test.py"))  # 若当前目录有 test.py 则为 True
print("是否为目录：", os.path.isdir("data"))  # 若存在 data 目录则为 True
```

#### 2. 目录操作

创建、删除、遍历目录，是批量处理文件的核心。

|方法|作用|
|---|---|
|`os.mkdir(path)`|创建**单个**目录（父目录必须存在，否则报错）|
|`os.makedirs(path)`|递归创建目录（父目录不存在则自动创建，如 `a/b/c`）|
|`os.rmdir(path)`|删除**空**目录（非空则报错）|
|`os.removedirs(path)`|递归删除空目录（如 `a/b/c` 空则删 c→b→a，直到非空）|
|`os.listdir(path)`|列出指定目录下的所有文件/目录（返回列表，不含子目录内容）|
**示例**：

```Python

import os

# 1. 创建目录
os.mkdir("single_dir")  # 创建单个目录
os.makedirs("parent/child/grandchild")  # 递归创建多级目录

# 2. 列出目录内容
print("当前目录内容：", os.listdir("."))  # 列出当前目录所有文件/目录

# 3. 删除目录（注意：只能删空目录）
os.rmdir("single_dir")  # 删除空目录
os.removedirs("parent/child/grandchild")  # 递归删除空的多级目录
```

#### 3. 文件操作

重命名、删除文件（注意：`os` 库不推荐直接读写文件，读写用 `open()` 即可）。

|方法|作用|
|---|---|
|`os.rename(old_path, new_path)`|重命名文件/目录|
|`os.remove(path)`|删除**文件**（不能删目录）|
|`os.replace(src, dst)`|替换文件（覆盖目标文件，比 rename 更稳定）|
**示例**：

```Python

import os

# 1. 创建测试文件（用 open()）
with open("old_file.txt", "w") as f:
    f.write("test")

# 2. 重命名文件
os.rename("old_file.txt", "new_file.txt")

# 3. 删除文件
os.remove("new_file.txt")
```

#### 4. 系统信息与环境变量

获取系统类型、环境变量等，适配不同操作系统。

|方法|作用|
|---|---|
|`os.name`|获取操作系统类型（`posix`=Linux/Mac，`nt`=Windows）|
|`os.environ`|获取系统环境变量（字典格式，可读写）|
|`os.getenv(key, default=None)`|获取指定环境变量的值（推荐用这个，避免 KeyError）|
|`os.system(command)`|执行系统命令（返回命令退出码，stdout 直接打印）|
**示例**：

```Python

import os

# 1. 操作系统类型
print("系统类型：", os.name)  # Linux/Mac: posix；Windows: nt

# 2. 环境变量
print("Python 路径：", os.getenv("PATH"))  # 获取 PATH 环境变量
os.environ["MY_VAR"] = "123"  # 设置环境变量
print("自定义环境变量：", os.getenv("MY_VAR"))  # 123

# 3. 执行系统命令
os.system("ls -l")  # Linux/Mac 列出目录内容；Windows 用 "dir"
```

#### 5. 文件/目录权限（进阶）

修改文件/目录的权限（主要用于 Linux/Mac，Windows 支持有限）。

|方法|作用|
|---|---|
|`os.chmod(path, mode)`|修改文件/目录权限（mode 用八进制，如 0o755）|
|`os.chown(path, uid, gid)`|修改文件/目录的所有者（需管理员权限）|
**示例（Linux/Mac）**：

```Python

import os

# 给文件设置 可读可写可执行（所有者）、可读可执行（组/其他）
os.chmod("test.py", 0o755)
```

#### 6. 其他实用方法

|方法|作用|
|---|---|
|`os.path.getsize(path)`|获取文件大小（字节）|
|`os.path.getmtime(path)`|获取文件最后修改时间（时间戳）|
|`os.walk(top)`|递归遍历目录（返回 (当前目录, 子目录列表, 文件列表)）|
**示例**：

```Python

import os
import time

# 1. 获取文件信息
if os.path.exists("test.py"):
    print("文件大小（字节）：", os.path.getsize("test.py"))
    # 最后修改时间转成易读格式
    mtime = os.path.getmtime("test.py")
    print("最后修改时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime)))

# 2. 递归遍历目录（核心！批量处理文件必备）
for root, dirs, files in os.walk("data"):
    print(f"当前目录：{root}")
    print(f"子目录：{dirs}")
    print(f"文件：{files}")
    # 遍历当前目录的所有文件
    for file in files:
        file_path = os.path.join(root, file)
        print(f"文件路径：{file_path}")
```

### 二、完整示例（综合用法）

```Python

import os
import time

# 1. 定义目标目录
target_dir = os.path.join(os.getcwd(), "my_project", "logs")

# 2. 若目录不存在则创建
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
    print(f"创建目录：{target_dir}")

# 3. 创建测试文件
log_file = os.path.join(target_dir, "app_2026.log")
with open(log_file, "w") as f:
    f.write("2026-01-10: 程序启动成功")

# 4. 打印文件信息
print(f"文件绝对路径：{os.path.abspath(log_file)}")
print(f"文件大小：{os.path.getsize(log_file)} 字节")
print(f"最后修改时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(log_file)))}")

# 5. 遍历目录下的所有文件
print("\n目录下的所有文件：")
for root, dirs, files in os.walk(target_dir):
    for file in files:
        print(os.path.join(root, file))

# 6. 清理（删除文件和空目录）
os.remove(log_file)
os.removedirs(target_dir)
print(f"\n删除文件和目录：{target_dir}")
```

### 三、注意事项

1. **路径分隔符**：永远用 `os.path.join()` 拼接路径，不要手动写 `\` 或 `/`，避免跨系统兼容问题。

2. **删除操作**：`os.remove()` 删文件、`os.rmdir()` 删空目录，删除非空目录需用 `shutil.rmtree()`（需导入 `shutil` 库）。

3. **权限问题**：执行 `os.chmod()`、`os.chown()` 或删除/创建系统目录时，可能需要管理员/root 权限。

4. **`os.walk()`**：遍历目录时，`dirs` 是子目录列表，可通过修改 `dirs`（如 `dirs.remove("tmp")`）跳过指定子目录。

### 总结

1. `os` 库核心分为 6 类：路径处理（`os.path.join()`/`os.path.exists()`）、目录操作（`os.makedirs()`/`os.walk()`）、文件操作（`os.rename()`/`os.remove()`）、系统信息（`os.getcwd()`/`os.environ`）等。

2. 最常用的方法：`os.getcwd()`、`os.path.join()`、`os.path.exists()`、`os.makedirs()`、`os.walk()`（批量处理文件必备）。

3. 核心原则：路径操作优先用 `os.path` 系列方法，保证跨系统兼容；删除操作需谨慎，先判断路径存在性。

4. `os.walk()` 是递归遍历目录的核心，批量读取/处理文件时一定要掌握。
> （注：文档部分内容可能由 AI 生成）