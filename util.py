import akshare as ak
from datetime import datetime, timedelta

def proceee_code(stock_code):
    """
    给A股6位数字代码添加交易所前缀（SH/SZ/BJ）
    :param stock_code: 输入的A股代码（可传数字/字符串，如601127、"000001"）
    :return: 带交易所前缀的代码（如SH601127、SZ300001）
    :raises ValueError: 输入格式不合法或代码开头不符合A股规则时抛出异常
    """
    # 步骤1：统一转为字符串，去除首尾空格，处理数字输入（如601127→"601127"）
    stock_code_str = str(stock_code).strip()
    
    # 步骤2：校验是否为6位纯数字
    if len(stock_code_str) != 6 or not stock_code_str.isdigit():
        raise ValueError(f"输入的代码「{stock_code}」不合法！必须是6位纯数字（如601127、000001）")
    
    # 步骤3：根据代码开头判断交易所
    first_two = stock_code_str[:2]  # 取前两位（核心判断依据）
    first_one = stock_code_str[:1]
    
    if first_two.startswith("60") or first_two.startswith("68"):
        # 上交所：60开头（主板）、68开头（科创板）
        exchange = "SH"
    elif first_two.startswith("00") or first_two.startswith("30"):
        # 深交所：00开头（主板/中小板）、30开头（创业板）
        exchange = "SZ"
    elif first_one == "8":
        # 北交所：8开头（83/87/88等）
        exchange = "BJ"
    else:
        raise ValueError(f"输入的代码「{stock_code_str}」开头不符合A股规则，无法匹配交易所！")
    
    # 步骤4：拼接并返回结果
    return f"{exchange}{stock_code_str}"

def stock_sse_summary():
    get_sse_md = ak.stock_sse_summary().to_markdown(index=False)
    get_szse_md = ak.stock_szse_summary(date=datetime.now().strftime("%Y%m%d")).to_markdown(index=False)
    return f"""以下是A股的市场总览，分为两部分，第一部分是上海证券交易所的数据：\n{get_sse_md} \n 第二部分是深圳证券交易所的数据： \n {get_szse_md}"""

# 注意字符串类型的symbol
def stock_individual_info(symbol="600519"):
    sources = [
        lambda: ak.stock_individual_basic_info_xq(symbol=process_code(symbol)),
        lambda: ak.stock_individual_info_em(symbol=symbol).to_markdown(index=False)
    ]
    
    for i, source in enumerate(sources, 1):
        try:
            return f"公司概况-公司简介如下:\n{source()}"
        except Exception as e:
            if i == len(sources):
                return f"所有数据源均失败，最后一个错误: {e}"
    
def stock_real_spot():
    sources = [
        lambda: f"获取的A股全部行情数据\n {ak.stock_zh_a_spot().to_markdown(index=False)}",
        lambda: f"获取的A股全部行情数据\n 深圳：{ak.stock_zh_a_spot_em().to_markdown(index=False)}北京{ak.stock_bj_a_spot_em().to_markdown(index=False)}\n新股{ak.stock_new_a_spot_em().to_markdown(index=False)}\n科创{ak.stock_kc_a_spot_em().to_markdown(index=False)}"
    ]
    for i, source in enumerate(sources, 1):
            try:
                return f"{source()}"
            except Exception as e:
                if i == len(sources):
                    return f"所有数据源均失败，最后一个错误: {e}"

#A 股个股代码，A 股场内基金代码，A 股指数，美股代码, 美股指数
def stock_real_a(symbol="600519"):
    if len(symbol)==6:
        symbol = proceee_code(symbol)
    return ak.stock_individual_spot_xq(symbol=symbol).to_markdown(index=False)

def stock_list_a(symbol="600519"):
    symbol = proceee_code(symbol)
    end_time = datetime.now()
    start_time = end_time - timedelta(days=80)
    start_date=start_time.strftime("%Y%m%d")
    end_date=end_time.strftime("%Y%m%d")
    sources = [
        lambda: ak.stock_zh_a_hist_tx(symbol=symbol.lower(), start_date=start_date, end_date=end_date, adjust="").to_markdown(index=False),
        lambda: ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust="").to_markdown(index=False)
    ]
    
    for i, source in enumerate(sources, 1):
        try:
            result = source()
            if result:
                return f"历史行情数据如下:\n{result}"
            else:
                print(f"数据源 {i} 返回空数据")
        except Exception as e:
            print(f"数据源 {i} 错误: {e}")
            if i == len(sources):
                return f"所有数据源均失败，最后一个错误: {e}"
    


if __name__ == "__main__":
    print(stock_list_a())