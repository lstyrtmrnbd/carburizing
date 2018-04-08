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

temp_entry = ttk.Entry(mainframe, width=7, textvariable=T)

D = D0 * math.exp( -Q / (R * T))

Cs = 1.3

# get C0 value: select 1018 for .0018, 1045 for .0045
C0 = DoubleVar()

ceeoh_entry = ttk.Entry(mainframe, width=7, textvariable=C0)

Cx = C0 + math.pow(10, -16)

z = (Cs - Cx) / (Cs - C0)

# get t value in minutes
time = DoubleVar()

x = 2 * erfinv(z) * math.pow(D * time, 1/2)


root.mainloop()
