# Python 中 multiprocessing 进程池的全面使用指南

Python `multiprocessing` 中进程池（`Pool`）的用法，这是批量管理子进程的高效方式，尤其适合处理大量重复任务，我会从核心概念、基础用法、进阶场景等方面讲透，结合代码示例让你快速上手。

### 一、进程池的核心概念

进程池（`multiprocessing.Pool`）是对多个子进程的“池化管理”工具，核心价值是：

- **复用进程**：提前创建固定数量的进程，避免频繁创建/销毁进程的开销（进程创建销毁是高开销操作）；

- **自动调度**：将任务分配给池中的空闲进程执行，无需手动管理每个进程的生命周期；

- **简化编程**：无需手动循环创建 `Process` 对象，一行代码即可批量处理任务。

可以把进程池比作“工厂的固定生产线”：

- 生产线数量（进程数）固定，避免频繁搭建/拆除生产线（对应进程创建/销毁）；

- 任务来了，空闲生产线就处理，忙完再接新任务，效率更高。

### 二、进程池的基础用法（核心方法）

`multiprocessing.Pool` 最常用的方法有 `apply()`、`apply_async()`、`map()`、`imap()`、`close()`、`join()`，其中**异步方法（** **`apply_async`** **/** **`map`** **）** 是日常开发的首选（同步方法 `apply` 效率低，几乎不用）。

#### 1. 基础准备：定义任务函数

先定义一个简单的任务函数（模拟耗时操作）：

```Python

import multiprocessing
import time

# 定义要执行的任务函数
def task(num):
    """模拟耗时任务：计算数字平方，休眠1秒"""
    print(f"进程 {multiprocessing.current_process().pid} 处理任务 {num}")
    time.sleep(1)
    return num * num
```

#### 2. 核心用法1：`map()`（批量同步执行）

`map()` 类似 Python 内置的 `map`，将任务批量分配给进程池，**主进程会等待所有任务完成**，返回结果列表（按任务顺序）。

```Python

if __name__ == "__main__":
    start_time = time.time()
    
    # 创建进程池，指定进程数（建议设为CPU核心数，如4）
    with multiprocessing.Pool(processes=4) as pool:
        # 批量处理任务：将列表中的每个元素传给task函数
        results = pool.map(task, [1, 2, 3, 4, 5])
    
    print(f"所有任务完成，结果：{results}")
    print(f"总耗时：{time.time() - start_time:.2f}秒")
```

**执行结果**：

```Plain Text

进程 1234 处理任务 1
进程 1235 处理任务 2
进程 1236 处理任务 3
进程 1237 处理任务 4
进程 1234 处理任务 5  # 进程1234处理完任务1后，复用处理任务5
所有任务完成，结果：[1, 4, 9, 16, 25]
总耗时：2.01秒  # 4个进程并行，5个任务仅需2秒（而非5秒）
```

- `processes=4`：池中有4个进程，最多同时执行4个任务；

- `with` 语句：自动管理进程池的生命周期（无需手动 `close()`/`join()`）；

- `map()` 特点：结果顺序与任务顺序一致，主进程阻塞等待所有任务完成。

#### 3. 核心用法2：`apply_async()`（异步执行单个任务）

`apply_async()` 是异步执行单个任务，**主进程不阻塞**，需通过 `get()` 获取结果（或 `wait()` 等待），适合灵活控制任务执行。

```Python

if __name__ == "__main__":
    start_time = time.time()
    
    with multiprocessing.Pool(processes=4) as pool:
        # 异步提交5个任务，返回结果对象列表
        result_objs = [pool.apply_async(task, args=(num,)) for num in [1,2,3,4,5]]
        
        # 遍历结果对象，获取每个任务的结果（get()会阻塞，直到对应任务完成）
        results = [res.get() for res in result_objs]
    
    print(f"所有任务完成，结果：{results}")
    print(f"总耗时：{time.time() - start_time:.2f}秒")
```

**执行结果**：与 `map()` 一致，但底层是异步提交任务，灵活性更高。

- `apply_async(task, args=(num,))`：异步提交单个任务，`args` 是任务函数的参数；

- `res.get()`：获取单个任务的结果，若任务未完成则阻塞；

- 优势：可按需获取部分任务结果，无需等待所有任务完成。

#### 4. 核心用法3：`imap()`（迭代式批量执行）

`imap()` 是 `map()` 的迭代版，**返回迭代器**，可逐个获取结果（无需等待所有任务完成），适合处理大量任务（节省内存）。

```Python

if __name__ == "__main__":
    start_time = time.time()
    
    with multiprocessing.Pool(processes=4) as pool:
        # 批量提交任务，返回迭代器
        result_iter = pool.imap(task, [1,2,3,4,5])
        
        # 逐个获取结果（哪个任务先完成，就先返回哪个？不，imap保持顺序）
        for num, res in enumerate(result_iter, 1):
            print(f"任务 {num} 结果：{res}")
    
    print(f"总耗时：{time.time() - start_time:.2f}秒")
```

**执行结果**：

```Plain Text

进程 1234 处理任务 1
进程 1235 处理任务 2
进程 1236 处理任务 3
进程 1237 处理任务 4
任务 1 结果：1  # 任务1完成后立即返回
进程 1234 处理任务 5
任务 2 结果：4
任务 3 结果：9
任务 4 结果：16
任务 5 结果：25
总耗时：2.01秒
```

- 区别于 `map()`：`imap()` 无需一次性存储所有结果，适合处理上万/百万级任务；

- 注意：`imap()` 仍保持任务顺序，若想“谁先完成谁先返回”，用 `imap_unordered()`。

### 三、进程池的关键方法（生命周期管理）

使用进程池时，需掌握以下方法管理其生命周期（`with` 语句会自动处理，但手动管理需注意顺序）：

1. `pool.close()`：关闭进程池，**不再接受新任务**，但已提交的任务会继续执行；

2. `pool.join()`：主进程等待进程池中的所有任务完成，**必须在 ** **`close()`** ** 之后调用**；

3. `pool.terminate()`：强制终止进程池，立即停止所有任务（未完成的任务被终止）。

手动管理示例：

```Python

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4)
    # 提交任务
    results = pool.map(task, [1,2,3,4,5])
    # 关闭进程池（不接受新任务）
    pool.close()
    # 等待所有任务完成
    pool.join()
    print(f"结果：{results}")
```

### 四、进阶场景：进程池的实用技巧

#### 1. 设置进程数为CPU核心数（最优配置）

进程数建议设为 CPU 核心数（或核心数+1），避免进程过多导致调度开销：

```Python

# 获取CPU核心数
cpu_count = multiprocessing.cpu_count()
print(f"CPU核心数：{cpu_count}")
# 创建进程池（默认进程数=CPU核心数）
with multiprocessing.Pool() as pool:  # 不指定processes，默认用cpu_count()
    results = pool.map(task, [1,2,3,4,5])
```

#### 2. 任务函数传多参数（用 `starmap()`）

若任务函数需要多个参数，用 `starmap()`（对应 `map()`）或 `starmap_async()`（对应 `apply_async()`）：

```Python

# 定义多参数任务函数
def task_multi(num1, num2):
    time.sleep(1)
    return num1 + num2

if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        # 传入参数元组的列表
        results = pool.starmap(task_multi, [(1,2), (3,4), (5,6)])
    print(f"多参数任务结果：{results}")  # [3,7,11]
```

#### 3. 回调函数（任务完成后自动执行）

`apply_async()`/`starmap_async()` 支持 `callback` 参数，任务完成后自动调用回调函数（在主进程执行）：

```Python

# 定义回调函数（主进程执行）
def callback_func(result):
    print(f"回调函数：任务结果为 {result}，执行主进程逻辑（如入库/日志）")

if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        pool.apply_async(task, args=(5,), callback=callback_func)
        pool.close()
        pool.join()
```

**执行结果**：

```Plain Text

进程 1234 处理任务 5
回调函数：任务结果为 25，执行主进程逻辑（如入库/日志）
```

- 回调函数适合处理任务结果的后续逻辑（如写入数据库、打印日志），无需主进程主动轮询。

### 五、进程池 vs 手动创建 Process

|维度|进程池（Pool）|手动创建 Process|
|---|---|---|
|进程复用|支持，避免频繁创建/销毁开销|每次创建新进程，开销大|
|任务调度|自动分配任务给空闲进程|需手动管理任务分配|
|代码复杂度|低（一行代码批量处理）|高（循环创建、管理进程列表）|
|适用场景|大量重复、独立的小任务|少量、逻辑复杂的个性化任务|
### 总结

1. **核心价值**：进程池通过复用进程降低开销，自动调度任务，简化批量任务处理；

2. **核心方法**：

    - 批量同步：`map()`（返回结果列表）、`imap()`（返回迭代器）；

    - 异步灵活：`apply_async()`（单个任务）、`starmap_async()`（多参数）；

3. **最佳实践**：

    - 进程数设为 CPU 核心数（`multiprocessing.cpu_count()`）；

    - 用 `with` 语句自动管理进程池生命周期；

    - 大量任务用 `imap()`/`imap_unordered()`，多参数任务用 `starmap()`。

简单来说，进程池是处理“批量、重复、独立任务”的最优选择，比手动创建 `Process` 效率更高、代码更简洁。
> （注：文档部分内容可能由 AI 生成）