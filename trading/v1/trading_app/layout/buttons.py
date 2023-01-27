import tkinter as tk

class ButtonsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background="#222")

        self.start_training_btn = tk.Button(self, text="Start Training", bg="#444", borderwidth=0, highlightthickness=0, fg="#cacaca", activebackground="#555", activeforeground="#bebebe")
        self.start_training_btn.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)

        self.evaluate_training_btn = tk.Button(self, text="Evaluate Training", bg="#444", borderwidth=0, highlightthickness=0, fg="#cacaca", activebackground="#555", activeforeground="#bebebe")
        self.evaluate_training_btn.grid(row=0, column=1, sticky=tk.NSEW, padx=10, pady=10)

        self.practice_btn = tk.Button(self, text="Practice trading", bg="#444", borderwidth=0, highlightthickness=0, fg="#cacaca", activebackground="#555", activeforeground="#bebebe")
        self.practice_btn.grid(row=0, column=2, sticky=tk.NSEW, padx=10, pady=10)

        self.real_trading_btn = tk.Button(self, text="Real Trading", bg="#444", borderwidth=0, highlightthickness=0, fg="#cacaca", activebackground="#555", activeforeground="#bebebe")
        self.real_trading_btn.grid(row=0, column=3, sticky=tk.NSEW, padx=10, pady=10)

        self.reset_bot_btn = tk.Button(self, text="Reset Bot", bg="#444", borderwidth=0, highlightthickness=0, fg="#cacaca", activebackground="#555", activeforeground="#bebebe")
        self.reset_bot_btn.grid(row=0, column=4, sticky=tk.NSEW, padx=10, pady=10)

        self.stop_tasks_btn = tk.Button(self, text="Stop all tasks", bg="#444", borderwidth=0, highlightthickness=0, fg="#cacaca", activebackground="#555", activeforeground="#bebebe")
        self.stop_tasks_btn.grid(row=0, column=5, sticky=tk.NSEW, padx=10, pady=10)
        
        self.grid(row=0, column=4, columnspan=24, sticky=tk.NSEW)
