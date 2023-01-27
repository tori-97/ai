import os, json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pandas as pd

from trading_app import utils
from trading_app.layout.sidepanel import SidePanelFrame
from trading_app.layout.graphs import GraphsFrame
from trading_app.layout.buttons import ButtonsFrame

from ai_trader.trader.agent import Agent
from ai_trader.trader.environment import TradingEnvironment
from ai_trader.trader.support.iqoption import IQOptionEnvironment
from ai_trader.utils import get_random_data_sample_without_shuffle, reset_trader, get_random_data_sample
from ai_trader.settings import umail, upasswd

from iqoptionapi.stable_api import IQ_Option


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__(className="Tradingbot")

        self.geometry("1600x1200")
        self.title("TradingBot")
        self.config(bg="#444")     

        utils.reconfigure_layout(self, 24, 24)

        self.side_panel = SidePanelFrame(self)
        self.buttons_frame = ButtonsFrame(self)
        self.graphs = GraphsFrame(self)

        self._load_default_configuration()
        
        self.buttons_frame.start_training_btn.config(command=self.start_training)
        self.buttons_frame.evaluate_training_btn.config(command=self.evaluate_training)
        self.buttons_frame.practice_btn.config(command=self.practice_trading)
        self.buttons_frame.real_trading_btn.config(command=self.real_trading)
        self.buttons_frame.reset_bot_btn.config(command=self.reset_bot)
        self.buttons_frame.stop_tasks_btn.config(command=self.stop_task)

        self.is_running_task = False
    
        self.bind("<Destroy>", self._destroying)

        icon_photo = tk.PhotoImage(file=os.path.join(os.getcwd(), "trading_app/data/icon.png"))
        self.iconphoto(False, icon_photo)
        self.iconname("TradingBot")
        
    def _destroying(self, *args):
        backup_path = os.path.join(os.getcwd(), "trading_app/data/configurations.json")

        with open(backup_path, "w+") as f:
            json.dump(self.side_panel.configurations.get_configuration(), f, indent=2)            
        
    def _load_default_configuration(self):

        backup_path = os.path.join(os.getcwd(), "trading_app/data/configurations.json")
        
        try:        
            with open(backup_path) as f:
                data = json.loads(f.read())
                self.side_panel.configurations.set_configuration(**data)
        except FileNotFoundError:
            pass

    def stop_task(self):
        if self.is_running_task:
            self.is_running_task = False
            messagebox.showinfo("Information", "All tasks successfully stopped !!")
        else:
            messagebox.showwarning("Warning", "No tasks are running !!")

    def reset_bot(self): 
        resp = messagebox.askquestion("Reset Bot", "Are you sure you want reset anything ?")
        
        if resp == "yes":
            reset_trader()
            self.side_panel.configurations.set_configuration(10, 0.0025, 0.98, 34, 64, "brain.pth", "optim.pth")
            messagebox.showinfo("Information", "Bot successfully reseted !!")

    def start_training(self):
        self.is_running_task = True

        print("[+] Start training...")

        agent_config = self.side_panel.configurations.get_configuration()

        agent = Agent(
            lr=agent_config['lr'], 
            gamma=agent_config['gamma'], 
            batch_size=agent_config['batch_size'], 
            model_hidden_layers=int(agent_config['hidden_layers']), 
            brain_fpath=agent_config['brain_path'], 
            optim_fpath=agent_config['optim_path']
            )

        agent.load()
        env = TradingEnvironment(start_balance=100.00)

        data_sample, data_sample_len = get_random_data_sample_without_shuffle(env.days, 0.32)
        
        max_profit_of_all_episodes = 0
        max_episodes = agent_config['max_episodes']
        
        env.minimun_trades_need = 100

        max_balance_per_episode = 100.00

        for ep in range(1, max_episodes + 1):
            
            if not self.is_running_task:
                break

            max_profit = 0
            env.start_balance = 100.00
            env.balance = env.start_balance

            for i in range(data_sample_len - 1):
                day = data_sample.iloc[i]
                next_day = data_sample.iloc[i+1]

                state = env.get_state(day)
                action, decision_made_by, pred_percent = agent.get_action(state)
                done, rewards, profit, info = env.step(action, day)

                next_state = env.get_state(next_day)
                agent.optimize(state, action, rewards, next_state, done)
                agent.remember(state, action, rewards, next_state, done)

                if done:
                    env.reset()
                    # agent.n_trades += 1
                    agent.optimize_long_memory()

                    if profit > max_profit:
                        max_profit = profit

                eps_percentage = (100 / max_episodes) * ep
                days_percentage = (100 / data_sample_len) * i

                self.side_panel.informations.update_information(
                        f"({ep}/{max_episodes})[{eps_percentage:.2f} %]", 
                        f"({i}/{data_sample_len})[{days_percentage:.2f} %]", 
                        max_profit, 
                        env.balance, 
                        f"{env.balance - env.start_balance:.2f}", 
                        f"{len(env.trades)}/{env.minimun_trades_need}", 
                        rewards, 
                        decision_made_by, 
                        pred_percent
                    )

                buy, close = info           
                self.graphs.update_plot(day.time, day.close, buy, close)
               

                del day, next_day, state, action, decision_made_by, done, rewards, profit, next_state

                if max_profit > max_profit_of_all_episodes:
                    # agent.save()
                    max_profit_of_all_episodes = max_profit
                    # print("Bot Saved !!")

                if not self.is_running_task:
                    break
                
                self.update()

            self.graphs.reset_plot()
            self.update()
            env.trades = []
            agent.n_trades += 1

            if env.balance > max_balance_per_episode:
                max_balance_per_episode = env.balance
                agent.save()
                print(f"[!] Bot last saved at {datetime.now()} | MaxBalance: {max_balance_per_episode}")

        self.is_running_task = False
        messagebox.showinfo("Information", "Training runs successfully done !!")

    def evaluate_training(self):
        messagebox.showwarning("Warning", "In development !!")

    def practice_trading(self):
        self.is_running_task = True

        print("[+] Starting IQoption Api...")

        iq = IQ_Option(umail, upasswd)
        check, msg = iq.connect()

        env = IQOptionEnvironment(iq)
        agent_config = self.side_panel.configurations.get_configuration()

        agent = Agent(
            lr=agent_config['lr'], 
            gamma=agent_config['gamma'], 
            batch_size=agent_config['batch_size'], 
            model_hidden_layers=int(agent_config['hidden_layers']), 
            brain_fpath=agent_config['brain_path'], 
            optim_fpath=agent_config['optim_path']
            )

        agent.load()

        ACTIVE = "EURUSD"
        SIZE = 3600

        iq.start_candles_stream(ACTIVE, SIZE, 1)

        train_done = False
        max_profit = 0

        print("[+] Starting Practice mode...")

        rounds = 1

        while not train_done:
            candles = iq.get_realtime_candles(ACTIVE, SIZE)
            id = list(candles.keys())[0]
            data = candles[id]

            day = {
                "time": datetime.fromtimestamp(data.get('from')),
                "open": float(data.get("open")),
                "close": float(data.get("close")),
                "high": float(data.get("max")),
                "low": float(data.get("min")),
                "volume": int(data.get("volume"))
            }

            state = env.get_state(day)
            action, decision_made_by, pred_percent = agent.get_action(state)
            done, rewards, profit = env.step(action) 

            next_state = state
            agent.optimize(state, action, rewards, next_state, done)
            agent.remember(state, action, rewards, next_state, done)

            if done:
                env.reset()
                agent.n_trades += 1
                agent.optimize_long_memory()

                if profit > max_profit:
                    max_profit = profit
                    agent.save()

        
            self.side_panel.informations.update_information(
                    f"Real Time", 
                    f"Real Time", 
                    max_profit, 
                    env.balance, 
                    f"{env.balance - env.start_balance:.2f}", 
                    f"{agent.n_trades}/{env.minimun_trades_need}", 
                    rewards, 
                    decision_made_by, 
                    pred_percent
                )
            
            self.graphs.update_plot(rounds, profit)

            if not self.is_running_task:
                train_done = True

            self.graphs.reset_plot()
            self.update()
            env.trades = []

            print(f"Rounds: {rounds}", end="\r")
            # del day, state, action, decision_made_by, done, rewards, profit, next_state, candles, id, data


            rounds += 1

            if not self.is_running_task:
                train_done = True           

        self.is_running_task = False

        iq.stop_candles_stream(ACTIVE, SIZE)

    def real_trading(self):
        messagebox.showwarning("Warning", "In development !!")


__all__ = [
    "MainWindow"
]