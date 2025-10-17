import ccxt

# 创建 Binance 交易所实例
binance = ccxt.binance()

# 加载市场
markets = binance.load_markets()

# 获取所有非永续合约
non_perpetual_contracts = [symbol for symbol in markets if 'PERPETUAL' not in symbol]

# 打印非永续合约
for contract in non_perpetual_contracts:
    print(contract)

