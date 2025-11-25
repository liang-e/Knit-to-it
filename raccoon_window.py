import os
import tkinter as tk
from tkinter import Entry, StringVar, messagebox
from PIL import Image, ImageTk

class RaccoonWindow:

    def __init__(self, window, x=1400, y=700, dimension=128):

        self.impath = os.path.join(os.path.dirname(__file__), 'image', '')  # image directory
        self.raccoon_knitting = [tk.PhotoImage(file=self.impath + 'raccoon_knitting.gif', format='gif -index %i' % i) for i in range(2)]
        self.raccoon_idle = [tk.PhotoImage(file=self.impath + 'raccoon_idle.gif', format='gif -index %i' % i) for i in range(2)]
        self.raccoon_sad_idle = [tk.PhotoImage(file=self.impath + 'raccoon_sad.gif', format='gif -index %i' % i) for i in range(3)]
        self.raccoon_sad_knitting = [tk.PhotoImage(file=self.impath + 'raccoon_sad_knitting.gif', format='gif -index %i' % i) for i in range(2)]

        # Positioning and size
        self.x = x
        self.y = y
        self.dimension = dimension
        self.window = window
        self.state = "idle"
        self.gif = self.raccoon_idle
        self.frame = 0

        # Drag variables
        self.drag_start_x = 0
        self.drag_start_y = 0

        # Timer variables
        self.hour = StringVar(value="00")
        self.minute = StringVar(value="00")
        self.second = StringVar(value="00")
        self.remaining_seconds = 0
        self.timer_running = False
        self.timer_window = None
        self._after_id = None

        # Window setup
        self.window.geometry(f"{dimension}x{dimension}+{x}+{y}")
        self.window.overrideredirect(True)
        self.window.wm_attributes('-transparentcolor', 'red')
        self.window.wm_attributes('-topmost', True)


        # Pet label
        self.label = tk.Label(self.window, bd=0, bg='red')
        self.label.pack()
        self.label.bind('<Button-3>', self.on_right_click)
        self.label.bind('<Button-1>', self.start_drag)
        self.label.bind('<B1-Motion>', self.on_drag)

        self.__play_gif()

    # ---------------------- DRAG ----------------------
    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag(self, event):
        new_x = self.window.winfo_x() + (event.x - self.drag_start_x)
        new_y = self.window.winfo_y() + (event.y - self.drag_start_y)
        self.window.geometry(f'+{new_x}+{new_y}')
        self.x, self.y = new_x, new_y

    # ---------------------- GIF ----------------------
    def __play_gif(self):
        self.label.configure(image=self.gif[self.frame])
        self.frame = (self.frame + 1) % len(self.gif)
        delay = 1000
        if self.state == "sad_pomodoro":
            delay = 1800
        elif self.state == "sad_idle":
            delay = 500
        self.window.after(delay, self.__play_gif)

    def __set_state(self, state):
        self.state = state
        self.frame = 0
        if state == "pomodoro":
            self.gif = self.raccoon_knitting
        elif state == "idle":
            self.gif = self.raccoon_idle
        elif state == "sad_idle":
            self.gif = self.raccoon_sad_idle
        elif state == "sad_pomodoro":
            self.gif = self.raccoon_sad_knitting

    # ---------------------- TIMER UI ----------------------
    def _setup_timer_ui(self):
        if hasattr(self, 'hour_entry'):
            return
        if self.timer_window is None:
            self.timer_window = tk.Toplevel(self.window)
        win = self.timer_window
        win.geometry("360x200")
        win.title("Pomodoro Timer")
        win.resizable(False, False)

        # Load and resize background
        raw_bg = Image.open(os.path.join(self.impath, 'background.png'))
        resized_bg = raw_bg.resize((360, 200), Image.Resampling.LANCZOS)
        self.timer_bg = ImageTk.PhotoImage(resized_bg)

        # Background label (fills timer window)
        bg_label = tk.Label(win, image=self.timer_bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Now place your timer widgets on top
        self.hour_entry = Entry(win, width=3, font=("Arial", 28), textvariable=self.hour,
                                state='readonly', readonlybackground="#2c3e50", fg="white", justify='center')
        self.hour_entry.place(x=60, y=30)
        tk.Label(win, text=":", font=("Arial", 28), bg="#2c3e50", fg="white").place(x=115, y=30)
        self.minute_entry = Entry(win, width=3, font=("Arial", 28), textvariable=self.minute,
                                  state='readonly', readonlybackground="#2c3e50", fg="white", justify='center')
        self.minute_entry.place(x=140, y=30)
        tk.Label(win, text=":", font=("Arial", 28), bg="#2c3e50", fg="white").place(x=195, y=30)
        self.second_entry = Entry(win, width=3, font=("Arial", 28), textvariable=self.second,
                                  state='readonly', readonlybackground="#2c3e50", fg="white", justify='center')
        self.second_entry.place(x=220, y=30)

    def __start_timer(self, state, fresh=True):
        self.__set_state(state)
        if not hasattr(self, 'hour_entry'):
            self._setup_timer_ui()
        self.timer_window.deiconify()
        self.timer_window.lift()
        if fresh and state in ("pomodoro", "sad_pomodoro"):
            self.remaining_seconds = 25 * 60
        self.__update_display()
        self.timer_running = True
        self.__countdown()

    def __update_display(self):
        mins, secs = divmod(self.remaining_seconds, 60)
        hours, mins = divmod(mins, 60)
        self.hour.set(f"{hours:02d}")
        self.minute.set(f"{mins:02d}")
        self.second.set(f"{secs:02d}")

    def __countdown(self):
        if self.timer_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.__update_display()
            self._after_id = self.timer_window.after(1000, self.__countdown)
        else:
            if self.remaining_seconds <= 0:
                self.timer_running = False
                messagebox.showinfo("Done!", "Time's up!")
                self.__end_timer("sad_idle")

    def __pause_timer(self):
        self.timer_running = False
        if self._after_id is not None:
            self.timer_window.after_cancel(self._after_id)
            self._after_id = None
        self.__set_state("sad_idle")

    def __end_timer(self, state):
        self.__set_state(state)
        self.remaining_seconds = 0
        self.timer_running = False
        self.__update_display()
        if self.timer_window:
            self.timer_window.withdraw()

    # ---------------------- MENU ----------------------
    def on_right_click(self, event):
        menu = tk.Menu(self.window, tearoff=0)
        if self.state in ("pomodoro", "sad_pomodoro"):
            menu.add_command(label="Pause Pomodoro", command=self.__pause_timer)
            menu.add_command(label="End Pomodoro", command=lambda: self.__end_timer("sad_idle"))
        elif self.state == "sad_idle":
            if self.remaining_seconds == 0:
                menu.add_command(label="Start Pomodoro", command=lambda: self.__start_timer("sad_pomodoro"))
            else:
                menu.add_command(label="Resume Pomodoro", command=lambda: self.__start_timer("sad_pomodoro", fresh=False))
        else:
            menu.add_command(label="Start Pomodoro", command=lambda: self.__start_timer("pomodoro"))
        menu.add_separator()
        menu.add_command(label="Close", command=self.window.quit)
        menu.post(event.x_root, event.y_root)

    # NEW: Public method for menu (starts timer + setup)
    def start_pomodoro(self):
        if not hasattr(self, 'hour_entry'):  # Lazy init UI
            self._setup_timer_ui()
        self.__start_timer("pomodoro")
