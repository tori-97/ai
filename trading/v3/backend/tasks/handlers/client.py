class Client():
    def __init__(self, handler) -> None:
        self.handler = handler

    def do_is_open(self):
        self.handler.report("Hello from backend")

    def do_is_closed(self):
        self.handler.report("Bye from backend")

