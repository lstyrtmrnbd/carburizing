from math import *
from scipy.special import erfinv
from tkinter import *
from tkinter import ttk

#x = 2 * erfinv(z) * sqrt(D * time)
#time = pow(x/(2* erfinv(z))), 2) / D
#T = -Q/(R*log(D/D0)) - 273

class Calculator:

    def __init__(self):
        self.D0 = 0.23 * 60 # cm^2 / min
        self.R  = 1.987     # cal / mol K
        self.Q  = 32900     # cal / mol
        self.T = 950        # temperature (C)
        self.Cs = 1.3
        self.C0 = .18
        self.time = 60
        
        self.D = self.D0 * exp( -self.Q / (self.R * (273 + self.T)))  
        self.Cx = self.C0 + pow(10, -16)
        self.z = (self.Cs - self.Cx) / (self.Cs - self.C0)
        self.x = 2 * erfinv(self.z) * sqrt(self.D * self.time)

    def update():
        self.D = self.D0 * exp( -self.Q / (self.R * (273 + self.T)))  
        self.Cx = self.C0 + pow(10, -16)
        self.z = (self.Cs - self.Cx) / (self.Cs - self.C0)
        self.x = 2 * erfinv(self.z) * sqrt(self.D * self.time)

    def solve_x():
        self.x = 2 * erfinv(self.z) * sqrt(self.D * self.time)

    def solve_time():
        self.time = pow(self.x / (2 * erfinv(self.z))), 2) / self.D

    def solve_T():
        self.T = -self.Q / (self.R * log(self.D / self.D0)) - 273


root = Tk()

root.title("Carburization Penetration Depth")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

D0 = 0.23 * 60 # cm^2 / min
R  = 1.987 # cal / mol K
Q  = 32900 # cal / mol

# get T temperature 900 - 1100
T = DoubleVar()
Tin = DoubleVar()
T.set(950)
Tin.set(950)

def capT(*args):
    global T
    if Tin.get() > 1000:
        Tin.set(1000)
    elif Tin.get() < 900:
        Tin.set(900)
    T.set(Tin.get())

temp_entry = Spinbox(mainframe,from_=900, to=1000, textvariable=Tin)
temp_entry.grid(column=2, row=2, sticky=(W, E))

temp_label = ttk.Label(mainframe, text="Temperature (C)")
temp_label.grid(column=1, row=2, sticky=(W, E))

Tin.trace("w", capT)

D = D0 * exp( -Q / (R * (273 + T.get())))

Cs = 1.3

# get C0 value: select 1018 for .0018, 1045 for .0045
steel = StringVar()
steel.set('1018')
C0 = .18

# steel selection callback
def selectC0(*args):
    global C0
    if steel.get() == '1018':
        C0 = .18
    elif steel.get() == '1045':
        C0 = .45

steel_entry = ttk.Combobox(mainframe, width=7, textvariable=steel)
steel_entry.grid(column=2, row=1, sticky=(W, E))

steel_entry['values'] = ('1018', '1045')
steel_entry.bind("<<ComboboxSelected>>", selectC0)

#steel.trace("w", selectC0)

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

depth = DoubleVar()

output_entry = ttk.Entry(mainframe, width=7, textvariable=depth)
output_entry.grid(column=2, row=4, sticky=(W, E))

output_label = ttk.Label(mainframe, text="Depth (cm):")
output_label.grid(column=1, row=4, sticky=(W, E))

x = 2 * erfinv(z) * sqrt(D * time.get())

#recalculate callback
def update_calc():
    global D
    global Cx
    global z
    global x
    D = D0 * exp( -Q / (R * (273 + T.get())))
    Cx = C0 + pow(10, -16)
    z = (Cs - Cx) / (Cs - C0)
    x = 2 * erfinv(z) * sqrt(D * time.get())
    depth.set(x)
    root.update_idletasks()

output_result = ttk.Label(mainframe)
output_result.grid(column=2, row=4, sticky=(W, E))

variable_inspect = ttk.Label(mainframe)
variable_inspect.grid(column=1, row=5, sticky=(W, E))

#debug callback
def update_variable_string():
    #var_string = "D: " + str(D) + " Cx: " + str(Cx) + " z: " + str(z) + " x: " + str(x)
    var_string = "C0: " + str(C0)
    variable_inspect.configure(text=var_string)
    root.update_idletasks()

#button update callback    
def update():
    update_calc()
    output_result.configure(text=x)
    update_variable_string()

calculate = ttk.Button(mainframe, text="Calculate", command=update)
calculate.grid(column=1, row=6, sticky=(W, E))

root.mainloop()
