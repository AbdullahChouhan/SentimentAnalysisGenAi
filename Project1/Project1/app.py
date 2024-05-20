try:
    import tkinter as tk
    from tkinter import ttk
    from os import path
    from enum import Enum
    import math
except ModuleNotFoundError as e:
    print(f"Couldn't import modules: {e}")
    exit(1)

class Appstate(Enum):
    START = 0
    BUILDING = 1
    RNN = 2
    LSTM = 3
    CNN = 4
    ANALYSIS = 5

class app:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, root):
        if not hasattr(self, 'root'):
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
        self.root.heading1 = ttk.Label(self.root, text="Sentiment Analysis", font=("Helvetica", 24)).pack(pady=20)
        self.root.heading2 = ttk.Label(self.root, text="Select Model").pack()
        self.root.button1 = ttk.Button(self.root, text="LSTM", command=self.rnn).pack()
        self.root.button2 = ttk.Button(self.root, text="CNN", command=self.lstm).pack()
        self.root.button3 = ttk.Button(self.root, text="CNN-LSTM", command=self.cnn).pack()
        
    def updateui(self):
        if self.state == Appstate.START:
            for widget in self.root.winfo_children():
                if widget != self.root.heading1:
                    widget.destroy()
            self.root.heading2 = ttk.Label(self.root, text="Building").pack()
            self.state = Appstate.BUILDING
        
    def rnn(self):
        print("LSTM")
    
    def lstm(self):
        print("CNN")
    
    def cnn(self):
        print("CNN-LSTM")
        
    @classmethod
    def run(cls):
        root = tk.Tk()
        _app_instance = cls(root)
        
        root.mainloop()