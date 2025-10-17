import requests

def get_instruments():
    url = "https://www.deribit.com/api/v2/public/get_instruments"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['result']
    else:
        print("请求失败:", response.status_code)

# 获取并打印期权链
instruments = get_instruments()
if instruments:
    for instrument in instruments:
        print(instrument)

