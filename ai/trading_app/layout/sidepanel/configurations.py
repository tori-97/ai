
import tkinter as tk

class SidePanelRowFrame(tk.Frame):
    def __init__(self, master,row, label, placeholder: str = None):
        super().__init__(master, background="#333")

        # utils.reconfigure_layout(self, 1, 7)

        self.label = tk.Label(self, text=label, background="#333", fg="#cacaca")
        self.value = tk.Variable()
        self.entry = tk.Entry(self, textvariable=self.value, background="#222", border=0, borderwidth=0, highlightthickness=0, foreground="#cacaca", insertbackground="#bebebe", insertborderwidth=0.1)

        if placeholder is not None:
            self.value.set(placeholder)


        self.label.pack(fill="x", side='left', expand=True, anchor="c", ipadx=1, padx=10)
        self.entry.pack(fill="x", side='right', expand=False, anchor="c", ipadx=60, padx=10, ipady=5)

        self.pack(fill='both', expand=True)

    @property
    def val(self): return self.value.get()

    @val.setter
    def val(self, val): self.value.set(val)

class SidePanelConfigurationsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background="#333")

        self.title = tk.Label(self, text="Configuration", bg="#444", fg="#bebebe")
        self.title.pack(fill="both", expand=True, ipady=5)

        self.max_episodes = SidePanelRowFrame(self, 0, "MaxEpisodes")
        self.lr           = SidePanelRowFrame(self, 1, "LearningRate")
        self.gamma        = SidePanelRowFrame(self, 2, "Gamma")
        self.batch_size   = SidePanelRowFrame(self, 3, "BatchSize")
        self.hidden_layers= SidePanelRowFrame(self, 4, "HiddenLayers")
        self.brain_path   = SidePanelRowFrame(self, 5, "BrainPath")
        self.optim_path   = SidePanelRowFrame(self, 6, "OptimPath")

        self.grid(row=0, column=0, columnspan=12, sticky=tk.NSEW)

    def get_configuration(self):
        return {
            "max_episodes": int(self.max_episodes.val),
            "lr": float(self.lr.val),
            "gamma": float(self.gamma.val),
            "batch_size": int(self.batch_size.val),
            "hidden_layers": int(self.hidden_layers.val),
            "brain_path": self.brain_path.val,
            "optim_path": self.optim_path.val
        }

    def set_configuration(self, max_episodes, lr, gamma, batch_size, hidden_layers, brain_path, optim_path):
        self.max_episodes.val = max_episodes
        self.lr.val = lr
        self.gamma.val = gamma
        self.batch_size.val = batch_size
        self.hidden_layers.val = hidden_layers
        self.brain_path.val = brain_path
        self.optim_path.val = optim_path