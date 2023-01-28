import socket,re
from hashlib import sha1
from base64 import b64encode

from websocket.lib import WebSocketClient, SocketResponse


class WebSocket():
    def __init__(self, 
        host: str = '127.0.0.1', 
        port: int = 9001, 
        backlog: int = 8,
        max_clients: int = 1
        
        ) -> None:
        
        self._host, self._port = host, port
        self._backlog = backlog
        self._max_clients = max_clients
        self._is_running = True

        self._clients = []

    def _create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock

    def do_websocket_handshake(self, conn, payload: SocketResponse):
        id = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        key = payload.headers.get("sec-websocket-key")

        # calculate accept key
        tmp = sha1((key + id).encode()).digest()
        client_key = b64encode(tmp).decode()
        
        response = "HTTP/1.1 101 Switching Protocols\r\n"
        response += "Upgrade: websocket\r\n"
        response += "Connection: Upgrade\r\n"
        response += f"Sec-WebSocket-Accept: {client_key}\r\n"
        response += f"Sec-WebSocket-Version: 13\r\n"
        response += "Sec-WebSocket-Protocol: chat\r\n"
        response += "\r\n"

        conn.send(response.encode())

        return True

    def stop_connection(self, current_conn):
        self._is_running = False
        current_conn.close()
    
    def stop_server(self):
        self._sock.close()

    def clean_clients(self):
        # Check if clients are still alive !!
        for c in self._clients:
            if not c.is_running:
                self._clients.pop(self._clients.index(c))
        
    def serve(self, buffer_size: int = 5000):
        # Prepare Socket & active it
        self._sock = self._create_socket()
        self._sock.bind((self._host,self._port))
        self._sock.listen(self._backlog)

        while self._is_running:
            print(f"[+] Websocket is listenning for connections on ws://{self._host}:{self._port}/")
            conn, addr = self._sock.accept()
            done = False

            if conn:
                print("="*50)
                # Parse query
                data = conn.recv(5000)
                req = SocketResponse(data)

                if req.query == "/trading":
                    if req.method == "GET":
                        # Prints needs to be changed to logger
                        print(f"[+] New connection {addr[0]}:{addr[1]} with trading-app !!")
                        print("[+] try do handshake...")
                        done = self.do_websocket_handshake(conn, req)
                        print(f"[+] Handshake done: {done}")

                        client = WebSocketClient(conn, addr[0], addr[1])

                        if client not in self._clients and len(self._clients) < self._max_clients:
                            self._clients.append(client)
                            client.start()
                else:
                    print("[+] Invalid Request")
                    conn.close()
                print("="*50)

            # Clean closed sessions
            self.clean_clients()
            print(f"[+] Current clients amount: {len(self._clients)}")


        self.stop_server()



__all__ = [
    "WebSocket"
]