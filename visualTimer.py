import tkinter as tk
import os
from PIL import Image, ImageTk  # make sure Pillow library is installed

class StandaloneTimer:
    def __init__(self, master, timer_width=120):
        self.master = master
        self.master.overrideredirect(True)
        self.master.wm_attributes('-topmost', True)
        self.master.wm_attributes('-transparentcolor', 'white')

        self.impath = os.path.join(os.path.dirname(__file__), 'image')

        # scale
        pil_timer = Image.open(os.path.join(self.impath, "cartoonTimerEditpng.png"))
        orig_width, orig_height = pil_timer.size

        # calculate height proportionally
        scale_factor = timer_width / orig_width
        timer_height = int(orig_height * scale_factor)
        pil_timer = pil_timer.resize((timer_width, timer_height), Image.Resampling.LANCZOS)
        self.timer_image = ImageTk.PhotoImage(pil_timer)

        canvas_width = timer_width + 40
        canvas_height = timer_height + 40
        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height,
                                bg='white', highlightthickness=0)
        self.canvas.pack()

        # timer image centered in canvas
        self.timer_x = canvas_width // 2
        self.timer_y = canvas_height // 2 - 5  # adjust vertical placement
        self.timer_item = self.canvas.create_image(self.timer_x, self.timer_y, image=self.timer_image)

        # timer text over image
        self.time_left = 25*60  # default 25 minutes
        font_size_multiplier = 15
        self.timer_text_item = self.canvas.create_text(
            self.timer_x,
            self.timer_y - 17,  # slightly above center of timer image
            text=self.format_time(self.time_left),
            font=("DS-Digital", font_size_multiplier),
            fill="white",
            anchor="center"
        )

        self.running = False
        self.update_timer()

    def format_time(self, sec):
        return f"{sec // 60:02d}:{sec % 60:02d}"

    def update_timer(self):
        if self.running:
            if self.time_left > 0:
                self.time_left -= 1
                self.canvas.itemconfig(self.timer_text_item, text=self.format_time(self.time_left))
        self.master.after(1000, self.update_timer)

    def start_countdown(self, seconds=None):
        if seconds is not None:
            self.time_left = seconds
        self.running = True

    def stop_countdown(self):
        self.running = False


if __name__ == "__main__":
    root = tk.Tk()
    timer = StandaloneTimer(root, timer_width=120)  # adjust width here
    timer.start_countdown()
    root.mainloop()