from mcp.server.fastmcp import FastMCP
from util import (
    stock_sse_summary,
    stock_individual_info,
    stock_real_spot,
    stock_real_a,
    stock_list_a,
)

# Create an MCP server
mcp = FastMCP("Stock-MCP")


@mcp.tool()
def get_sse_summary() -> str:
    """获取A股市场总览（上交所和深交所数据）"""
    return stock_sse_summary()


@mcp.tool()
def get_stock_info(symbol: str = "600519") -> str:
    """获取个股公司概况信息
    
    参数:
    - symbol: 股票代码（6位数字，如600519）
    """
    return stock_individual_info(symbol)


@mcp.tool()
def get_stock_realtime() -> str:
    """获取A股全部实时行情数据"""
    return stock_real_spot()


@mcp.tool()
def get_stock_price(symbol: str = "600519") -> str:
    """获取个股实时价格
    
    参数:
    - symbol: 股票代码（6位数字或带交易所前缀，如600519或SH600519）
    """
    return stock_real_a(symbol)


@mcp.tool()
def get_stock_history(symbol: str = "600519") -> str:
    """获取个股80天历史行情数据
    
    参数:
    - symbol: 股票代码（6位数字，如600519）
    """
    return stock_list_a(symbol)


if __name__ == "__main__":
    mcp.run(transport="sse")
