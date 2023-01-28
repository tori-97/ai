from time import sleep
from threading import Thread, Lock

from tools.DataCrawler import Manager
from tools.AiTrader.lib import TrainingRoom
    
class AiTrading(Thread):
    def __init__(self, 
        handler, 
        symbol: str = "EURUSD", period: str = "H1", train_data_amount: int = 1, shuffled: bool = False,
        min_threads: int = 1, run_forever: bool = False, 
        **training_config
    ) -> None:
        super().__init__()

        self.paused             = False
        self._killed            = False
        self._locker            = Lock()
        self._handler           = handler
        self._manager           = Manager()

        # Trading Config
        self._symbol            = symbol
        self._period            = period
        self._shuffled          = shuffled
        self._run_forever       = run_forever
        self._min_threads       = min_threads
        self._config            = training_config
        self._train_data_amount = train_data_amount

        self._trainings_threads: list[TrainingRoom] = []

    def pause(self, on: bool = False):
        if on:
            self.paused = True
        else:
            self.paused = False
    
    def kill(self): 
        for room in self._trainings_threads:
            room.kill()

        self._killed = True
    
    def _pause(self):
        for room in self._trainings_threads:
            room.pause(True)

        while self.paused:
            print("[+] MainThread paused !!")

            if self._killed:
                self.paused = False

            self._handler.report(inner_task={
                "name": "status",
                "data": "paused"
            })  

            sleep(1)
        
        for room in self._trainings_threads:
            room.pause(False)

        self._locker.release()

    def load_data(self):
        data, msg = self._manager.getSymbol(self._symbol, self._period, self._train_data_amount, self._shuffled)

        print(self._symbol, self._train_data_amount)

        if data is None:
            self._handler.report(msg, False)

            return [], False

        days = list(map(lambda x: x.get("time"), data))
        closes = list(map(lambda x: x.get("close"), data))

        self._handler.report(
            inner_task={
                "name": "load-data",            
                "data":{
                    "days": days,
                    "closes": closes,
                    "symbol": self._symbol
                }
        })

        return data, True

    def set_speed(self, amount: float):
        for t in self._trainings_threads:
            t.training_speed = amount
        

    def run(self): 
        train_data, check = self.load_data()
        # symbol=EURUSD,period=H1,train_data_amount=10,balance=1000,min_balance=2000,lr=0.002,gamma=0.98,batch_size=10,min_episodes=10,max_episodes=20

        if not check:
            print("Something wents wrongs")
            return None

        # print(f"Train data amount: {self._train_data_amount}")
        # create all threads:
        for i in range(1, self._min_threads + 1):
            thread = TrainingRoom(self._handler, train_data, **self._config)
            thread.name = f"bot_{i}"
            thread.start()
            self._trainings_threads.append(thread)

        threads_names = list(map(lambda x: x.name, self._trainings_threads))            

        self._handler.report(inner_task={
            "name": "load-bots",
            "data": threads_names
        })

        sleep(2)
        
        print("[+] Trading simulation is online !!")
        self._handler.report(inner_task={
            "name": "status",
            "data": "active"
        })  

        max_episodes, max_balance = 0, 0

        while not self._killed:
            if self.paused:
                self._locker.acquire()
                self._pause()

            if self._run_forever and len(self._trainings_threads) < self._min_threads:
                thread = TrainingRoom(self._handler, train_data, **self._config)
                thread.start()
                self._trainings_threads.append(thread)

            for t in self._trainings_threads:
                if not t.is_alive():

                    if float(t.env.balance) > float(max_balance):
                        max_balance = t.balance
                        t.agent.save_current_status()
                    
                    if int(t.current_episode) > int(max_episodes):
                        max_episodes = t.current_episode
                        t.agent.save_current_status()                   

                    self._trainings_threads.pop(self._trainings_threads.index(t))
            sleep(1)

            if len(self._trainings_threads) == 0:
                self.kill()

        print("Trading simulation is offline !!")
                
        self._handler.report(inner_task={
            "name": "status",
            "data": "stopped"
        })  