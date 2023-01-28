from time import sleep
import random, os
from datetime import datetime
import json

from aibot.lib import Environment, Agent

from DataCrawler.dataset import DataSet

class AiTrading():
    def __init__(self,
        handler,
        balance: float,
        max_episodes: int,
        learning_rate: float,
        gamma: float,
        batch_size: int,
        bot: str,
        symbol: str,
        period: str,
        train_data_percentage: float,
        min_episodes: int,
        bot_config: dict
    
    ) -> None:
        self._handler = handler
        self._balance = balance
        self._max_episodes = max_episodes
        self._learning_rate = learning_rate
        self._gamma = gamma
        self._batch_size = batch_size
        self._bot = bot
        self._symbol = symbol
        self._period = period
        self._training_data_amount = train_data_percentage
        self._min_episodes = min_episodes

        self._dataset = None
        self._bot_current_day = 0

        self._is_running = True

        self._config = bot_config

    def load_dataset(self):
        ds = DataSet()
        try:
            tmp = ds.getSymbol(self._symbol, self._period, False)
        except FileNotFoundError:
            tmp = None
                
        if tmp is None:
            self._handler.report(f"Dataset: '{self._symbol}/{self._period}' is currently unnavailable !!", is_client_msg=True)
            return False

        tmp_len = len(tmp)
        _tmp = tmp[0:int(self._training_data_amount * tmp_len)]
        
        self._dataset = _tmp

        times = list(map(lambda x: x.get("time") if x is not None else [], self._dataset))
        closes = list(map(lambda x: x.get("close") if x is not None else [], self._dataset))

        self._handler.report("load-data", True, False, {
            "time": times,
            "closes": closes,
            "symbol": self._symbol
        })

        return True

    def start_training(self):
        # get_data
        self._handler.report("Loading dataset...", is_client_msg=True)
        loaded = self.load_dataset()

        if loaded:
            self._handler.report("Dataset loaded...", is_client_msg=True)
        else:
            return "Data couldn't be loaded !!"

        sleep(2.5)

        # init agent
        agent = Agent(self._bot, self._balance, self._learning_rate, self._gamma, self._batch_size)

        status = agent.load()
        self._handler.report(f"Agent loaded: {'yes' if status else 'no'}")

        # init environment
        env = Environment(agent.balance)
        # start episodes
        
        self._handler.report("Training will start shortly...", is_client_msg=True)
        # # Start Episode
        sleep(3.5)
        self._handler.report("Training started...", is_client_msg=True)

        max_balance_per_episode = 0
        max_profit_per_episode = 0

        i = 1

        while i < int(self._min_episodes):
            self._handler.report("reset-episode")

            if i > 1:
                self._handler.report("Training has been reseted...", is_client_msg=True)
            
            sleep(.5)

            env.balance = env.start_balance
            break_out = False

            for i in range(1, self._max_episodes + 1):
                max_profit = 0
                max_balance = 0

                if break_out:
                    break
                
                for j in range(len(self._dataset)):
                    row = self._dataset[j]

                    try:
                        nrow = self._dataset[j+1]
                    except IndexError:
                        nrow = row

                    if int(env.balance) <= 0:
                        self._handler.report("Agent dont have any balance anymore !!", is_client_msg=True)
                        # print("No balance , training will finish now")
                        break_out = True
                        sleep(2)
                        break
            
                    # get state
                    state = env.getState(row, agent.current_action)
                    # get action
                    agent.current_action, predictions, decision_made_by = agent.get_action(state)
                    # # do environment step
                    done, rewards, info = env.step(agent.translate_action_to_human(agent.current_action), row)
                    # # get next state
                    next_state = env.getState(nrow, agent.current_action)
                    # # optimize agent
                    agent.train_short(state, agent.current_action, rewards, next_state, done)
                    # # remember agent
                    agent.remember(state, agent.current_action, rewards, next_state, done)

                    profit = info.get("profit") if isinstance(info, dict) else 0

                    if done:
                        env.reset()
                        agent.train_long()

                        if profit > max_profit:
                            max_profit = profit

                        if env.balance > max_balance:
                            max_balance = env.balance

                        agent.balance = env.balance

                        if info is not None and info != "no-balance":
                            agent.trades.append(info)

                        if len(agent.trades) > 0 and env.balance > env.start_balance:
                            status = agent.save_current_status()
                            self._handler.report(f"Agent saved at {datetime.now()}", is_client_msg=True)

                    data2send = {
                        "episodes": {
                            "current": i,
                            "max": self._max_episodes,
                            # "percentage_done": round((100 / self._max_episodes), 2) * i, 2)
                            "percentage_done": round((100/ self._max_episodes) * i, 2)
                        },
                        "days": {
                            "current": j,
                            "max": len(self._dataset),
                            # "percentage_done": round((100 / len(self._dataset) * j, 2)
                            "percentage_done": round((100 / len(self._dataset)) * j, 2)
                        },
                        "max_profit": round(max_profit, 2),
                        "max_balance": round(max_balance, 2),
                        "balance": round(env.balance, 2),
                        "profit": round(env.balance - env.start_balance, 2),
                        "trades": len(agent.trades),
                        "rewards": round(rewards, 2),
                        "last_decision": decision_made_by,
                        "prediction": predictions,
                        "bot": { "day": j, "trades": agent.trades }
                    }
                    self._handler.report("update", False, False, data2send)

                    sleep(.5)

                    del state, done, rewards, profit, info, next_state, data2send

                if max_profit > max_profit_per_episode:
                    max_profit_per_episode = max_profit
                
                if max_balance > max_balance_per_episode:
                    max_balance_per_episode = max_balance

                if i % 2 == 0:
                    if len(agent.trades) > 0 and env.balance > env.start_balance:
                        status = agent.save_current_status()
                        self._handler.report(f"Agent saved at {datetime.now()}", is_client_msg=True)

                self._config['counter']['amount_trades'] += len(agent.trades)
                self._config['counter']['amount_episodes'] += 1

                agent.trades = []

                sleep(.5)


        # Closing training
        self._is_running = False
        agent.save_current_status()
        
        self._config['counter']['amount_trainings'] += 1
        
        if i > self._config['records']['max_episodes']:
            self._config['records']['max_episodes'] = i
        
        if max_balance > self._config['records']['max_balance']:
            self._config['records']['max_balance'] = max_balance_per_episode

        if max_profit > self._config['records']['max_profit']:
            self._config['records']['max_profit'] = max_profit_per_episode


        with open(os.path.join(os.getcwd(), f"aibot/data/bots/{self._bot}/config.json"), "w+") as f:
            json.dump(self._config,f, indent=2)

        self._handler.report(f"Agent saved and finished training at {datetime.now()}", is_client_msg=True)
        self._handler.report(f"end")
        sleep(2)

        #do running loop until min eps is reached.

        return "Training ends !"

__all__ = [
    "AiTrading"
]