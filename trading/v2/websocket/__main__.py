from websocket import WebSocket
import os

def main():
    os.system("clear")
    
    ws = WebSocket(max_clients=10)
    ws.serve()


if __name__ == '__main__': 
    main()