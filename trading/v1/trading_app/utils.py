
def reconfigure_layout(master, rows, columns):
    for i in range(0, rows):
        for j in range(0, columns):
            master.columnconfigure(j, weight=1)
        master.rowconfigure(i, weight=1)
