from math import *
from decimal import *
import numpy as np
from scipy.special import erf
from scipy.special import erfinv
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import matplotlib as plt
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

## holds current time temp and depth and recalculates when necessary
class Calculator:

    R  = 1.987     # cal / mol K
    Q  = 32900     # cal / mol

    def __init__(self):
        self.D0 = 0.23 * 60 # cm^2 / min #\\ changes with C0
        self.T = 950        # temperature (C)
        self.C0 = .18
        self.time = 60      # min
        
        self.update()
        self.solve_x()
        
    def update(self):
        self.Cs = (self.T - 485) / 285
        self.D = self.D0 * exp( -Calculator.Q / (Calculator.R * (273 + self.T)))  
        self.Cx = self.C0 + pow(10, -15)
        self.z = (self.Cs - self.Cx) / (self.Cs - self.C0)

    def solve_x(self):
        self.x = 2 * erfinv(self.z) * sqrt(self.D * self.time)

    def solve_time(self):
        self.time = pow(self.x / (2 * erfinv(self.z)), 2) / self.D

    def solve_tempt(self):
        self.T = -Calculator.Q / (2 * Calculator.R * log(self.x / (2 * sqrt(self.D0 * self.time) * erfinv(self.z)))) - 273

    def cx_solver(self):
        return lambda x: self.Cs - (self.Cs - self.C0) * erf(x / (2 * (self.D0 * (60 * self.time) * exp(-Calculator.Q / (Calculator.R * (self.T + 273))))))

## stateless Calculator alternative and assistant    
class Solve:

    R = 1.87
    Q = 32900
    
    def Cs(temp):
        return (temp - 485) / 285

    def D(D0, temp):
        return D0 * exp(Q / R * (273 + temp))

    def Cx(C0):
        return C0 + pow(10, -16)

    def z(C0, Cs, Cx):
        return (Cs - Cx) / (Cs - C0)
    
    def x(z, D, time):
        return 2 * erfinv(z) * sqrt(D * time)

    def time(x, z, D):
        return pow(x / (2 * erfinv(z)), 2) / D

    def temp(x, D0, time, z):
        return -Q / (2 * R * log(x / (2 * sqrt(D0 * time) * erfinv(z)))) - 273 

    def cx(Cs, C0, x, D0, time, temp):
        return lambda x: Cs - (Cs - C0) * erf(x / (2 * (D0 * (60 * time) * exp(-Q / (R * (temp + 273))))))

    # return the same cx_solver as a Calculator but with time scaled by s
    def cx_time(calc, s):
        return lambda x: calc.Cs - (calc.Cs - calc.C0) * erf(x / (2 * (calc.D0 * (60 * calc.time * s) * exp(-Calculator.Q / (Calculator.R * (calc.T + 273))))))

## maintains the plotting state and functionality
class Graph:
    
    def __init__(self, X=None, Y=None):
        if X == None: self.X = np.linspace(0, 2 * np.pi, 50)
        if Y == None: self.Y = np.sin(self.X)
        self.fig = plt.figure.Figure(figsize=(6.5, 3.25))
        self.ax = self.fig.add_axes([0.110, 0.15, 0.85, 0.75]) # parameter is very specific layout offsets

        self.ax.plot(self.X, self.Y)
        self.ax.set_xlabel("Depth (cm)")
        self.ax.set_ylabel("Concentration @ Depth (wt%C)")
        self.ax.set_title("Carburization")

    def labels(self, xlabel=None, ylabel=None, title=None):
        if xlabel != None: self.ax.set_xlabel(xlabel)
        if ylabel != None: self.ax.set_ylabel(ylabel)
        if title  != None: self.ax.set_title(title)

    def plot(self, X, Y):
        self.ax.clear()
        self.ax.plot(X, Y)

    def multiplot(self, X, Ylist):
        self.ax.clear()
        for Y in Ylist:
            self.ax.plot(X, Y)

def draw_figure(canvas, figure, loc=(0, 0)):
    """ 
    Draw a matplotlib figure onto a Tk canvas
    """
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = PhotoImage(master=canvas, width=figure_w, height=figure_h)

    # Position: convert from top-left anchor to center anchor
    canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

    # Unfortunately, there's no accessor for the pointer to the native renderer
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    # Return a handle which contains a reference to the photo object
    # which must be kept live or else the picture disappears
    return photo

## chops off decimals for the calculation results
def truncate(number, decs=3):
    places = Decimal(10) ** -decs
    return Decimal(number).quantize(places, rounding=ROUND_HALF_UP)

def main():     
    calc = Calculator()

    graph = Graph()
        
    root = Tk()

    mainframe = ttk.Frame(root, padding="3 3 3 3")

    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    optionsmenu = Menu(menubar, tearoff=0)
    
    tempt = DoubleVar()
    steel = StringVar()
    time = DoubleVar()
    depth = DoubleVar()
    solve_for = StringVar()

    temp_entry = ttk.Entry(mainframe, textvariable=tempt)
    temp_label = ttk.Label(mainframe, text="Temperature (C)")
    steel_entry = ttk.Combobox(mainframe, width=7, textvariable=steel)
    steel_label = ttk.Label(mainframe, text="Type of Steel")
    time_entry = ttk.Entry(mainframe, width=7, textvariable=time)
    time_label = ttk.Label(mainframe, text="Time (min.)")
    output_entry = ttk.Entry(mainframe, width=7, textvariable=depth)
    output_label = ttk.Label(mainframe, text="Depth (cm)")
    radio_tempt = ttk.Radiobutton(mainframe, variable=solve_for, value="temperature")
    radio_time = ttk.Radiobutton(mainframe, variable=solve_for, value="time")
    radio_depth = ttk.Radiobutton(mainframe, variable=solve_for, value="depth")
    
    calculate = ttk.Button(mainframe, text="Calculate")
    variable_inspect = ttk.Label(mainframe)
    canvas = Canvas(mainframe, width=640, height=320)
    fig_photo =  draw_figure(canvas, graph.fig)

    def init():
        root.title("Carburization Penetration Depth")

        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Export Graph", command=export_graph)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=root.quit)
        menubar.add_cascade(label="Options", menu=optionsmenu)
        optionsmenu.add_command(label="Imperial/Metric", command=do_nothing)
        root.config(menu=menubar)
        
        tempt.set(calc.T)
        steel.set('1018')
        time.set(calc.time)
        depth.set(truncate(calc.x))
        solve_for.set("depth")

        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        radio_tempt.grid(column=3, row=2)
        radio_time.grid(column=3, row=3)
        radio_depth.grid(column=3, row=4)
        temp_label.grid(column=1, row=2, sticky=(W, E))        
        temp_entry.grid(column=2, row=2, sticky=(W, E))
        steel_label.grid(column=1, row=1, sticky=(W, E))
        steel_entry.grid(column=2, row=1, sticky=(W, E))
        steel_entry['values'] = ('1018', '1045')
        steel_entry.bind("<<ComboboxSelected>>", selectC0)
        time_label.grid(column=1, row=3, sticky=(W, E))        
        time_entry.grid(column=2, row=3, sticky=(W, E))
        output_label.grid(column=1, row=4, sticky=(W, E))
        output_entry.grid(column=2, row=4, sticky=(W, E))
        
        variable_inspect.grid(column=1, row=6, columnspan=4, rowspan=2, sticky=(W, E))
        calculate.grid(column=2, row=5, sticky=(W, E))
        calculate.config(command=update)
        canvas.grid(column=4, row=1, columnspan=5, rowspan=5, sticky=N+W)

        set_graph(4, 2) # INTIAL SET_GRAPH()

        root.mainloop() # sticks in here and handles events

    ## graph write out
    def set_graph(count=1, multiple=1):
        nonlocal fig_photo
        X = np.arange(0, calc.x, 0.005)
        Ylist = []
        for x in range(count):
            Cx = np.vectorize(Solve.cx_time(calc, multiple * (1 + x)))
            Ylist.append(Cx(X))

        graph.multiplot(X, Ylist)
        graph.labels("Depth (cm)", "Concentration @ Depth (wt%C)", "Carburization")
        fig_photo = draw_figure(canvas, graph.fig)
        
    ## steel type selection
    def selectC0(*args):
        if steel.get() == '1018':
            calc.C0 = .18
        elif steel.get() == '1045':
            calc.C0 = .45

    ## sync input with calc
    def update_variables():
        solve = solve_for.get()
        if solve == "depth":
            calc.T = tempt.get()
            calc.time = time.get()
        elif solve == "temperature":
            calc.time = time.get()
            calc.x = depth.get()
        elif solve == "time":
            calc.T = tempt.get()
            calc.x = depth.get()

    ## recalculations made here
    def update_calc():
        calc.update()
        solve = solve_for.get()
        if solve == "depth":
            calc.solve_x()
            depth.set(truncate(calc.x))
        elif solve == "temperature":
            calc.solve_tempt()
            tempt.set(truncate(calc.T))
        elif solve == "time":
            calc.solve_time()
            time.set(truncate(calc.time))
            
        root.update_idletasks()

    ## debugging write out
    def update_debug(debug_string=None):
        calc_vars_check = "D: " + str(calc.D) + " Cx: " + str(calc.Cx) + " z: " + str(calc.z) + " x: " + str(calc.x)
        out_vars_check = "x: " + str(calc.x) + " time: " + str(calc.time) + " temp: " + str(calc.T)
        x0, y0, w, h = graph.ax.get_position().bounds
        ax_size_check = "x0: " + str(x0) + " y0: " + str(y0) + " w: " + str(w) + " h: " + str(h)
        C0_check = "C0: " + str(calc.C0)
        x_ticks = graph.ax.get_xticks()
        
        if debug_string == None:
            var_string = out_vars_check
        else:
            var_string = debug_string
            
        variable_inspect.configure(text=var_string)
        root.update_idletasks()

    ## button update    
    def update():
        update_variables()
        update_calc()
        set_graph(4, 2)
        update_debug()

    ## --- menu callbacks ---
    ## File -> Export Graph
    def export_graph():
        savename = filedialog.asksaveasfilename(defaultextension=".png")
        if savename != "":
            graph.fig.savefig(savename, format="png")

    ## placeholder command
    def do_nothing():
        return None

    init()
    
if __name__=="__main__":
   main()
