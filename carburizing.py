import matplotlib as plt
from math import *
from scipy.special import erfinv
from tkinter import *
from tkinter import ttk
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

#x = 2 * erfinv(z) * sqrt(D * time)
#time = pow(x/(2* erfinv(z))), 2) / D
#T = -Q/(R*log(D/D0)) - 273

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

    fig = plt.figure.Figure(figsize=(8, 4))

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

        variable_inspect.grid(column=1, row=6, sticky=(W, E))
        
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
x=0:.0005:.01; # 0 to .01 increments of .0005
prompt='what is the value for T1?';
T1=input(prompt);
prompt='what is the value for T2?';
T2=input(prompt);
prompt='what is the value for T3?';
T3=input(prompt);
prompt='what is the value for t1?';
t1=input(prompt);
prompt='what is the value for t2?';
t2=input(prompt);
prompt='what is the value for t3?';
t3=input(prompt);
prompt='what is the value for t4?';
t4=input(prompt);
prompt='what is the value for Co?';
Co=input(prompt);
Cx1=Cs-(Cs-Co)*erf(x/(2*(Do*t1*exp(-Q/(R*T1)))));
Cx2=Cs-(Cs-Co)*erf(x/(2*(Do*t2*exp(-Q/(R*T1)))));
Cx3=Cs-(Cs-Co)*erf(x/(2*(Do*t3*exp(-Q/(R*T1)))));
Cx4=Cs-(Cs-Co)*erf(x/(2*(Do*t4*exp(-Q/(R*T1)))));
Cx5=Cs-(Cs-Co)*erf(x/(2*(Do*t1*exp(-Q/(R*T2)))));
Cx6=Cs-(Cs-Co)*erf(x/(2*(Do*t2*exp(-Q/(R*T2)))));
Cx7=Cs-(Cs-Co)*erf(x/(2*(Do*t3*exp(-Q/(R*T2)))));
Cx8=Cs-(Cs-Co)*erf(x/(2*(Do*t4*exp(-Q/(R*T2)))));
Cx9=Cs-(Cs-Co)*erf(x/(2*(Do*t1*exp(-Q/(R*T3)))));
Cx10=Cs-(Cs-Co)*erf(x/(2*(Do*t2*exp(-Q/(R*T3)))));
Cx11=Cs-(Cs-Co)*erf(x/(2*(Do*t3*exp(-Q/(R*T3)))));
Cx12=Cs-(Cs-Co)*erf(x/(2*(Do*t4*exp(-Q/(R*T3)))));
plot(x,Cx1,'g');hold on
plot(x,Cx2,'b');hold on
plot(x,Cx3,'r');hold on
plot(x,Cx4,'c');hold on
plot(x,Cx5,'--g');hold on
plot(x,Cx6,'--b');hold on
plot(x,Cx7,'--r');hold on
plot(x,Cx8,'--c');hold on
plot(x,Cx9,':g');hold on
plot(x,Cx10,':b');hold on
plot(x,Cx11,':r');hold on
plot(x,Cx12,':c');hold off
xlabel('depth (cm)');
ylabel('concentration @ depth(%C)');
title('Carburization');
"""
