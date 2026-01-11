# Python requests 库核心用法教程

你想系统学习 Python 中 `requests` 库的核心用法，这个库是处理 HTTP 请求的首选工具（比内置的 `urllib` 更简洁易用），我会按「核心请求方法+响应处理+进阶功能」的逻辑，逐个讲解核心方法、作用并附可直接运行的示例，让你快速上手。

### 一、前置准备：安装 requests 库

`requests` 不是 Python 内置库，需先安装：

```Bash

pip install requests
```

### 二、requests 库核心请求方法

`requests` 库的核心是发送不同类型的 HTTP 请求，对应 HTTP 协议的常用方法（GET/POST/PUT/DELETE 等），其中 **GET** 和 **POST** 是最常用的。

#### 1. requests.get()：发送 GET 请求（最常用）

**作用**：向指定 URL 发送 GET 请求（用于获取数据，如查询、读取页面内容），参数通常拼在 URL 后或通过 `params` 传参。

**语法**：

```Python

requests.get(url, params=None, headers=None, cookies=None, timeout=None)
```

|参数|作用|
|---|---|
|`url`|必选，请求的目标 URL|
|`params`|可选，字典/字符串，拼接在 URL 后的查询参数（如 `?key1=val1&key2=val2`）|
|`headers`|可选，字典，请求头（模拟浏览器、传递 Token 等）|
|`cookies`|可选，字典，请求携带的 Cookie|
|`timeout`|可选，数字，请求超时时间（秒），避免程序卡死|
**示例 1：基础 GET 请求（获取数据）**

```Python

import requests

# 目标 URL（示例：获取GitHub公共API数据）
url = "https://api.github.com/users/octocat"

# 发送 GET 请求
response = requests.get(url, timeout=10)

# 打印响应状态码（200=成功）
print("响应状态码：", response.status_code)

# 打印响应内容（JSON 格式）
print("响应内容（JSON）：", response.json())
```

**示例 2：带查询参数的 GET 请求**

```Python

import requests

url = "https://httpbin.org/get"
# 查询参数：key1=value1，key2=value2
params = {
    "key1": "value1",
    "key2": "value2"
}

# 发送带参数的 GET 请求（自动拼接为 https://httpbin.org/get?key1=value1&key2=value2）
response = requests.get(url, params=params, timeout=10)

# 打印最终请求的 URL（验证参数是否拼接成功）
print("最终请求URL：", response.url)
# 打印响应文本
print("响应文本：", response.text)
```

**示例 3：带请求头的 GET 请求（模拟浏览器）**

很多网站会拦截非浏览器请求，需添加 `User-Agent` 头：

```Python

import requests

url = "https://www.baidu.com"
# 请求头：模拟 Chrome 浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers, timeout=10)
# 设置编码（避免中文乱码）
response.encoding = "utf-8"
print("百度首页内容：", response.text[:500])  # 打印前500个字符
```

#### 2. requests.post()：发送 POST 请求

**作用**：向指定 URL 发送 POST 请求（用于提交数据，如登录、表单提交、上传数据），参数通常放在请求体中。

**语法**：

```Python

requests.post(url, data=None, json=None, headers=None, cookies=None, timeout=None)
```

|参数|作用|
|---|---|
|`data`|可选，字典/字符串，表单格式的请求体（`application/x-www-form-urlencoded`）|
|`json`|可选，字典，JSON 格式的请求体（`application/json`，接口开发最常用）|
**示例 1：表单格式的 POST 请求（模拟登录）**

```Python

import requests

url = "https://httpbin.org/post"  # 测试用的 POST 接口
# 表单数据（如用户名、密码）
form_data = {
    "username": "test_user",
    "password": "123456"
}

# 发送表单格式的 POST 请求
response = requests.post(url, data=form_data, timeout=10)
print("响应内容：", response.json())
```

**示例 2：JSON 格式的 POST 请求（接口开发常用）**

```Python

import requests

url = "https://httpbin.org/post"
# JSON 数据（接口请求最常用格式）
json_data = {
    "name": "张三",
    "age": 25,
    "hobbies": ["读书", "编程"]
}

# 发送 JSON 格式的 POST 请求（自动设置 Content-Type: application/json）
response = requests.post(url, json=json_data, timeout=10)
print("响应JSON：", response.json())
```

#### 3. 其他常用请求方法（PUT/DELETE/HEAD）

|方法|作用|用法示例|
|---|---|---|
|`requests.put()`|更新资源（全量更新）|`response = requests.put(url, json={"age":26})`|
|`requests.delete()`|删除资源|`response = requests.delete(url, timeout=10)`|
|`requests.head()`|只获取响应头（不返回体）|`response = requests.head(url, timeout=10)`|
### 三、响应对象（Response）的核心方法/属性

发送请求后会返回 `Response` 对象，这是处理返回数据的核心，常用属性/方法如下：

|属性/方法|作用|
|---|---|
|`response.status_code`|HTTP 响应状态码（200=成功，404=未找到，500=服务器错误，401=未授权）|
|`response.text`|响应内容的字符串形式（自动解码，适合文本/HTML）|
|`response.json()`|响应内容解析为 JSON 字典（仅适用于 JSON 格式的响应，否则报错）|
|`response.content`|响应内容的二进制形式（适合下载图片、文件）|
|`response.headers`|响应头（字典格式）|
|`response.cookies`|响应返回的 Cookie（RequestsCookieJar 对象，可按字典访问）|
|`response.encoding`|设置/获取响应内容的编码（如 `utf-8`，解决中文乱码）|
|`response.url`|最终请求的 URL（含重定向后的地址）|
**示例：完整处理响应**

```Python

import requests

url = "https://api.github.com/users/octocat"
response = requests.get(url, timeout=10)

# 1. 检查请求是否成功（状态码 200）
if response.status_code == 200:
    print("请求成功！")
    
    # 2. 响应头
    print("响应头：", response.headers["Content-Type"])  # application/json; charset=utf-8
    
    # 3. 解析 JSON 数据
    data = response.json()
    print("用户名：", data["login"])  # octocat
    print("仓库数量：", data["public_repos"])  # 8
    
    # 4. 编码（确保中文不乱码）
    response.encoding = "utf-8"
else:
    print(f"请求失败，状态码：{response.status_code}")
```

### 四、requests 库进阶用法（实用场景）

#### 场景1：下载文件/图片（二进制内容）

```Python

import requests

# 图片 URL
img_url = "https://www.baidu.com/img/flexible/logo/pc/result.png"
# 发送请求获取二进制内容
response = requests.get(img_url, timeout=30)

# 保存图片到本地
if response.status_code == 200:
    with open("baidu_logo.png", "wb") as f:
        f.write(response.content)
    print("图片下载成功！")
else:
    print("图片下载失败！")
```

#### 场景2：处理 Cookie（保持登录状态）

```Python

import requests

# 第一步：登录获取 Cookie（示例用测试接口）
login_url = "https://httpbin.org/cookies/set"
# 发送请求设置 Cookie
response = requests.get(login_url, params={"token": "123456abc"}, timeout=10)

# 第二步：携带 Cookie 访问需要登录的接口
target_url = "https://httpbin.org/cookies"
# 方式1：直接用响应的 cookies
response2 = requests.get(target_url, cookies=response.cookies, timeout=10)
# 方式2：手动传 Cookie 字典
# cookies = {"token": "123456abc"}
# response2 = requests.get(target_url, cookies=cookies, timeout=10)

print("Cookie 信息：", response2.json())
```

#### 场景3：设置超时和异常处理（健壮性）

```Python

import requests
from requests.exceptions import RequestException, Timeout

url = "https://api.github.com/users/octocat"

try:
    # 设置超时时间 5 秒
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # 若状态码非 200，抛出 HTTPError 异常
    data = response.json()
    print("请求成功：", data["login"])
except Timeout:
    print("请求超时！")
except RequestException as e:
    print(f"请求失败：{e}")
```

#### 场景4：使用 Session 保持会话（跨请求保持状态）

`Session` 可在多个请求间保持 Cookie、连接复用，适合登录后连续请求：

```Python

import requests

# 创建 Session 对象
session = requests.Session()

# 第一步：登录（Session 会自动保存 Cookie）
login_data = {"username": "test", "password": "123"}
session.post("https://httpbin.org/post", data=login_data, timeout=10)

# 第二步：后续请求（自动携带登录的 Cookie）
response = session.get("https://httpbin.org/cookies", timeout=10)
print("会话中的 Cookie：", response.json())

# 关闭 Session
session.close()
```

### 总结

1. `requests` 库核心请求方法：

    - `get()`：获取数据（参数用 `params`）；

    - `post()`：提交数据（表单用 `data`，JSON 用 `json`）；

    - 其他：`put()`（更新）、`delete()`（删除）。

2. 响应处理核心：

    - `status_code` 判成功；`text` 取文本；`json()` 解析 JSON；`content` 取二进制（下载文件）。

3. 进阶技巧：

    - 用 `headers` 模拟浏览器；`timeout` 防止卡死；

    - `Session` 保持会话；异常处理提升健壮性；

    - `response.encoding` 解决中文乱码。

4. 核心优势：语法简洁、功能全面，是 Python 处理 HTTP 请求的首选库，覆盖接口测试、爬虫、后端对接等所有 HTTP 场景。
> （注：文档部分内容可能由 AI 生成）