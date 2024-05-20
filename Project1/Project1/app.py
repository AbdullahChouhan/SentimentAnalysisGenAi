try:
    import tkinter as tk
    from tkinter import ttk
    from os import path
    from enum import Enum
    import math
    from ctypes import windll
except ModuleNotFoundError as e:
    print(f"Couldn't import modules: {e}")
    exit(1)

class Appstate(Enum):
    START = 0
    INPUT = 1
    BUILDING = 2
    RNN = 3
    LSTM = 4
    CNN = 5
    ANALYSIS = 6
    
class Spinner(tk.Canvas):
    def __init__(self, master, size=50, color="blue", num_segments=12, speed=0.1, width=1, **kwargs):
        super().__init__(master, width=size, height=size, **kwargs)
        self.size = size
        self.color = color
        self.num_segments = num_segments
        self.speed = speed
        self.width = width
        self.angle = 0
        self.segment_size = 360 / self.num_segments
        self.create_segments()

    def create_segments(self):
        for i in range(self.num_segments):
            angle_deg = self.segment_size * i
            start_x = self.size / 2 + math.cos(math.radians(angle_deg)) * (self.size / 3)
            start_y = self.size / 2 + math.sin(math.radians(angle_deg)) * (self.size / 3)
            end_x = self.size / 2 + math.cos(math.radians(angle_deg)) * (self.size / 2)
            end_y = self.size / 2 + math.sin(math.radians(angle_deg)) * (self.size / 2)
            self.create_line(start_x, start_y, end_x, end_y, fill=self.color, width=self.width, tags="spinner")

    def rotate(self):
        self.angle += self.speed
        self.delete("spinner")
        for i in range(self.num_segments):
            angle_deg = self.segment_size * i + self.angle
            start_x = self.size / 2 + math.cos(math.radians(angle_deg)) * (self.size / 3)
            start_y = self.size / 2 + math.sin(math.radians(angle_deg)) * (self.size / 3)
            end_x = self.size / 2 + math.cos(math.radians(angle_deg)) * (self.size / 2)
            end_y = self.size / 2 + math.sin(math.radians(angle_deg)) * (self.size / 2)
            self.create_line(start_x, start_y, end_x, end_y, fill=self.color, width=self.width, tags="spinner")

class app:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, root):
        if not hasattr(self, 'root'):
            windll.shcore.SetProcessDpiAwareness(2)
            self.root = root
            self.root.title("Sentiment Analysis")
            self.setgeometry()
            self.root.resizable(False, False)
            try:
                self.root.iconbitmap(path.join(path.dirname(__file__), 'assets', 'app.ico'))
            except Exception as e:
                print(f"Couldn't set icon: {e}")
            self.state = Appstate.START
            self.setupui()
            
    def setgeometry(self):
        self.root.geometry("600x400")
        
    def setupui(self):
        self.root.heading1 = ttk.Label(self.root, text="Sentiment Analysis", font=("Helvetica", 36)).pack(pady=20)
        self.root.heading2 = ttk.Label(self.root, text="Select Model").pack()
        self.root.button1 = ttk.Button(self.root, text="LSTM", command=self.rnn).pack()
        self.root.button2 = ttk.Button(self.root, text="CNN", command=self.lstm).pack()
        self.root.button3 = ttk.Button(self.root, text="CNN-LSTM", command=self.cnn).pack()
        
    def updateui(self):
        if self.state == Appstate.INPUT:
            for widget in self.root.winfo_children():
                if widget != self.root.heading1:
                    widget.destroy()
            self.root.heading2 = ttk.Label(self.root, text="Building", font=("Helvetica", 24)).pack()
            self.root.loading = Spinner(self.root, size=100, color="blue", num_segments=12, speed=2, width=5)
            self.root.loading.pack()
            self.state = Appstate.BUILDING
        elif self.state == Appstate.BUILDING:
            self.root.loading.rotate()
            
        self.root.after(50, self.updateui)
        
    def rnn(self):
        print("LSTM")
        self.state = Appstate.INPUT
    
    def lstm(self):
        print("CNN")
        self.state = Appstate.INPUT
    
    def cnn(self):
        print("CNN-LSTM")
        self.state = Appstate.INPUT
        
    @classmethod
    def run(cls):
        root = tk.Tk()
        _app_instance = cls(root)
        _app_instance.updateui()
        root.mainloop()