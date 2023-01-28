from backend import WebSocket


def main(): 
    sock = WebSocket(server_name="ws://ws.app-trading:9000")
    sock.run()


if __name__ == '__main__': main()