try:
    import tkinter as tk
    import math
    import time
except ModuleNotFoundError as e:
    print(f"Couldn't import modules: {e}")
    exit(1)

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
        self.running = True

    def create_segments(self):
        for i in range(self.num_segments):
            angle_deg = self.segment_size * i
            start_x = self.size / 2 + math.cos(math.radians(angle_deg)) * (self.size / 3)
            start_y = self.size / 2 + math.sin(math.radians(angle_deg)) * (self.size / 3)
            end_x = self.size / 2 + math.cos(math.radians(angle_deg)) * (self.size / 2)
            end_y = self.size / 2 + math.sin(math.radians(angle_deg)) * (self.size / 2)
            self.create_line(start_x, start_y, end_x, end_y, fill=self.color, width=self.width, tags="spinner")

    def rotate(self):
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
        self.running = False
        self.update()
        time.sleep(0.1)
    
    def on_destroy(self):
        self.stop()