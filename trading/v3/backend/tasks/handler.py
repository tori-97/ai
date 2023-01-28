import json

from backend.tasks import Tasks

class TasksHandler():
    """
    request:
        {
            query: string,
            view: string,
            params: {custom?}
        }

    response:
        {
            name: query,
            view: string, 
            done: boolean,
            data: {custom?},
            client_msg: string | null,
            inner_task: task
        }
    """
    def __init__(self, client, query: str, view: str, params: str) -> None:
        
        self.query     = query
        self.view      = view 
        self.params    = json.dumps(params) if params is not None else None

        self._client   = client
        
        Tasks(self)

    def report(self, 
        client_msg: str or None = None, 
        done: bool = False, 
        data: dict or None = None, 
        inner_task: dict or None = None
    ):
        self._client.send(json.dumps({
            'name': self.query,
            'view': self.view,
            'done': done,
            'data': data,
            'client_msg': client_msg,
            'inner_task': inner_task
        }))

