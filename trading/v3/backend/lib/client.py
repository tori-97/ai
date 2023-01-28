import socket, json
from threading import Thread

from backend.lib.frame import WebSocketFrame
from backend.tasks.handler import TasksHandler

class WebSocketClient(Thread):
    def __init__(self, conn: socket.socket, host: str, port: int) -> None:
        super().__init__()

        self._conn = conn
        self._host = host
        self._port = port

        self.is_live = True

    def connect(self):
        while self.is_live:
            print("Listenning to client...")
            request = WebSocketFrame(self.recv())

            if request.is_none() or request == "client-is-closed":
                self.is_alive = False
                print("Conecction will be deactivated")
                break

            # Verify tasks and distribuit it
            data = request.decode()

            try:
                TasksHandler(self, **data)
            except TypeError:
                pass

        self._conn.close()
    
    def recv(self):
        while True:
            data = self._conn.recv(1024)

            if len(data) < 1024:
                break
        
        return data

    def send(self, data: dict):  
        frame = WebSocketFrame(data)
        self._conn.send(frame.encode())

    def run(self):
        self.connect()
