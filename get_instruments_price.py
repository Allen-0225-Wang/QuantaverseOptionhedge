import requests

def get_option_market_data(instrument_name):
    # Deribit API URL
    url = "https://www.deribit.com/api/v2/public/get_order_book"
    
    # 请求参数
    params = {
        "instrument_name": instrument_name
    }
    
    # 发送 GET 请求
    response = requests.get(url, params=params)
    
    # 确保请求成功
    if response.status_code == 200:
        data = response.json()
        if data['result']:
            return data['result']
        else:
            print("未找到相关数据")
    else:
        print("请求失败:", response.status_code)

# 示例：获取特定期权的市场数据
instrument_name = "ETH-5SEP25-4500-C"  # 替换为您想查询的期权名称
market_data = get_option_market_data(instrument_name)

if market_data:
    print(f"期权 {instrument_name} 的市场数据: {market_data}")

