import os, json

#from aibot.lib import DataSet##
from aibot import AiTrading

from DataCrawler.dataset import DataSet

BOTS_PATH = os.path.join(os.getcwd(), "aibot/data/bots/")


class TasksHandler():
    def __init__(self,conn, name: str = "", query: dict = {}) -> None:
        self._conn = conn
        self._name = name
        self._query = query
        self._tasks = {}

        self.__dataset = DataSet()
        
        try:
            func = getattr(self, f"do_{name.replace('-', '_')}")
        except AttributeError:
            self.report("Invalid Taskname !!")
        else:
            func()
        

    def report(self, msg: str = "", done: bool = False, is_client_msg: bool = False, data: list | dict = []):
        self._conn.send({
            "name": self._name,
            "done": done,
            "msg": msg,
            "body": data,
            "is_client_msg": is_client_msg,
        })

    def do_client_is_open(self):
        self.report("Hello from WebSocket")

    def do_client_is_closed(self):
        self._conn.close()
        
    def do_bot_create(self): 
        data = self._query.get("data")
        name, lr, gamma, hidden_layers = data.get("name"), data.get("lr"), data.get("gamma"), data.get("hidden_layers")

        bots = os.listdir(BOTS_PATH)

        if name in bots:
            self.report(f"Bot {name} already exists !!", is_client_msg=True)
            
            return None
        
        if name is None or lr is None or gamma is None or hidden_layers is None:
            self.report(f"Please fill all inputs provided !!", is_client_msg=True)
            return None

        BOT_PATH = os.path.join(BOTS_PATH, name)
        os.mkdir(BOT_PATH)

        # Create config file
        with open(os.path.join(BOT_PATH, "config.json"), "w+") as f:
            json.dump({
                "info": data,
                "defaults": {
                    "training": {
                        "balance": 1000.00,
                        "batch_size": 1000,
                        "train_data_percentage": 80,
                        "max_episodes": 30,
                        "period": "D1",
                        "symbol": "EURUSD",
                        "min_episodes": 10
                    },
                },
                "counter": {
                    "amount_trades": 0,
                    "amount_trainings": 0,
                    "amount_episodes": 0,
                },
                "records": {
                    "max_episodes": 0,
                    "max_balance": 0,
                    "max_profit": 0,
                }
            }, f, indent=2)

        self.report(f"Bot {name} has been successfully created !!", True, True)
        
    def do_bot_get_all(self): 
        bots = os.listdir(BOTS_PATH)

        bots_info = []

        for b in bots:
            config_bot_path = os.path.join(BOTS_PATH, f"{b}/config.json")

            with open(config_bot_path) as f:
                data = json.loads(f.read())
                          
            info = { 'name': b, 'info': data }
            bots_info.append(info)

        self.report(done=True, data=bots_info)

    def do_bot_get_config(self):
        bot_name = self._query.get("name")

        bots = os.listdir(BOTS_PATH)

        if bot_name not in bots:
            self.report("Bot could not be found !!!", is_client_msg=True)
            return None

        config = open(os.path.join(BOTS_PATH, f"{bot_name}/config.json"))
        config_data = json.loads(config.read())
        config.close()

        self.report(data=config_data)

    def do_training_datasets_load(self):
        data = self._query.get("data")
        data = self.__dataset.getSymbol(**data)
    
        self.report(data=data)

    def do_training_datasets_symbols(self): 
        data = self.__dataset.list_symbols_available()
        self.report(data=data)

    def do_training_datasets_periods(self): 
        symbol = self._query.get("symbol")
        periods = self.__dataset.getSymbolPeriodsByName(symbol)
        self.report(data=periods)

    def do_training_start(self): 
        config = self._query.get("config")

        if config is None:
            return None

        bot_name = config.get("bot")
        bot_path = os.path.join(BOTS_PATH, f"{bot_name}/config.json")

        bot_config = None

        with open(bot_path) as f:
            bot_config = json.loads(f.read())

        ai = AiTrading(self, bot_config=bot_config, **config)
        result = ai.start_training()
        self.report(result, is_client_msg=True)

    def do_modal_training_load(self):
        # bots, symbols, period

        bots = os.listdir(BOTS_PATH)
        symbols = self.__dataset.list_symbols_available

        self.report(data={
            "bots": bots,
            "symbols": symbols,
        })

