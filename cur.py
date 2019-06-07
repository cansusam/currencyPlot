import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
import requests
from datetime import datetime
import pandas as pd
import seaborn as sns; sns.set(style="darkgrid")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fmri = sns.load_dataset("fmri")

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

URL = 'https://www.freeforexapi.com/api/live'

listOfRatios = ["USDTRY", "EURUSD", "USDXAU"]
seperator = ','
params = seperator.join(listOfRatios)
PARAMS = {'pairs':params}
data_hist = {}
ts_old = {}
for r in listOfRatios:
    data_hist[r] = []
    ts_old[r] = 0
Lb = ''
lastRate = listOfRatios[0]

f, a = plt.subplots()

def animate(i):
    global lastRate
    if len(Lb.curselection()) != 0:
        rate = Lb.get(Lb.curselection())
    else:
        rate = listOfRatios[0]
    for r in listOfRatios:
        if len(data_hist[rate]) == 0:
            ts_old[r] = 0
        else:
            ts_old[r] = data_hist[rate][-1]['timestamp']
    data = requests.get(url=URL, params=PARAMS).json()
    result = data['rates']
    for r in listOfRatios:
        ts = result[r]['timestamp']
        result[r]['timestamp'] = mdates.date2num(datetime.fromtimestamp(ts))
        if ts != ts_old[r]:
            data_hist[r].append(result[r])
    if lastRate != rate or ts_old[rate] != result[rate]['timestamp']:
        if lastRate != rate:
            plt.cla()
            lastRate = rate
        dft = pd.DataFrame.from_dict(data_hist[rate])
        sns.lineplot(x="timestamp", y="rate", data=dft, color='purple', legend=False)
        a.xaxis.set_major_locator(mdates.AutoDateLocator())
        a.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # '%Y-%m-%d %H:%M:%S'))
        f.autofmt_xdate()

class currencyPlot(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "Currency Graph")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # for F in ():
        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        # label.pack(pady=10, padx=10)

        labelList = tk.Label(self, text="Currencies", font=LARGE_FONT)
        labelList.pack(pady=1, padx=10)  # .grid(row=0,column=0)
        global Lb
        Lb = tk.Listbox(self, height=len(listOfRatios))

        for i in range(len(listOfRatios)):
            Lb.insert(i, listOfRatios[i])

        Lb.select_set(first = 0)
        Lb.pack(pady=1, padx=1)  # .grid(row=1,column=0,sticky=N)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



app = currencyPlot()

ani = animation.FuncAnimation(f, animate, interval=500)
while True:
    try:
        app.mainloop()
        break
    except UnicodeDecodeError:
        pass