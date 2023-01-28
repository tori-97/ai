import json

from tools.AiTrader import AiTrading

THREADS: list[AiTrading] = []

class Trainings():
    def __init__(self, handler) -> None:
        self.handler = handler
    
    def do_start(self):
        """
        {
            name: str, 
            traindataamount: int, 
            balance: float, 
            lr: float, 
            gamma: float,
            batch_size: int, 
            min_episodes: int, 
            max_episodes: int, 
            symbol: str, 
            period: str, 
            threads: int
        }
        """

        # self.handler.report("Preparing training")

        thread = AiTrading(self.handler, **json.loads(self.handler.params))
        thread.start()
        THREADS.append(thread)

        # self.handler.report("training started...")

    def do_pause(self):
        for t in THREADS:
            t.pause(True)
        self.handler.report("training paused...")
    
    def do_resume(self):
        for t in THREADS:
            t.pause(False)
        self.handler.report("training resumed...")
    
    def do_stop(self):
        for t in THREADS:
            t.kill()
        self.handler.report("training stopped...")

    def do_set_speed(self):
        speed = json.loads(self.handler.params).get("speed")

        if speed is None:
            return None

        for t in THREADS:
            t.set_speed(speed)

        
        self.handler.report(f"Speed {speed} adjusted !!", done=True)