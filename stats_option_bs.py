import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def black_scholes_call_price(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def implied_volatility_call(S, K, T, r, market_price):
    # 定义目标函数
    def objective_function(sigma):
        return black_scholes_call_price(S, K, T, r, sigma) - market_price
    
    # 使用 Brent 方法求解隐含波动率
    try:
        iv = brentq(objective_function, 1e-6, 1)  # 设定波动率范围
        return iv
    except ValueError:
        return None

# 示例参数
S = 4405.75  # 当前标的资产价格
K = 4500  # 行权价格
T = 1 / 365  # 到期时间（年）
r = 0.02388     # 无风险利率
market_price = 0.0035  # 期权市场价格

# 计算隐含波动率
iv = implied_volatility_call(S, K, T, r, market_price)
print(f"隐含波动率: {iv:.2%}" if iv is not None else "未能找到隐含波动率")

