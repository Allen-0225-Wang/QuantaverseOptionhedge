import numpy as np
from scipy.stats import norm
from scipy.optimize import newton

def black76_call_price(F, K, T, r, sigma):
    """
    计算 Black-76 模型的看涨期权理论价格
    
    参数:
    F: 标的期货价格
    K: 行权价
    T: 到期时间（年）
    r: 无风险利率
    sigma: 波动率
    
    返回:
    call_price: 看涨期权理论价格
    """
    d1 = (np.log(F / K) + (sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = np.exp(-r * T) * (F * norm.cdf(d1) - K * norm.cdf(d2))
    return call_price

def black76_put_price(F, K, T, r, sigma):
    """
    计算 Black-76 模型的看跌期权理论价格
    
    参数:
    F: 标的期货价格
    K: 行权价
    T: 到期时间（年）
    r: 无风险利率
    sigma: 波动率
    
    返回:
    put_price: 看跌期权理论价格
    """
    d1 = (np.log(F / K) + (sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    put_price = np.exp(-r * T) * (K * norm.cdf(-d2) - F * norm.cdf(-d1))
    return put_price

def black76_vega(F, K, T, r, sigma):
    """
    计算 Black-76 模型的 Vega 值（期权价格对波动率的导数）
    
    参数:
    F: 标的期货价格
    K: 行权价
    T: 到期时间（年）
    r: 无风险利率
    sigma: 波动率
    
    返回:
    vega: Vega 值
    """
    d1 = (np.log(F / K) + (sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    vega = F * np.exp(-r * T) * norm.pdf(d1) * np.sqrt(T)
    return vega

def implied_volatility(option_type, market_price, F, K, T, r, initial_sigma=0.5, tol=1e-6, max_iter=1000):
    """
    使用牛顿法计算隐含波动率
    
    参数:
    option_type: 'call' 或 'put'
    market_price: 期权市场价格
    F: 标的期货价格
    K: 行权价
    T: 到期时间（年）
    r: 无风险利率
    initial_sigma: 初始波动率猜测值
    tol: 容差
    max_iter: 最大迭代次数
    
    返回:
    iv: 隐含波动率
    """
    # 定义价格差异函数
    def price_difference(sigma):
        if option_type.lower() == 'call':
            return black76_call_price(F, K, T, r, sigma) - market_price
        elif option_type.lower() == 'put':
            return black76_put_price(F, K, T, r, sigma) - market_price
        else:
            raise ValueError("option_type 必须是 'call' 或 'put'")
    
    # 使用牛顿法求解
    try:
        iv = newton(
            price_difference, 
            initial_sigma, 
            fprime=lambda x: black76_vega(F, K, T, r, x),
            tol=tol,
            maxiter=max_iter
        )
        return max(iv, 1e-6)  # 确保波动率不为负
    except RuntimeError:
        # 如果牛顿法失败，使用二分法作为备选
        return implied_volatility_bisection(option_type, market_price, F, K, T, r)

def implied_volatility_bisection(option_type, market_price, F, K, T, r, low=0.001, high=5.0, tol=1e-6, max_iter=100):
    """
    使用二分法计算隐含波动率（牛顿法的备选方案）
    """
    for i in range(max_iter):
        mid = (low + high) / 2
        if option_type.lower() == 'call':
            price_mid = black76_call_price(F, K, T, r, mid)
        else:
            price_mid = black76_put_price(F, K, T, r, mid)
        
        if abs(price_mid - market_price) < tol:
            return mid
        
        if price_mid < market_price:
            low = mid
        else:
            high = mid
    
    return (low + high) / 2  # 返回最后一次迭代的结果

# 示例使用
if __name__ == "__main__":
    # 示例参数（假设值）
    F = 1  # 比特币期货价格
    K = 1 * (4294 / 4450)  # 行权价
    T = 3/365   # 30天到期（以年为单位）
    r = 0.0     # 无风险利率（在加密货币中常设为0）
    market_price = 0.013 # 观察到的看涨期权市场价格
    
    # 计算隐含波动率
    iv = implied_volatility('call', market_price, F, K, T, r)
    print(f"隐含波动率 (IV): {iv:.4f} ({iv*100:.2f}%)")
    
    # 验证：使用计算出的IV计算理论价格，应与市场价格接近
    theoretical_price = black76_call_price(F, K, T, r, iv)
    print(f"市场价格: {market_price:.4f}")
    print(f"理论价格: {theoretical_price:.4f}")
    print(f"差异: {abs(theoretical_price - market_price):.6f}")
