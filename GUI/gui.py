import ttkbootstrap as ttk
import tkinter as tk

class Main(ttk.Window):
    def __init__(self, title, dimensions):
        super().__init__(self)
        self.title(title)
        self.geometry(dimensions)

    def __str__(self):
        return super().__str__()

class APIconsumer():
    def __init__(self,title, dimensions):
        self.main = Main(title, dimensions)
        self.mainFrame = self.CreateMainFrame(self.main, "750x450")
        self.CreateContentWindow()
        self.main.mainloop()

    def CreateContentWindow(self):
        instruction = ttk.Label(self.mainFrame, text= "The API endpoint is:")
        
        boton = ttk.Button(self.mainFrame, text= "API Consumer")
        instruction.pack()
        boton.pack()

    def CreateMainFrame(self, parent, dimensions):
        dimensions  = dimensions.split('x')
        width = dimensions[0]
        height = dimensions[1]
        frame = ttk.Frame(parent, height=height, width=width)
        frame.place(x=40, y=25, relwidth=0.9, relheight=0.9)
        return frame


APIconsumer("Baruch", "800x500")