from threading import Thread
import socket, json

from websocket.lib.frame import WebSocketFrame
from websocket.lib.tasks_handler import TasksHandler



class WebSocketClient(Thread):
    def __init__(self, conn: socket.socket, host: str, port: int) -> None:
        super().__init__()

        self._conn = conn
        self._host = host
        self._port = port
    
        self._is_running = True

        self._valid_queries = [
            "hello",
            "heartbeat",
            "start-training",
            "close"
        ]

    def stop_conn(self):
        self._is_running = False
        self._conn.close()

    @property
    def is_running(self):
        return self._is_running

    def send(self, message):

        if isinstance(message, dict):
            message = json.dumps(message)

        frame = WebSocketFrame(message).encode()

        self._conn.send(frame)

        while True:
            response = self.recv().decode()
            task = response.get("task")

            if task is not None and task == "confirm-query":
                break

        return True

    def recv(self):
        data = None
            
        while True:
            data = self._conn.recv(1024)

            if len(data) < 1024:
                break           
        
        frame = WebSocketFrame(data)

        return frame

    def run(self):
        print("[+] Connection established with the client !!")

        while self._is_running:
            print("[+] listenning for messages from client...")
            
            income_request = self.recv()

            if income_request.is_none():
                print("connection closed... ")
                self.stop_conn()
                break

            request = income_request.decode()
            query = request.get("query")

            if query is None:
                print(f"[+] Invalid query: {query}")
                continue

            print(f"[+] New query: {query} | {request}")

            TasksHandler(self, query, request)
       
        self.stop_conn()