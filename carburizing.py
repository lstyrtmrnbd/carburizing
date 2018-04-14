from math import *
import numpy as np
from scipy.special import erf
from scipy.special import erfinv
from tkinter import *
from tkinter import ttk
import matplotlib as plt
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Cx = Cs - (Cs - Co) * erf(x / (2 * (Do * t1 * exp(-Q / (R * T1)))))

class Calculator:

    R  = 1.987     # cal / mol K
    Q  = 32900     # cal / mol
    Cs = 1.3

    def __init__(self):
        self.D0 = 0.23 * 60 # cm^2 / min #\\ changes with C0
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

class Graph:
    
    def __init__(self, X=None, Y=None):
        if X == None: self.X = np.linspace(0, 2 * np.pi, 50)
        if Y == None: self.Y = np.sin(self.X)
        self.fig = plt.figure.Figure(figsize=(6.5, 3.25))
        self.ax = self.fig.add_axes([0.110, 0.15, 0.85, 0.75])

        self.ax.plot(self.X, self.Y)
        self.ax.set_xlabel("Depth (cm)")
        self.ax.set_ylabel("Concentration @ Depth (%C)")
        self.ax.set_title("Carburization")

    def labels(self, xlabel=None, ylabel=None, title=None):
        if xlabel != None: self.ax.set_xlabel(xlabel)
        if ylabel != None: self.ax.set_ylabel(ylabel)
        if title  != None: self.ax.set_title(title)

    def plot(self, X, Y):
        self.X = X
        self.Y = Y
        self.ax.plot(self.X, self.Y)

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
        
def main():
        
    calc = Calculator()

    graph = Graph()
        
    root = Tk()
    mainframe = ttk.Frame(root, padding="3 3 3 3")

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

    calculate = ttk.Button(mainframe, text="Calculate")
    variable_inspect = ttk.Label(mainframe)

    canvas = Canvas(mainframe, width=640, height=320)
    fig_photo =  draw_figure(canvas, graph.fig)

    def init():
        root.title("Carburization Penetration Depth")
        
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

        variable_inspect.grid(column=1, row=6, columnspan=4, sticky=(W, E))
        
        calculate.grid(column=2, row=5, sticky=(W, E))
        calculate.config(command=update)

        canvas.grid(column=3, row=1, columnspan=5, rowspan=5, sticky=N+W)

        root.mainloop() # sticks in here and handles events

    # these callbacks are bound to the calculations
    def selectC0(*args):
        if steel.get() == '1018':
            calc.C0 = .18
        elif steel.get() == '1045':
            calc.C0 = .45

    # sync input with calc
    def update_variables():
        calc.T = tempt.get()
        calc.time = time.get()

    #recalculate callback
    def update_calc():
        calc.update()
        depth.set(calc.x)
        root.update_idletasks()

    #debug callback
    def update_debug():
        #var_string = "D: " + str(calc.D) + " Cx: " + str(calc.Cx) + " z: " + str(calc.z) + " x: " + str(calc.x)
        #x0, y0, w, h = graph.ax.get_position().bounds
        #var_string = "x0: " + str(x0) + " y0: " + str(y0) + " w: " + str(w) + " h: " + str(h)
        var_string = "C0: " + str(calc.C0)
        variable_inspect.configure(text=var_string)
        root.update_idletasks()

    #button update callback    
    def update():
        update_variables()
        update_calc()
        update_debug()

    init()
    
if __name__=="__main__":
   main()

"""
Do=0.23; R=1.987; Q=32900; Cs=1.3;

x=0:.0005:.01; # 0 to .01 increments of .0005 # 0 to 3 instead

Cx1=Cs-(Cs-Co)*erf(x/(2*(Do*t1*exp(-Q/(R*T1)))));

plot(x,Cx1,'g');hold on

xlabel('depth (cm)');
ylabel('concentration @ depth(%C)');
title('Carburization');
"""
