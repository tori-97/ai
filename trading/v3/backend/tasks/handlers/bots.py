import os, json, shutil
from time import sleep

DATA_PATH = os.path.join(os.getcwd(), "backend/data/bots")

class Bots():
    """
        # Bots:
        - bots-create 
            * params: {
                name: string,
                lr: float,
                hidden_layers: int,
                gamma: float,
                discounter_rate: int
            }
        - bots-update
            * params: {
                name: string or null,
                lr: float or null,
                hidden_layers: int or null,
                gamma: float or null
            }
        - bots-delete
            * params: { name: string }
        - bots-get
            * params: { name: string }   
    """

    def __init__(self, handler) -> None:
        self.handler = handler

    def _params_guard(self):
        params = self.handler.params

        if params is None:
            self.handler.report("You need to provide some parameters !!")
            return False
        
        return True

    def __create_bot_workspace(self, bot_name: str, **params):
        bot_path = os.path.join(DATA_PATH, bot_name)
        model_path = os.path.join(DATA_PATH, f"{bot_name}/model")
        trainings_path = os.path.join(DATA_PATH, f"{bot_name}/trainings")

        os.mkdir(bot_path)
        os.mkdir(model_path)
        os.mkdir(trainings_path)

        self.__create_bot_config(**params)

    def __create_bot_config(self, name: str, lr: float = 0.0025, hidden_layers: int = 43, gamma: int = 0.98, discounter_rate: int = 80):
        with open(os.path.join(DATA_PATH, f"{name}/config.json"), "w+") as f:
            json.dump({
                'name': str(name),
                'lr': float(lr),
                'hidden_layers': int(hidden_layers),
                'gamma': float(gamma),
                'discounter_rate': int(discounter_rate),
            }, f, indent=2) 

    def __bot_exists(self, name: str):
        if name in os.listdir(DATA_PATH):
            return True
        return False

    def __get_bot_config(self, name):
        data = None
        with open(os.path.join(DATA_PATH, f"{name}/config.json")) as f:
            data = json.loads(f.read())
        return data

    def __remove_all_from_bot(self, name: str):
        for root, dirs, files in os.walk(os.path.join(DATA_PATH, name)):
            for f in files:
                path = os.path.join(root, f)
                os.remove(path)
        
        for root, dirs, files in os.walk(os.path.join(DATA_PATH, name)):           
            for d in dirs:
                path = os.path.join(root, d)
                os.rmdir(path)
        
        os.rmdir(os.path.join(DATA_PATH, name))

    def __update_config(self, name: str, attribute: str):
        params = json.loads(self.handler.params)

        if not self._params_guard():
            return None

        if not self.__bot_exists(name):
            self.handler.report("Bot don't exists !!")
            return None

        config = self.__get_bot_config(name)
        config[attribute] = params.get(attribute)
        self.__create_bot_config(**config)
        self.handler.report(f"Bot learning rate successfully updated !!", True)

    def do_create(self):
        # name=zxc,lr=0.00245,hidden_layers=43,gamma=0.98,discounter_rate=20
        params = json.loads(self.handler.params)
        name = params.get("name")

        print(self.handler.params)

        if name is None:
            self.handler.report("You need to define a name !!")        
            return None

        if self.__bot_exists(name):
            self.handler.report("Bot already exists !!")    
            return None

        self.__create_bot_workspace(name, **params)

        self.handler.report(f"Bot {name} successfully created !!", True)
        sleep(2.5)

        return None

    def do_get(self):
        params = self.handler.params

        if params is None:
            self.handler.report("You need to provide some parameters !!")
            return None

        params = json.loads(params)
        name = params.get("name")

        if not self.__bot_exists(name):
            return None

        config_file = os.path.join(DATA_PATH, f"{name}/config.json")

        tmp = None

        with open(config_file) as f:
            tmp = f.read()

        if tmp is not None:
            self.handler.report("Bot data get successfully", True, tmp)

    def do_get_all(self):
        bots = os.listdir(DATA_PATH)
        data = []

        for bot in bots:
            config = self.__get_bot_config(bot)
            data.append(config)

        self.handler.report(None, True, data)

        return None

    def do_delete(self): 
        params = self.handler.params

        if not self._params_guard():
            return None
        
        name = json.loads(params).get("name")

        if not self.__bot_exists(name):
            return None

        self.__remove_all_from_bot(name)

        self.handler.report(f"Bot {name} successfully deleted !!", True)

    def do_delete_all(self):
        bots = os.listdir(DATA_PATH)

        for bot in bots:
            self.__remove_all_from_bot(bot)
        
        self.handler.report("All bots successfully deleted !!")

    def do_reset(self):
        params = json.loads(self.handler.params)

        if params is None:
            self.handler.report("You need to provide some parameters !!")
            return None

        name = params.get("name")

        if not self.__bot_exists(name):
            return None
        
        model_path = os.path.join(DATA_PATH, f"{name}/model")
        
        for f in os.listdir(model_path):
            fpath = os.path.join(model_path, f)
            os.remove(fpath)

        self.handler.report("Successfully reseted !!", True)

    def do_update_name(self):
        params = json.loads(self.handler.params)

        if not self._params_guard():
            return None

        if not self.__bot_exists(params.get("name")):
            self.handler.report("Bot don't exists !!")
            return None

        if self.__bot_exists(params.get("new_name")):
            self.handler.report(f"Bot {params.get('new_name')} already exists !!")
            return None
        

        config = self.__get_bot_config(params.get("name"))
        config["name"] = params.get(f"new_name")

        src_path = os.path.join(DATA_PATH, params.get("name"))
        dst_path = os.path.join(DATA_PATH, config["name"])
        shutil.move(src_path, dst_path)
        self.__create_bot_config(**config)

        self.handler.report(f"Bot name successfully updated !!", True)

    def do_update_learningrate(self):
        params = json.loads(self.handler.params)

        if not self._params_guard():
            return None

        if not self.__bot_exists(params.get("name")):
            self.handler.report("Bot don't exists !!")
            return None

        self.__update_config(params.get("name"), "lr")
    
    def do_update_hiddenlayers(self):
        params = json.loads(self.handler.params)

        if not self._params_guard():
            return None

        if not self.__bot_exists(params.get("name")):
            self.handler.report("Bot don't exists !!")
            return None

        self.__update_config(params.get("name"), "hidden_layers")

    def do_update_gamma(self):
        params = json.loads(self.handler.params)

        if not self._params_guard():
            return None

        if not self.__bot_exists(params.get("name")):
            self.handler.report("Bot don't exists !!")
            return None

        self.__update_config(params.get("name"), "gamma")
    
    def do_update_discounterrate(self):
        params = json.loads(self.handler.params)

        if not self._params_guard():
            return None

        if not self.__bot_exists(params.get("name")):
            self.handler.report("Bot don't exists !!")
            return None

        self.__update_config(params.get("name"), "discounter_rate")

    def do_update_all(self):
        params = self.handler.params
        print(params)