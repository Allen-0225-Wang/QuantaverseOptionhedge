import websocket
import json

def on_message(ws, message):
    """处理接收到的消息"""
    data = json.loads(message)
    print(data)

def on_error(ws, error):
    """处理错误消息"""
    print(f"错误: {error}")

def on_close(ws):
    """处理关闭连接"""
    print("连接已关闭")

def on_open(ws):
    """打开连接时的操作"""
    print("连接已打开")

if __name__ == "__main__":
    # 创建 WebSocket 连接
    symbol = "btcusdt"  # 您可以更改为其他交易对，注意是小写
    #ws_url = f"wss://stream.binance.com:9443/ws/{symbol}@bookTicker"
    ws_url = f"wss://stream.binance.com:9443/ws/{symbol}@orderbook"
    
    # 初始化 WebSocket
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    # 运行 WebSocket
    ws.run_forever()
