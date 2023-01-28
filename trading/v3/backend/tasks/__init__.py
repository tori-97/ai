from backend.tasks import handlers

from threading import Thread

class Tasks():
    def __init__(self, handler) -> None:
        self.handler = handler

        cmd_route = self.handler.query.split(".")[0]
        cmd_event = "_".join(self.handler.query.split(".")[1::])

        print(f"CMD: {cmd_route} EVENT: {cmd_event}")

        self.redirect_to_task(cmd_route, cmd_event)

    def redirect_to_task(self, route, event):
        try:
            obj = getattr(handlers, route.capitalize())
        except AttributeError:
            print("Task don't exists !!")
            pass
        else:
            o = obj(self.handler)
            
            try:
                func = getattr(o, f"do_{event}")
            except AttributeError:
                self.handler.report("Invalid task name !!")
                pass
            else:
                # Add thread here to use multi threading
                thread = Thread(target=func)
                thread.start()
