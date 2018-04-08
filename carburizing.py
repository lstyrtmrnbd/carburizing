from scipy.special import erfinv
from tkinter import *
from tkinter import ttk

D0 = 0.23
R  = 1.987
Q  = 32900

# get T temperature 900 - 1100

D = D0 * math.exp( -Q / (R * T))

Cs = 1.3

# get C0 value: select 1018 for .0018, 1045 for .0045

Cx = C0 + math.pow(10, -16)

z = (Cs - Cx) / (Cs - C0)

# get t value in minutes

x = 2 * erfinv(z) * math.pow(D * t, 1/2)

root = Tk()

root.title("Carburization Penetration Depth")

ttk.Button(root, text="Hello World").grid()

root.mainloop()
