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
temp_entry.grid(column=2, row=2, sticky=(W, E))

temp_label = ttk.Label(mainframe, text="Temperature (C)")
temp_label.grid(column=1, row=2, sticky=(W, E))

D = D0 * exp( -Q / (R * T.get()))

Cs = 1.3

# get C0 value: select 1018 for .0018, 1045 for .0045
steel = StringVar()
C0 = .0018

# steel selection callback
def selectC0():
    if steel == '1018':
        C0 = .0018
    elif steel == '1045':
        C0 = .0045

steel_entry = ttk.Combobox(mainframe, width=7, textvariable=steel)
steel_entry.grid(column=2, row=1, sticky=(W, E))

steel_entry['values'] = ('1018', '1045')
steel_entry.bind('<<ComboboxSelected>>', selectC0)

steel_label = ttk.Label(mainframe, text="Type of Steel:")
steel_label.grid(column=1, row=1, sticky=(W, E))

Cx = C0 + pow(10, -16)

z = (Cs - Cx) / (Cs - C0)

# get t value in minutes
time = DoubleVar()
time.set(60)

time_entry = ttk.Entry(mainframe, width=7, textvariable=time)
time_entry.grid(column=2, row=3, sticky=(W, E))

time_label = ttk.Label(mainframe, text="Time (min.)")
time_label.grid(column=1, row=3, sticky=(W, E))

output_label = ttk.Label(mainframe, text="Output:")
output_label.grid(column=1, row=4, sticky=(W, E))

x = 2 * erfinv(z) * pow(D * time.get(), 1/2)

output_result = ttk.Label(mainframe)
output_result.grid(column=2, row=4, sticky=(W, E))

def updatetext(event):
    output_result.configure(text=x)
    root.update_idletasks()

temp_entry.bind("<Key>", updatetext)
steel_entry.bind("<Key>", updatetext)
time_entry.bind("<Key>", updatetext)

root.mainloop()
