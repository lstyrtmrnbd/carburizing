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

Cs = 0.8

# get C0 value: select 1018 for .0018, 1045 for .0045
steel = StringVar()
C0 = .18

# steel selection callback
def selectC0():
    if steel == '1018':
        C0 = .18
    elif steel == '1045':
        C0 = .45

steel_entry = ttk.Combobox(mainframe, width=7, textvariable=steel)
steel_entry.grid(column=2, row=1, sticky=(W, E))

steel_entry['values'] = ('1018', '1045')
steel_entry.bind("<<ComboboxSelected>>", selectC0)

steel_label = ttk.Label(mainframe, text="Type of Steel:")
steel_label.grid(column=1, row=1, sticky=(W, E))

Cx = C0 + pow(10, -16)

z = (Cs - Cx) / (Cs - C0)
#z = (Cx - C0) / (Cs - C0)

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
#x = 2 * erfinv(1 - z) * pow(D * time.get(), 1/2)

#recalculate callback
def update_calc():
    global D
    global Cx
    global z
    global x
    D = D0 * exp( -Q / (R * T.get()))
    Cx = C0 + pow(10, -16)
    z = (Cs - Cx) / (Cs - C0)
    x = 2 * erfinv(z) * pow(D * time.get(), 1/2)
    root.update_idletasks()

output_result = ttk.Label(mainframe)
output_result.grid(column=2, row=4, sticky=(W, E))

#update output callback
def update_text(event):
    output_result.configure(text=x)
    root.update_idletasks()

temp_entry.bind("<Key>", update_text)
steel_entry.bind("<Key>", update_text)
time_entry.bind("<Key>", update_text)

variable_inspect = ttk.Label(mainframe)
variable_inspect.grid(column=1, row=5, sticky=(W, E))

#debug callback
def update_variable_string():
    var_string = "D: " + str(D) + " Cx: " + str(Cx) + " z: " + str(z) + " x: " + str(x)
    variable_inspect.configure(text=var_string)
    root.update_idletasks()

#button update callback    
def update():
    update_calc()
    output_result.configure(text=x)
    #update_variable_string()

calculate = ttk.Button(mainframe, text="Calculate", command=update)
calculate.grid(column=1, row=6, sticky=(W, E))

root.mainloop()
