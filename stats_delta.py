import math
import numpy as np
from scipy.stats import norm

def ceil_to_two_decimal(value):
    return math.ceil(value * 100) / 100

def floor_to_two_decimal(value):
    return math.floor(value * 100) / 100

def calculate_delta(option_type, S, K, T, r, sigma):
    """
    计算期权的 Delta
    :param option_type: 'call' 或 'put'
    :param S: 当前基础资产价格
    :param K: 期权行权价格
    :param T: 到期时间（以年为单位）
    :param r: 无风险利率
    :param sigma: 波动率
    :return: 期权的 Delta
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    
    if option_type == 'call':
        delta = norm.cdf(d1)
    elif option_type == 'put':
        delta = norm.cdf(d1) - 1
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    return delta
