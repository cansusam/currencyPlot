# from tkinter import *
# import seaborn as sns
# import numpy as np
# import pandas as pd
# from string import ascii_letters
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#
# def create_plot():
#     sns.set(style="white")
#
#     # Generate a large random dataset
#     rs = np.random.RandomState(33)
#     d = pd.DataFrame(data=rs.normal(size=(100, 26)),
#                      columns=list(ascii_letters[26:]))
#
#     # Compute the correlation matrix
#     corr = d.corr()
#
#     # Generate a mask for the upper triangle
#     mask = np.zeros_like(corr, dtype=np.bool)
#     mask[np.triu_indices_from(mask)] = True
#
#     # Set up the matplotlib figure
#     f, ax = plt.subplots(figsize=(11, 9))
#
#     # Generate a custom diverging colormap
#     cmap = sns.diverging_palette(220, 10, as_cmap=True)
#
#     # Draw the heatmap with the mask and correct aspect ratio
#     sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
#                 square=True, linewidths=.5, cbar_kws={"shrink": .5})
#
#     return f
#
#
# # Here, we are creating our class, Window, and inheriting from the Frame
# # class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
# class Window(Frame):
#
#     # Define settings upon initialization. Here you can specify
#     def __init__(self, master=None):
#         # parameters that you want to send through the Frame class.
#         Frame.__init__(self, master)
#
#         # reference to the master widget, which is the tk window
#         self.master = master
#
#         # with that, we want to then run init_window, which doesn't yet exist
#         self.init_window()
#
#     # Creation of init_window
#     def init_window(self):
#         # changing the title of our master widget
#         self.master.title("GUI")
#
#         # allowing the wdget to take the full space of the root window
#         self.grid_columnconfigure(0, weight=0)#.pack(fill=BOTH, expand=1)
#         self.grid_rowconfigure(0, weight=0)
#
#         # creating a menu instance
#         menu = Menu(self.master)
#         self.master.config(menu=menu)
#
#         # create the file object)
#         file = Menu(menu)
#
#         # adds a command to the menu option, calling it exit, and the
#         # command it runs on event is client_exit
#         file.add_command(label="Exit", command=self.client_exit)
#
#         # added "file" to our menu
#         menu.add_cascade(label="File", menu=file)
#
#         # ListBox
#         labelList = Label(root, text="Currencies")
#         labelList.grid(row=0,column=0)
#         Lb = Listbox(root)
#         Lb.insert(1, 'USDTRY')
#         Lb.insert(2, 'EURTRY')
#         Lb.insert(3, 'XAUUSD')
#         Lb.insert(4, 'BTCUSD')
#         Lb.grid(row=1,column=0,sticky=N)
#         # Graph
#         label = Label(root, text="Currency Plot")
#         label.grid(row=0,column=1)
#         fig = create_plot()
#         canvas = FigureCanvasTkAgg(fig, master=root) # A tk.DrawingArea.
#         canvas.draw()
#         canvas.get_tk_widget().grid(row=1,column=1,sticky=N)
#
#     def client_exit(self):
#         exit()
#
# root = Tk()
# root.geometry('{}x{}'.format(400,300))
# app = Window(root)
#
# # to prevent macos crashes with mouse wheel move


# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)


def animate(i):
    pullData = open("sampleText.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList, yList)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)#(), default="clienticon.ico")
        tk.Tk.wm_title(self, "Sea of BTC client")

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
        labelList.pack(pady=10, padx=10)  # .grid(row=0,column=0)
        Lb = tk.Listbox(self)
        Lb.insert(1, 'USDTRY')
        Lb.insert(2, 'EURTRY')
        Lb.insert(3, 'XAUUSD')
        Lb.insert(4, 'BTCUSD')
        Lb.pack(pady=10, padx=10)  # .grid(row=1,column=0,sticky=N)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



app = SeaofBTCapp()
ani = animation.FuncAnimation(f, animate, interval=1000)
while True:
    try:
        app.mainloop()
        break
    except UnicodeDecodeError:
        pass