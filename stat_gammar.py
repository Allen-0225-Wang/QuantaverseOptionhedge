import numpy as np
from scipy.stats import norm

def calculate_gamma(S, K, T, r, sigma):
    """
    计算期权的 Gamma
    :param S: 当前基础资产价格
    :param K: 期权行权价格
    :param T: 到期时间（以年为单位）
    :param r: 无风险利率
    :param sigma: 波动率
    :return: 期权的 Gamma
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    N_prime_d1 = norm.pdf(d1)  # 计算标准正态分布的概率密度函数
    
    gamma = N_prime_d1 / (S * sigma * np.sqrt(T))
    
    return gamma
