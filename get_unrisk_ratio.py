import requests

def get_deribit_risk_free_rate():
    """
    获取 Deribit 的无风险利率
    """
    url = "https://www.deribit.com/api/v2/public/get_index"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # 提取无风险利率
        if 'result' in data and 'risk_free_rate' in data['result']:
            risk_free_rate = data['result']['risk_free_rate']
            return risk_free_rate
        else:
            print("未找到无风险利率信息")
    else:
        print(f"请求失败，状态码: {response.status_code}")

    return None

# 获取并打印无风险利率
risk_free_rate = get_deribit_risk_free_rate()
if risk_free_rate is not None:
    print(f"Deribit 无风险利率: {risk_free_rate:.4f}")

