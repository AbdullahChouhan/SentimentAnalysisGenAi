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
    """
    A class representing the main application of the sentiment analysis tool.
    
    This class contains methods and attributes for setting up and managing the GUI of the application.
    
    Attributes:
    - root (tkinter.Tk): The main window of the application.
    - state (Appstate): The current state of the application.
    - modelstate (Appstate): The current model selected by the user.
    - analysistext (tk.StringVar): A variable for storing the text to be analyzed.
    
    Methods:
    - __init__: Initializes the application with the given root window.
    - __new__: A singleton method for ensuring only one instance of the class is created.
    - setgeometry: Sets up the geometry of the root window.
    - setupui: Sets up the UI of the application.
    - style_button: Sets up the style of the buttons in the application.
    - updateui: Updates the UI of the application based on its current state.
    - rnn: Starts the process of building an RNN model.
    - lstm: Starts the process of building an LSTM model.
    - cnn: Starts the process of building a CNN model.
    - startbuild: Starts the process of building the model selected by the user.
    - build: The method for building the model.
    - analyze: Analyzes the text in the entry box using the current model.
    - clear: Clears the text in the entry box.
    """
    _instance = None
    def __new__(cls, *args, **kwargs):
        """
        Create and return a singleton instance of the class.

        This method ensures that only one instance of the class is created and returned. It checks if the class has an existing instance stored in the `_instance` attribute. If it does, it returns the existing instance. Otherwise, it creates a new instance using the `super().__new__(cls)` method and stores it in the `_instance` attribute.

        Parameters:
        - cls (type): The class object.
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.

        Returns:
        - The singleton instance of the class.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, root):
        """
        Initializes the application with the given root window.

        This method sets up the main window of the application and initializes its attributes. It sets the DPI awareness level, sets the window title, sets the window geometry, disables resizing, styles the buttons, initializes the analysis text variable, sets the window icon, sets the initial state of the application, and sets up the UI.

        Parameters:
        - root (tkinter.Tk): The main window of the application.
        """
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
        """
        Sets the geometry of the root window to 600x400.

        This method is used to set the size of the main window of the application. It takes no parameters and does not return anything.
        """
        self.root.geometry("600x400")
        
    def setupui(self):
        """
        Sets up the UI of the application.

        This method creates and configures the labels and buttons for the main window of the application. It sets the text, font, and style of the labels, and sets the text, command, and style of the buttons. The buttons are packed into the main window with padding and internal padding.

        Parameters:
        - self: The instance of the class.
        """
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
        """
        Configures the style of the button widget.

        This class method sets the font and padding for the "MyButton.TButton" style. It also maps the background, foreground, highlightcolor, and highlightbackground properties for different button states.

        Parameters:
        - cls (type): The class object.
        """
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
        """
        Updates the user interface based on the current state of the application.

        This method is responsible for updating the user interface of the application based on its current state. It performs different actions depending on the value of the `state` attribute.

        If the state is `Appstate.INPUT`, the method destroys all the widgets in the main window except for the heading1 label. It then creates a new heading2 label with the text "Building" and packs it into the main window. It also creates a new loading Spinner widget with specified size, color, number of segments, speed, and width. The loading widget is packed into the main window. The state is changed to `Appstate.BUILDING` and a new thread is started to rotate the loading widget. A binding is created to stop the loading widget when it is destroyed.

        If the state is `Appstate.BUILDING`, the method is an intermediate state. It does nothing.

        If the state is `Appstate.MODELBUILT`, the method stops the loading widget rotation. It destroys all the widgets in the main window except for the heading1 label. It creates a new sentiment label with an empty text and packs it into the main window. It also creates a new currmodel label with the text "Current Model: " followed by the name of the current model state. It packs the currmodel label into the main window. It creates a new entry widget with specified font, width, and textvariable. The entry widget is packed into the main window. It creates two new buttons with the text "Analyze" and "Clear" respectively, and specified command and style. The buttons are packed into the main window. The sentiment label is packed into the main window. The state is changed to `Appstate.ANALYSIS`.

        If the state is `Appstate.ANALYSIS`, the method is an intermediate state. It does nothing.

        After performing the necessary actions, the method schedules itself to be called again after 50 milliseconds using the `after` method of the main window.

        Parameters:
        - self: The instance of the class.
        """
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
        """
        Sets the model state to Appstate.RNN and starts the build process.

        This function prints "RNN" to the console and updates the model state to Appstate.RNN. It then calls the startbuild() method to begin the build process.

        Parameters:
        - self (object): The instance of the class.
        """
        print("RNN")
        self.modelstate = Appstate.RNN
        self.startbuild()
    
    def lstm(self):
        """
        Sets the model state to Appstate.LSTM and starts the build process.

        This function prints "LSTM" to the console and updates the model state to Appstate.LSTM. It then calls the startbuild() method to begin the build process.

        Parameters:
        - self (object): The instance of the class.
        """
        print("LSTM")
        self.modelstate = Appstate.LSTM
        self.startbuild()
    
    def cnn(self):
        """
        Sets the model state to Appstate.CNN and starts the build process.

        This function prints "CNN" to the console and updates the model state to Appstate.CNN. It then calls the startbuild() method to begin the build process.

        Parameters:
        - self (object): The instance of the class.
        """
        print("CNN")
        self.modelstate = Appstate.CNN
        self.startbuild()
        
    def startbuild(self):
        """
        Starts the build process by setting the state to Appstate.INPUT and calling the build() method.

        This function sets the state attribute of the object to Appstate.INPUT, indicating that the build process is about to begin. It then calls the build() method to perform the actual build.

        Parameters:
        - self (object): The instance of the class.
        """
        self.state = Appstate.INPUT
        self.build()
        
    def build(self):
        """
        Builds the model based on the current model state.

        This function is responsible for building the model based on the current model state. It creates a new thread that runs the `build_task` function. The `build_task` function builds the user-selected model and then sets the state of the object to `Appstate.MODELBUILT`.

        Parameters:
        - self (object): The instance of the class.
        """
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
        """
        Analyzes the input text and updates the sentiment label accordingly.

        This function checks if the analysis text is empty. If it is, it updates the sentiment label to display the message "Please enter text". If the analysis text is not empty, it checks the sentiment of the text and updates the sentiment label accordingly. The sentiment label is colour-coded accordingly.

        Parameters:
        - self (object): The instance of the class.
        """
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
        """
        Clears the analysis text and resets the sentiment label.

        This function clears the `analysistext` variable by setting it to an empty string. It also resets the `text` attribute of the `sentiment` widget to an empty string.

        Parameters:
        - self (object): The instance of the class.
        """
        self.analysistext.set("")
        self.root.sentiment.config(text="")

    @classmethod
    def run(cls):
        """
        Run the application.

        This class method initializes a Tkinter root window, creates an instance of the class with the root window, and calls the `updateui` method to update the user interface. It then enters the Tkinter main loop to start the application.

        Parameters:
        - cls (type): The class object.
        """
        root = tk.Tk()
        _app_instance = cls(root)
        _app_instance.updateui()
        root.mainloop()