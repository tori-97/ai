import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background="#333")

        self.grid(row=1, column=4, columnspan=24, rowspan=24, sticky="NSEW")

        self.fig = Figure(figsize=(5,5), dpi=80, facecolor="#666")
        self.canvas = FigureCanvasTkAgg(self.fig,master=self)

        self._create_plot()
    

    def _create_plot(self):
        self.fig.clear()
        
        
        self.plot = self.fig.add_subplot(111)
        
        self.plot.set_title("EURUSD")
        self.plot.set_xlabel("Days", fontdict={'color': "#222"})
        self.plot.set_ylabel("Price", fontdict={'color': "#222"})
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, ipadx=18, ipady=18)

        self._days = []
        self._prices = []

        self._buys = []
        self._closes = []


    def update_plot(self, days, price = None, buy = None, close = None):
        self.plot.clear()

        self._days.append(days)
        self._prices.append(price)
        self._buys.append(buy)
        self._closes.append(close)

        # self.plot.set_xticklabels(self._days, rotation = 50)

        self.plot.plot(self._days, self._prices)
        self.plot.plot(self._days, self._buys, marker="o", color="green")
        self.plot.plot(self._days, self._closes, marker="o", color="red")

        self.canvas.draw()

    
    def reset_plot(self):
        self._create_plot()