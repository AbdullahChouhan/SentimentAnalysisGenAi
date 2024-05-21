try:
    import tkinter as tk
    import math
    import time
except ModuleNotFoundError as e:
    print(f"Couldn't import modules: {e}")
    exit(1)

class Spinner(tk.Canvas):
    def __init__(self, master, size=50, color="blue", num_segments=12, speed=0.1, width=1, **kwargs):
        """
        Initializes a new instance of the Spinner class.

        Parameters:
        - master (tkinter.Tk): The master widget.
        - size (int, optional): The size of the spinner in pixels. Defaults to 50.
        - color (str, optional): The color of the spinner. Defaults to "blue".
        - num_segments (int, optional): The number of segments in the spinner. Defaults to 12.
        - speed (float, optional): The speed of rotation in degrees per second. Defaults to 0.1.
        - width (int, optional): The width of the spinner lines in pixels. Defaults to 1.
        - **kwargs: Additional keyword arguments to pass to the tkinter.Canvas constructor.
        """
        super().__init__(master, width=size, height=size, **kwargs)
        self.size = size
        self.color = color
        self.num_segments = num_segments
        self.speed = speed
        self.width = width
        self.angle = 0
        self.segment_size = 360 / self.num_segments
        self.create_segments()
        self.running = True

    def create_segments(self):
        """
        Creates the segments of the spinner.

        This function is responsible for creating the segments of the spinner. It iterates over the range of the number of segments and calculates the angle in degrees for each segment. Then, it calculates the starting and ending coordinates of each segment using the angle, size, and the radius of the spinner. Finally, it creates a line for each segment using the calculated coordinates and the specified color, width, and tags.

        Parameters:
        - self (Spinner): The instance of the Spinner class.
        """
        for i in range(self.num_segments):
            angle_deg = self.segment_size * i
            start_x = self.size / 2 + math.cos(math.radians(angle_deg)) * (self.size / 3)
            start_y = self.size / 2 + math.sin(math.radians(angle_deg)) * (self.size / 3)
            end_x = self.size / 2 + math.cos(math.radians(angle_deg)) * (self.size / 2)
            end_y = self.size / 2 + math.sin(math.radians(angle_deg)) * (self.size / 2)
            self.create_line(start_x, start_y, end_x, end_y, fill=self.color, width=self.width, tags="spinner")

    def rotate(self):
        """
        Rotates the spinner by incrementing the angle by the speed and redrawing the segments.

        This method continuously rotates the spinner by incrementing the angle by the speed until the running flag is set to False. It deletes the existing spinner segments and redraws them using the updated angle. The angle is calculated by multiplying the segment size by the index of the segment and adding the current angle. The starting and ending coordinates of each segment are calculated using the angle, size, and the radius of the spinner. The create_line method is called to create a line for each segment with the specified color, width, and tags. The method sleeps for 0.05 seconds between each iteration to control the rotation speed.

        Parameters:
        - self (Spinner): The instance of the Spinner class.
        """
        while self.running:
            self.angle += self.speed
            self.delete("spinner")
            for i in range(self.num_segments):
                angle_deg = self.segment_size * i + self.angle
                start_x = self.size / 2 + math.cos(math.radians(angle_deg)) * (self.size / 3)
                start_y = self.size / 2 + math.sin(math.radians(angle_deg)) * (self.size / 3)
                end_x = self.size / 2 + math.cos(math.radians(angle_deg)) * (self.size / 2)
                end_y = self.size / 2 + math.sin(math.radians(angle_deg)) * (self.size / 2)
                self.create_line(start_x, start_y, end_x, end_y, fill=self.color, width=self.width, tags="spinner")
            time.sleep(0.05)
            
    def stop(self):
        """
        Graceful thread termination. Stop the spinner by setting the running flag to False, updating the canvas, and giving the running thread a short time to finish.

        This method stops the spinner by setting the `running` flag to False, calling the `update` method to redraw the canvas, and sleeping for 0.01 seconds to ensure the spinner has finished rotating.

        Parameters:
        - self (Spinner): The instance of the Spinner class.
        """
        self.running = False
        self.update()
        time.sleep(0.01)
    
    def on_destroy(self):
        """
        Graceful thread termination. Stop the spinner by setting the running flag to False, updating the canvas, and giving the running thread a short time to finish.

        This method stops the spinner by calling the `stop` method, which sets the `running` flag to False, updates the canvas, and sleeps for 0.01 seconds to ensure the spinner has finished rotating.

        Parameters:
        - self (Spinner): The instance of the Spinner class.
        """
        self.stop()