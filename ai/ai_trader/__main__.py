"""
    * Ai trader
"""
import gc
import random

from ai_trader.trader import Agent, TradingEnvironment

import logging

class Logger():
    def __init__(self, fpath: str) -> None:
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        self._handler = logging.FileHandler(fpath, mode="w+")
        self._logger.addHandler(self._handler)

    def log(self, msg):
        self._logger.debug(msg)


class Trainer():
    def __init__(self, max_episodes: int = 10, **kwargs) -> None:
        if kwargs:
            self.agent = Agent(lr=kwargs.get("lr"), gamma=kwargs.get('gamma'), batch_size=kwargs.get('batch_size'), model_hidden_layers=kwargs.get("hidden_layers"), brain_fpath=kwargs.get("brain_fpath"), optim_fpath=kwargs.get("optim_fpath"))
        else:
            self.agent = Agent()
        
        self.env = TradingEnvironment(start_balance=1000.00)

        self.episodes = 1
        self.max_episodes = max_episodes

    def get_random_data_sample(self):
        train_rand_range = random.uniform(0, 1)
        data_sample = self.env.days.sample(int(len(self.env.days) * train_rand_range))
        data_sample_len = len(data_sample)

        return data_sample, data_sample_len

    def do_training(self):
        loaded = self.agent.load()
        print("\nPre-trained agent loaded !!" if loaded else "\nNo pre-trained agent will be used !")

        data_sample, data_sample_len = self.get_random_data_sample()

        training_done = False
        max_profit = 0
        minimun_trades_needed = int(data_sample_len * 0.85)
        self.env.minimun_trades_need = minimun_trades_needed
        self.env.trades = []

        for i in range(data_sample_len - 1):
            current_day = data_sample.iloc[i]
            next_day = data_sample.iloc[i + 1]

            state = self.env.get_state(current_day)
            action, decision_made_by, pred_percent = self.agent.get_action(state)
            done, rewards, profit = self.env.step(action, current_day)

            next_state = self.env.get_state(next_day)
            self.agent.optimize(state, action, rewards, next_state, done)
            self.agent.remember(state, action, rewards, next_state, done)

            if done:
                self.env.reset()
                self.agent.n_trades += 1
                self.agent.optimize_long_memory()

                if profit > max_profit:
                    max_profit = profit

            print(f"""                
\033[KEpisodes:({self.episodes}/{max_episodes})[{(100 / max_episodes) * self.episodes:.2f} %]
\033[KRows:({i}/{data_sample_len})[{(100 / data_sample_len) * i:.2f} %] 
\033[KMaxProfit:{max_profit:.2f} 
\033[KBalance:{self.env.balance:.2f} 
\033[KProfit:{self.env.balance - self.env.start_balance:.2f} 
\033[KTrades:{self.agent.n_trades}/{self.env.minimun_trades_need} 
\033[KRewards:{rewards:.2f} 
\033[KDecisionMadeBy:{decision_made_by} 
\033[KPrediction:{pred_percent}
                """, end="\r\r\r\r\r\r\r\r\r\r\r")
            
            del current_day, next_day, state, action , done, rewards, next_state
            gc.collect()

            if int(self.env.balance) <= 0:
                print("\n[!] No Balance more !!")
                training_done = True
                break

        self.episodes += 1
        training_done = True
        
        del data_sample, data_sample_len

        return training_done


def main(max_episodes, **kwargs):

    training_done = False

    trainer = Trainer(max_episodes, **kwargs)

    while not training_done:
        training_done = trainer.do_training()

        if trainer.episodes < max_episodes:
            training_done = False
        
    del trainer

def training(max_episodes, **kwargs):

    training_done = False
    max_profit = 0
    episodes = 1
    # logger = Logger('./ai_trader/data/boti.log')

    while not training_done:
        


        episodes += 1

        if episodes % 5 == 0:
            agent.save()

        if episodes == max_episodes:
            training_done = True
        
        # if trainings_num_done % 5 == 0:
        #     logger.log(f"Trainings done: {trainings_num_done}/{max_episodes} [{(100 / max_episodes) * trainings_num_done:.2f}] | Rows {i}/{data_sample_len} [{(100 / data_sample_len) * i:.2f} %] | Max Profit: {max_profit:.2f} | Balance: {env.balance:.2f} | trades done: {agent.n_trades} | Decision made by: {decision_made_by} \n")

        del data_sample, env, agent, data_sample_len
        gc.collect()

    if episodes < max_episodes:
        training(max_episodes, **kwargs)

    print("Training Done !!")

    del training_done,max_profit

    return episodes


def reset_trader():
    import os

    model_path = os.path.join(os.getcwd(), "ai_trader/data/model")

    data = os.listdir(model_path)

    for f in data:
        fpath = os.path.join(model_path, f)
        os.remove(fpath)
   
    print("[+] Trader reseted !!")

def test(eps, **kwargs):
    agent = Agent(
        lr=kwargs.get("lr"), 
        gamma=kwargs.get('gamma'), 
        batch_size=kwargs.get('batch_size'), 
        model_hidden_layers=kwargs.get("hidden_layers"), 
        brain_fpath=kwargs.get("brain_fpath"), 
        optim_fpath=kwargs.get("optim_fpath")
        )

    agent.save()

if __name__ == "__main__":
    import argparse 

    parser = argparse.ArgumentParser("Ai trader")
    parser.add_argument(*["-me", "--max-episodes"], type=int, default=1000)
    parser.add_argument(*["-r", "--reset-trader"], action='store_true')
    # model configuration
    parser.add_argument(*["-lr", "--learning-rate"], type=float, default=0.0036)
    parser.add_argument(*["-g", "--gamma"], type=float, default=0.98)
    parser.add_argument(*["-bs", "--batch-size"], type=int, default=100)
    parser.add_argument(*["-hl", "--hidden-layers"], type=int, default=64)
    parser.add_argument(*["-bp", "--brain-path"], type=str, default="brain.pth")
    parser.add_argument(*["-op", "--optim-path"], type=str, default="optim.pth")

    args = parser.parse_args()

    max_episodes = args.max_episodes

    if args.reset_trader:
        reset_trader()

    main(max_episodes, **{
        "lr": args.learning_rate,
        "gamma": args.gamma,
        "batch_size": args.batch_size,
        "hidden_layers": args.hidden_layers,
        "brain_fpath": args.brain_path,
        "optim_fpath": args.optim_path,
    })