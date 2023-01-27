import tkinter as tk
from trading_app import utils
from trading_app.layout.sidepanel.configurations import SidePanelConfigurationsFrame
from trading_app.layout.sidepanel.informations import SidePanelInformationsFrame

class SidePanelFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background="#333")

        utils.reconfigure_layout(self, 12, 12)
        
        self.grid(row=0, column=0, rowspan=24, columnspan=4, sticky=tk.NSEW)

        self.configurations = SidePanelConfigurationsFrame(self)
        self.informations   = SidePanelInformationsFrame(self)