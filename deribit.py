import requests
import json
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, time, timedelta

def get_deribit_instruments(currency='BTC', kind='option', expired=False):
    """
    获取 Deribit 交易所的期权合约列表
    """
    url = "https://deribit.com/api/v2/public/get_instruments"
    params = {
        'currency': currency,
        'kind': kind,
        'expired': str(expired).lower()
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data['result']:
        return pd.DataFrame(data['result'])
    else:
        print("Error fetching instruments:", data.get('error', 'Unknown error'))
        return pd.DataFrame()

def get_deribit_orderbook(instrument_name):
    """
    获取特定期权合约的订单簿数据
    """
    url = "https://deribit.com/api/v2/public/get_order_book"
    params = {
        'instrument_name': instrument_name
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'result' in data:
        return data['result']
    else:
        print("Error fetching order book:", data.get('error', 'Unknown error'))
        return None

def get_deribit_index_price(currency='BTC'):
    """
    获取指数价格
    """
    url = "https://deribit.com/api/v2/public/get_index_price"
    params = {
        'index_name': f'{currency.lower()}_usd'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    
    if 'result' in data:
        return data['result']['index_price']
    else:
        print("Error fetching index price:", data.get('error', 'Unknown error'))
        return None


if __name__ == '__main__':
    #ddf = get_deribit_instruments()
    #print(ddf)

    ## test get orderbook
    optioname = 'ETH-9SEP25-4450-C'
    ob = get_deribit_orderbook(optioname)
    print(ob)

    #markprice = get_deribit_index_price('ETH')
    #print(markprice)

