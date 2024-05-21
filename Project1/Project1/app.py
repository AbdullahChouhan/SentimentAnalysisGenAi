try:
    import tkinter as tk
    from tkinter import ttk
    from os import path
    from enum import Enum
    from ctypes import windll
    import threading
    # from .text_classification import AI
    from .spinner import Spinner
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
    MODELBUILT = 6
    ANALYSIS = 7

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
            self.style_button()
            self.analysistext = tk.StringVar()
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
        self.root.heading2 = ttk.Label(self.root, text="Select Model", font=("Helvetica", 24)).pack()
        self.root.button1 = ttk.Button(self.root, text="RNN", command=self.rnn, style="MyButton.TButton")
        self.root.button1.pack(pady=10, ipady=5, ipadx=5)
        self.root.button2 = ttk.Button(self.root, text="LSTM", command=self.lstm, style="MyButton.TButton")
        self.root.button2.pack(pady=10, ipady=5, ipadx=5)
        self.root.button3 = ttk.Button(self.root, text="CNN", command=self.cnn, style="MyButton.TButton")
        self.root.button3.pack(pady=10, ipady=5, ipadx=5)
    @classmethod
    def style_button(cls):
        style = ttk.Style()
        style.configure(
            "MyButton.TButton",
            font=("Helvetica", 16),
            padding=5
        )
        style.map(
            "MyButton.TButton",
            background=[('active', '#ffffff'), ('!active', '#ffffff')],
            foreground=[('active', '#000000'), ('!active', '#000000')],
            highlightcolor=[('focus', '#ffffff'), ('!focus', '#ffffff')],
            highlightbackground=[('focus', '#ffffff'), ('!focus', '#ffffff')]
        )
        
    def updateui(self):
        if self.state == Appstate.INPUT:
            for widget in self.root.winfo_children():
                if widget != self.root.heading1:
                    widget.destroy()
            self.root.heading2 = ttk.Label(self.root, text="Building", font=("Helvetica", 24)).pack()
            self.root.loading = Spinner(self.root, size=100, color="blue", num_segments=12, speed=2, width=5)
            self.root.loading.pack()
            self.state = Appstate.BUILDING
            threading.Thread(target=self.root.loading.rotate).start()
            self.root.loading.bind("<Destroy>", lambda event: self.root.loading.on_destroy())
        elif self.state == Appstate.BUILDING:
            # self.root.loading.rotate()
            pass
        elif self.state == Appstate.MODELBUILT:
            self.root.loading.stop()
            for widget in self.root.winfo_children():
                if widget != self.root.heading1:
                    widget.destroy()
            self.root.sentiment = ttk.Label(self.root, text="", font=("Helvetica", 24))
            self.root.currmodel = ttk.Label(self.root, text="Current Model: " + self.modelstate.name, font=("Helvetica", 24)).pack()
            self.root.entry = ttk.Entry(self.root, font=("Helvetica", 24), width=50, textvariable=self.analysistext).pack()
            self.root.button4 = ttk.Button(self.root, text="Analyze", command=self.analyze, style="MyButton.TButton").pack()
            self.root.button5 = ttk.Button(self.root, text="Clear", command=self.clear, style="MyButton.TButton").pack()
            self.root.sentiment.pack()
            self.state = Appstate.ANALYSIS
        elif self.state == Appstate.ANALYSIS:
            pass
            
        self.root.after(50, self.updateui)
        
    def rnn(self):
        print("RNN")
        self.modelstate = Appstate.RNN
        self.startbuild()
    
    def lstm(self):
        print("LSTM")
        self.modelstate = Appstate.LSTM
        self.startbuild()
    
    def cnn(self):
        print("CNN")
        self.modelstate = Appstate.CNN
        self.startbuild()
        
    def startbuild(self):
        self.state = Appstate.INPUT
        self.build()
        
    def build(self):
        # ai = AI()
        # if self.modelstate == Appstate.RNN:
        #     ai.buildRNN_model()
        # elif self.modelstate == Appstate.LSTM:
        #     ai.buildLSTM_model()
        # elif self.modelstate == Appstate.CNN:
        #     ai.buildCNN_model()
        # wait 10 seconds
        def build_task():
            for i in range(20000):
                print(i)
            self.state = Appstate.MODELBUILT
        threading.Thread(target=build_task).start()
        
    def analyze(self):
        if self.analysistext.get() == "":
            self.root.sentiment.config(text="Please enter text")
        else:
            # Reconfigure if checks to model analysis
            if self.analysistext.get() == "Positive":
                self.root.sentiment.config(text="Positive")
                self.root.sentiment.config(foreground="green")
            elif self.analysistext.get() == "Negative":
                self.root.sentiment.config(text="Negative")
                self.root.sentiment.config(foreground="red")
                
    def clear(self):
        self.analysistext.set("")
        self.root.sentiment.config(text="")

    @classmethod
    def run(cls):
        root = tk.Tk()
        _app_instance = cls(root)
        _app_instance.updateui()
        root.mainloop()