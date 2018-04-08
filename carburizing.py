from math import *
from scipy.special import erfinv
from tkinter import *
from tkinter import ttk

root = Tk()

root.title("Carburization Penetration Depth")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

D0 = 0.23
R  = 1.987
Q  = 32900

# get T temperature 900 - 1100
T = DoubleVar()
T.set(900)

temp_entry = ttk.Entry(mainframe, width=7, textvariable=T)
temp_entry.grid(column=1, row=2, sticky=(W, E))

D = D0 * exp( -Q / (R * T.get()))

Cs = 1.3

# get C0 value: select 1018 for .0018, 1045 for .0045
C0 = DoubleVar()
C0.set(.0018)

ceeoh_entry = ttk.Combobox(mainframe, width=7, textvariable=C0)
ceeoh_entry.grid(column=1, row=1, sticky=(W, E))

Cx = C0.get() + pow(10, -16)

z = (Cs - Cx) / (Cs - C0.get())

# get t value in minutes
time = DoubleVar()
time.set(60)

time_entry = ttk.Entry(mainframe, width=7, textvariable=time)
time_entry.grid(column=1, row=3, sticky=(W, E))

x = 2 * erfinv(z) * pow(D * time.get(), 1/2)

root.mainloop()
