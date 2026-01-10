# Stock-MCP

一个基于 MCP (Model Context Protocol) 的 A 股数据服务器，提供实时股票行情、个股信息、历史数据等功能。

## 项目简介

Stock-MCP 是一个 MCP 服务器实现，集成了 AKShare 数据源，为 Claude 等 AI 助手提供 A 股市场数据接口。通过该服务器，可以轻松获取：

- A 股市场总览数据（上交所和深交所）
- 个股公司概况信息
- 实时行情数据
- 个股实时价格
- 个股 80 天历史行情数据

## 系统要求

- Python >= 3.10
- pip 或 uv 包管理器

## 安装指南

### 方式一：使用 uv（推荐）

uv 是一个快速的 Python 包管理器，安装和依赖解析速度更快。

1. **安装 uv**（如果未安装）

   ```bash
   pip install uv --upgrade
   ```

   或使用腾讯源加速：

   ```bash
   pip install uv --upgrade -i https://mirrors.cloud.tencent.com/pypi/simple
   ```

2. **同步项目依赖**

   ```bash
   uv sync
   ```

### 方式二：使用 pip

```bash
pip install -r requirements.txt
```

或使用腾讯源加速：

```bash
pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
```

## 依赖说明

- **akshare** (>=1.18.8)：A 股数据获取库，提供实时行情、历史数据等
- **mcp** (>=1.25.0)：Model Context Protocol 框架，用于构建 MCP 服务器

## 快速开始

### 启动服务器

```bash
python main.py
```

服务器将通过 SSE (Server-Sent Events) 传输启动，默认监听本地连接。

## 可用工具

### 1. get_sse_summary()

获取 A 股市场总览数据（上交所和深交所）

**参数：** 无

**返回：** JSON 格式的市场总览数据，包含涨跌家数、成交量等信息

**示例：**
```python
result = get_sse_summary()
```

### 2. get_stock_info(symbol)

获取个股公司概况信息

**参数：**
- `symbol` (str)：股票代码，6 位数字，如 `600519`（默认值）

**返回：** JSON 格式的公司信息，包含公司名称、行业、主营业务等

**示例：**
```python
result = get_stock_info("600519")  # 贵州茅台
result = get_stock_info("000858")  # 五粮液
```

### 3. get_stock_realtime()

获取 A 股全部实时行情数据

**参数：** 无

**返回：** JSON 格式的全市场实时行情数据

**示例：**
```python
result = get_stock_realtime()
```

### 4. get_stock_price(symbol)

获取个股实时价格

**参数：**
- `symbol` (str)：股票代码，6 位数字或带交易所前缀，如 `600519` 或 `SH600519`（默认值）

**返回：** JSON 格式的实时价格数据，包含当前价、涨跌幅、成交量等

**示例：**
```python
result = get_stock_price("600519")      # 上交所股票
result = get_stock_price("SH600519")    # 带前缀
result = get_stock_price("000858")      # 深交所股票
```

### 5. get_stock_history(symbol)

获取个股 80 天历史行情数据

**参数：**
- `symbol` (str)：股票代码，6 位数字，如 `600519`（默认值）

**返回：** JSON 格式的历史行情数据，包含日期、开盘价、收盘价、最高价、最低价、成交量等

**示例：**
```python
result = get_stock_history("600519")  # 获取贵州茅台 80 天历史数据
```

## 股票代码说明

### 交易所前缀

- **SH**：上海交易所（Shanghai）
- **SZ**：深圳交易所（Shenzhen）

### 常见股票代码示例

| 股票名称 | 代码 | 完整代码 |
|---------|------|---------|
| 贵州茅台 | 600519 | SH600519 |
| 五粮液 | 000858 | SZ000858 |
| 中国平安 | 601318 | SH601318 |
| 招商银行 | 600036 | SH600036 |
| 腾讯控股 | 00700 | HK00700 |

## 项目结构

```
stock-mcp/
├── main.py              # MCP 服务器主文件，定义所有工具
├── util.py              # 工具函数实现，调用 AKShare API
├── pyproject.toml       # 项目配置和依赖声明
├── uv.lock              # uv 依赖锁定文件
├── README.md            # 项目文档
├── LICENSE              # 许可证
└── .gitignore           # Git 忽略文件
```

## 使用示例

### 在 Claude 中使用

1. 在 Claude 的 MCP 配置中添加此服务器
2. 配置 SSE 传输方式
3. 在对话中使用相关工具获取股票数据

### 直接调用

```python
from main import mcp

# 获取市场总览
summary = get_sse_summary()
print(summary)

# 获取个股信息
info = get_stock_info("600519")
print(info)

# 获取实时价格
price = get_stock_price("600519")
print(price)

# 获取历史数据
history = get_stock_history("600519")
print(history)
```

## 常见问题

### Q: 如何加速包安装？

A: 使用腾讯源或其他国内镜像源：

```bash
pip install -i https://mirrors.cloud.tencent.com/pypi/simple package_name
```

或配置 pip 配置文件 `~/.pip/pip.conf`：

```ini
[global]
index-url = https://mirrors.cloud.tencent.com/pypi/simple
```

### Q: 数据来源是什么？

A: 所有数据来自 AKShare 库，该库聚合了多个数据源，提供免费的 A 股数据。

### Q: 如何处理网络错误？

A: 确保网络连接正常，AKShare 依赖网络获取实时数据。如果频繁出现错误，可能是数据源暂时不可用。

### Q: 支持哪些股票代码格式？

A: 支持 6 位数字代码（如 `600519`）和带交易所前缀的代码（如 `SH600519`、`SZ000858`）。

## 许可证

详见 LICENSE 文件

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [AKShare 文档](https://akshare.akfamily.xyz/)
- [Python 官方文档](https://docs.python.org/3/)