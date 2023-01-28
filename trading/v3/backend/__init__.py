import socket, re
from hashlib import sha1
from base64 import b64encode

from backend.lib import WebSocketClient

class WebSocket():
    DEFAULTS = {
        "host": "127.0.0.1",
        "port": 9000,
    }
    def __init__(self, 
        host: str = "127.0.0.1", 
        port: int = 9000,
        server_name: str = None
    ) -> None:

        # Configuration
        self._host, self._port = self.__parse_servername(server_name) if server_name is not None else self.__parse_hostname(host, port)
        self._backlog = 2
        self._buffersize = 1024

        # # Socket
        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__prepare_socket()

        self.is_running = True

    def __prepare_socket(self):
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self._host, self._port))
        self._socket.listen(self._backlog)

    def __parse_servername(self, name: str):
        host = self.DEFAULTS['host']
        port = self.DEFAULTS['port']

        if name is not None and not re.match(r"ws://(.*)\:([0-9]+)", name):
            raise "Invalid Protocoll !! Please only use ws://<url>:<port>"

        data = name.split("ws://")[1].split(":")
        host = data[0]
        port = data[1]

        return self.__parse_hostname(host, port) 

    def __parse_hostname(self, hostname: str, port: int):
        try:
            return socket.gethostbyname(hostname), int(port)
        except Exception as e:
            print(f"Error {e} with: {hostname} !!")

        return (self.DEFAULTS['host'], self.DEFAULTS['port'])

    def __parse_headers(self, headers: list):
        _headers = {}

        for h in headers:
            try:
                k, v = h.split(": ")
                _headers[k.lower()] = v
            except ValueError:
                pass
        
        return _headers

    def __parse_payload(self, data: str):
        lines = data.split("\r\n")

        try:
            methods, path, version = lines[0].split(" ")
        except ValueError:
            methods, path, version = None, None, None

        headers = self.__parse_headers(lines[1:-1])
        
        return {
            "method": methods,
            "path": path,
            "version": version,
            "headers": headers
        }

    def __prepare_response(self, accept_key: str):
        response = "HTTP/1.1 101 Switching Protocols\r\n"
        response += "Upgrade: websocket\r\n"
        response += "Connection: Upgrade\r\n"
        response += f"Sec-WebSocket-Accept: {accept_key}\r\n"
        response += f"Sec-WebSocket-Version: 13\r\n"
        response += "Sec-WebSocket-Protocol: chat\r\n"
        response += "\r\n"
        return response.encode()

    def __do__handshake(self, conn: socket.socket, payload: dict):
        id = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        client_key = payload['headers']['sec-websocket-key']

        # calculate accept_key
        accept_key = b64encode(sha1((client_key + id).encode()).digest()).decode()

        # prepare response
        response = self.__prepare_response(accept_key)
        conn.send(response)

        return True

    def __try_connection(self, conn: socket.socket, host: str, port: int):
        print(f"[+] New Connection with [{host}:{port}]")    

        # parse request
        data = conn.recv(self._buffersize).decode()
        payload = self.__parse_payload(data)
        # do handshake

        if payload['path'] != "/":
            return False, "[!] Invalid Path"

        done = self.__do__handshake(conn, payload)

        if not done:
            conn.close()
            return False, "[!] Handshake failed."

        # setup connection
        new_client = WebSocketClient(conn, host, port)
        new_client.run()

    def run(self):

        while self.is_running:
            print(f"[+] Listening at {self._host}:{self._port}")

            conn, addr = self._socket.accept()

            if conn:
                self.__try_connection(conn, addr[0], addr[1])
            
            print("[+] next connection...")
        