import tkinter as tk

from trading_app import utils


class SidePanelInformationsRowFrame(tk.Frame):
    def __init__(self, master, label, row):
        super().__init__(master, background="#222")

        utils.reconfigure_layout(self, 1, 2)

        self.label = tk.Label(self, text=label, width=15, bg="#222", fg="#cacaca")
        self.value = tk.Label(self, text="", width=30, bg="#333", fg="#cacaca")

        self.label.grid(row=0, column=0)
        self.value.grid(row=0, column=1, columnspan=2)
        self.label.grid_propagate(False)  
        self.value.grid_propagate(False)  

        self.grid(row=row, column=0)

class SidePanelInformationPredictionsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background="#222")

        utils.reconfigure_layout(self, 1, 8)

        self.title = tk.Label(self, text="Predictions:", bg="#444", fg="#cacaca")
        self.title.grid(row=0, column=0, columnspan=8, sticky=tk.NSEW)

        self.hold = tk.Label(self, text="Hold: ", bg="#222", fg="#cacaca")
        self.hold_val = tk.Label(self, text="", width=10, bg="#333", fg="#cacaca")

        self.long = tk.Label(self, text="long: ", bg="#222", fg="#cacaca")
        self.long_val = tk.Label(self, text="", width=10, bg="#333", fg="#cacaca")
        
        self.short = tk.Label(self, text="short: ", bg="#222", fg="#cacaca")
        self.short_val = tk.Label(self, text="", width=10, bg="#333", fg="#cacaca")
        
        self.sell = tk.Label(self, text="sell: ", bg="#222", fg="#cacaca")
        self.sell_val = tk.Label(self, text="", width=10, bg="#333", fg="#cacaca")

        self.hold.grid(row=1, column=2, sticky=tk.NSEW, pady=5)
        self.hold_val.grid(row=1, column=3, sticky=tk.NSEW, pady=5)

        self.sell.grid(row=1, column=4, sticky=tk.NSEW, pady=5)
        self.sell_val.grid(row=1, column=5, sticky=tk.NSEW, pady=5)

        self.long.grid(row=2, column=2, sticky=tk.NSEW, pady=5)
        self.long_val.grid(row=2, column=3, sticky=tk.NSEW, pady=5)

        self.short.grid(row=2, column=4, sticky=tk.NSEW, pady=5)
        self.short_val.grid(row=2, column=5, sticky=tk.NSEW, pady=5)

        self.grid(row=9, column=0, padx=10, pady=10)
        

class SidePanelInformationsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background="#222")

        utils.reconfigure_layout(self, 8, 1)

        self.title = tk.Label(self, text="Trading Information", background="#444", fg="#bebebe")
        self.title.grid(row=0, column=0, columnspan=1, sticky=tk.NSEW, ipady=5)

        self.episodes = SidePanelInformationsRowFrame(self, "Episodes:", 1)
        self.days = SidePanelInformationsRowFrame(self, "Days:", 2)
        self.max_profit = SidePanelInformationsRowFrame(self, "MaxProfit:", 3)
        self.balance = SidePanelInformationsRowFrame(self, "Balance:", 4)
        self.profit = SidePanelInformationsRowFrame(self, "Profit:", 5)
        self.trades = SidePanelInformationsRowFrame(self, "Trades:", 6)
        self.rewards = SidePanelInformationsRowFrame(self, "Rewards:", 7)
        self.decision_made_by = SidePanelInformationsRowFrame(self, "DecisionMadeBy:", 8)
        self.prediction = SidePanelInformationPredictionsFrame(self)

        self.grid(row=1, column=0, columnspan=12, rowspan=2, sticky=tk.NSEW)


    def update_information(self, episodes, days, max_profit, balance, profit, trades, rewards, decision_made, prediction):
        self.episodes.value.config(text=episodes)
        self.days.value.config(text=days)
        self.max_profit.value.config(text=round(max_profit, 2))
        self.balance.value.config(text=round(balance, 2))
        self.profit.value.config(text=profit)
        self.trades.value.config(text=trades)
        self.rewards.value.config(text=round(rewards, 2))
        self.decision_made_by.value.config(text=decision_made)

        self.prediction.hold_val.config(text=prediction.get("hold"))
        self.prediction.short_val.config(text=prediction.get("short"))
        self.prediction.long_val.config(text=prediction.get("long"))
        self.prediction.sell_val.config(text=prediction.get("sell"))
        