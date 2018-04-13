from math import *
from scipy.special import erfinv
from tkinter import *
from tkinter import ttk

#x = 2 * erfinv(z) * sqrt(D * time)
#time = pow(x/(2* erfinv(z))), 2) / D
#T = -Q/(R*log(D/D0)) - 273

class Calculator:

    R  = 1.987     # cal / mol K
    Q  = 32900     # cal / mol
    Cs = 1.3

    def __init__(self):
        self.D0 = 0.23 * 60 # cm^2 / min // changes with C0
        self.T = 950        # temperature (C)
        self.C0 = .18
        self.time = 60      # min
        
        self.D = self.D0 * exp( -Calculator.Q / (Calculator.R * (273 + self.T)))  
        self.Cx = self.C0 + pow(10, -16)
        self.z = (Calculator.Cs - self.Cx) / (Calculator.Cs - self.C0)
        self.x = 2 * erfinv(self.z) * sqrt(self.D * self.time)

    def update(self):
        self.D = self.D0 * exp( -Calculator.Q / (Calculator.R * (273 + self.T)))  
        self.Cx = self.C0 + pow(10, -16)
        self.z = (Calculator.Cs - self.Cx) / (Calculator.Cs - self.C0)
        self.x = 2 * erfinv(self.z) * sqrt(self.D * self.time)

    def solve_x(self):
        self.x = 2 * erfinv(self.z) * sqrt(self.D * self.time)

    def solve_time(self):
        self.time = pow(self.x / (2 * erfinv(self.z)), 2) / self.D

    def solve_tempt(self):
        self.T = -Calculator.Q / (Calculator.R * log(self.D / self.D0)) - 273

def main():
        
    calc = Calculator()
        
    root = Tk()
    mainframe = ttk.Frame(root, padding="3 3 12 12")

    # tie these to calc variables
    tempt = DoubleVar()
    steel = StringVar()
    time = DoubleVar()
    depth = DoubleVar()

    temp_entry = Spinbox(mainframe,from_=900, to=1000, textvariable=tempt)
    temp_label = ttk.Label(mainframe, text="Temperature (C)")
    
    steel_entry = ttk.Combobox(mainframe, width=7, textvariable=steel)
    steel_label = ttk.Label(mainframe, text="Type of Steel:")

    time_entry = ttk.Entry(mainframe, width=7, textvariable=time)
    time_label = ttk.Label(mainframe, text="Time (min.)")

    output_entry = ttk.Entry(mainframe, width=7, textvariable=depth)
    output_label = ttk.Label(mainframe, text="Depth (cm):")
    output_result = ttk.Label(mainframe)

    calculate = ttk.Button(mainframe, text="Calculate")
    variable_inspect = ttk.Label(mainframe)
    

    def init():      
        tempt.set(950)
        steel.set('1018')
        time.set(60)

        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        temp_entry.grid(column=2, row=2, sticky=(W, E))
        temp_label.grid(column=1, row=2, sticky=(W, E))

        steel_entry['values'] = ('1018', '1045')
        steel_entry.grid(column=2, row=1, sticky=(W, E))
        steel_entry.bind("<<ComboboxSelected>>", selectC0)

        steel_label.grid(column=1, row=1, sticky=(W, E))

        time_entry.grid(column=2, row=3, sticky=(W, E))
        time_label.grid(column=1, row=3, sticky=(W, E))

        output_entry.grid(column=2, row=4, sticky=(W, E))
        output_label.grid(column=1, row=4, sticky=(W, E))

        output_result.grid(column=2, row=4, sticky=(W, E))

        variable_inspect.grid(column=1, row=5, sticky=(W, E))
        
        calculate.grid(column=1, row=6, sticky=(W, E))
        calculate.config(command=update)

        root.mainloop() # sticks in here and handles events

    # these callbacks are bound to the calculations
    def selectC0(*args):
        if steel.get() == '1018':
            calc.C0 = .18
        elif steel.get() == '1045':
            calc.C0 = .45

    def update_variables():
        calc.T = tempt.get()
        calc.time = time.get()

    #recalculate callback
    def update_calc():
        calc.update()
        depth.set(calc.x)
        root.update_idletasks()

    #debug callback
    def update_variable_string():
        #var_string = "D: " + str(calc.D) + " Cx: " + str(calc.Cx) + " z: " + str(calc.z) + " x: " + str(calc.x)
        var_string = "C0: " + str(calc.C0)
        variable_inspect.configure(text=var_string)
        root.update_idletasks()

    #button update callback    
    def update():
        update_variables()
        update_calc()
        output_result.configure(text=calc.x)
        update_variable_string()

    init()
    
main()
