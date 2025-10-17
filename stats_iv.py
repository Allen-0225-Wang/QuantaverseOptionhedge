from deribit import *
from stats_delta import *
from stat_iv_back67 import *
from stat_gammar import *

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Black-Scholes 期权定价模型
    """
    if T <= 0:
        if option_type == 'call':
            return max(S - K, 0)
        else:
            return max(K - S, 0)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return price

def black_scholes_vega(S, K, T, r, sigma):
    """
    计算 Vega (对波动率的导数)
    """
    if T <= 0:
        return 0
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T)

def implied_volatility_bs(S, K, T, r, market_price, option_type='call'):
    """
    使用数值方法计算隐含波动率
    """
    # 定义计算误差的函数
    def error_function(sigma):
        return black_scholes(S, K, T, r, sigma, option_type) - market_price
    
    # 设置波动率搜索范围
    sigma_low = 1e-6
    sigma_high = 1.0
    
    try:
        # 使用布伦特方法求解
        implied_vol = brentq(error_function, sigma_low, sigma_high, xtol=1e-6)
        return implied_vol
    except ValueError:
        # 如果找不到解，返回 NaN
        print(f'no answer')
        return np.nan

def calculate_deribit_iv(instrument_name, risk_free_rate=0.0):
    """
    计算 Deribit 期权的隐含波动率
    """
    # 获取订单簿数据
    orderbook = get_deribit_orderbook(instrument_name)
    if not orderbook:
        return np.nan
    
    S = round(orderbook['underlying_price'], 2)
    mark = orderbook['mark_price']
    b_iv = orderbook['bid_iv'] / 100
    a_iv = orderbook['ask_iv'] / 100
    m_iv = orderbook['mark_iv'] / 100
    if not S:
        return np.nan
    
    # 解析期权信息
    parts = instrument_name.split('-')
    expiry_str = parts[1]
    strike = float(parts[2])
    option_type = parts[3].lower()
    option_type = 'call' if option_type == 'c' else 'put'
    
    # 计算到期时间（年）
    expiry_date = datetime.strptime(expiry_str, '%d%b%y')
    expiry_date = datetime.combine(expiry_date, time(8, 0))
    now = datetime.utcnow()
    expiry_time = expiry_date - now
    if expiry_time.days >= 1:
        T = (expiry_time.seconds // 60 + 1) / (365 * 24 * 60)
        T = T + (expiry_time.days) / 365
    else:
        T = (expiry_time.seconds // 60 + 1) / (365 * 24 * 60)
    
    bid_marketprice = S * orderbook['bids'][0][0]
    ask_marketprice = S * orderbook['asks'][0][0]
    mark_price = round(S * mark, 2)

    #bid_marketprice = round(S * orderbook['bids'][0][0], 2)
    #ask_marketprice = round(S * orderbook['asks'][0][0], 2)
    
    # 计算隐含波动率
    print(S)
    print(strike)
    print(expiry_date)
    print(now)
    print(expiry_time.days)
    print(T)
    print(risk_free_rate)
    print(mark_price)
    print(bid_marketprice)
    print(ask_marketprice)
    print(option_type)
    bid_iv = implied_volatility('call', bid_marketprice, S, strike, T, risk_free_rate)
    ask_iv = implied_volatility('call', ask_marketprice, S, strike, T, risk_free_rate)
    mark_iv = implied_volatility('call', mark_price, S, strike, T, risk_free_rate)
    print(f'{instrument_name}_bidiv={bid_iv}')
    print(f'{instrument_name}_askiv={ask_iv}')
    print(f'{instrument_name}_markiv={mark_iv}')
    print(f'diff_{instrument_name}={round(b_iv, 4) - bid_iv}')
    print(f'diff_{instrument_name}={round(a_iv, 4) - ask_iv}')
    print(f'diff_{instrument_name}={round(m_iv, 4) - mark_iv}')
    
    call_delta = calculate_delta('call', S, strike, T, risk_free_rate, mark_iv)
    put_delta = calculate_delta('put', S, strike, T, risk_free_rate, mark_iv)
    print(f'{instrument_name}_call_delta={round(call_delta, 2)}')
    print(f'{instrument_name}_put_delta={round(put_delta, 2)}')

    gammar = calculate_gamma(S, strike, T, risk_free_rate, mark_iv)
    print(f'gammar={gammar}')

    return bid_iv, ask_iv


if __name__ == '__main__':
    optioname = 'ETH-28NOV25-4500-C'
    calculate_deribit_iv(optioname)

