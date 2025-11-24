import os
import tkinter as tk
from tkinter import Entry, StringVar, messagebox

class RaccoonWindow:

    def __init__(self, window, x=1400, y=700, dimension=128):

        self.impath = os.path.join(os.path.dirname(__file__), 'image', '') #image directory
        self.raccoon_knitting = [tk.PhotoImage(file=self.impath + 'raccoon_knitting.gif', format='gif -index %i' % i)
                                 for i in range(2)]
        self.raccoon_idle = [tk.PhotoImage(file=self.impath + 'raccoon_idle.gif', format='gif -index %i' % i) for i in
                             range(2)]
        self.raccoon_sad_idle = [tk.PhotoImage(file=self.impath + 'raccoon_sad.gif', format='gif -index %i' % i) for i
                                 in range(3)]
        self.raccoon_sad_knitting = [
            tk.PhotoImage(file=self.impath + 'raccoon_sad_knitting.gif', format='gif -index %i' % i) for i in range(2)]

        self.x = x
        self.y = y
        self.dimension = dimension
        self.window = window
        self.state = "idle"
        self.gif = self.raccoon_idle
        self.frame = 0

        # Timer Additional from Geeks
        self.hour = StringVar(value="00")
        self.minute = StringVar(value="00")
        self.second = StringVar(value="00")
        self.remaining_seconds = 0
        self.timer_running = False
        self.timer_window = None
        self._after_id = None  # track scheduled countdown job

        # window and pet_label configuration and binding
        self.window.geometry(f"{dimension}x{dimension}+{x}+{y}")
        self.window.overrideredirect(True)
        self.window.wm_attributes('-transparentcolor', 'red')
        self.window.wm_attributes('-topmost', True)  # Make it top of everything

        self.pet_label = tk.Label(self.window, bd=0, bg='red')
        self.pet_label.pack()
        self.pet_label.bind('<Button-3>', self.on_right_click)  # Right click

        self.__play_gif()

    # making gif loop through frames
    def __play_gif(self):
        self.pet_label.configure(image=self.gif[self.frame])
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
        if self.state == "pomodoro":
            self.gif = self.raccoon_knitting
        elif state == "idle":
            self.gif = self.raccoon_idle
        elif state == "sad_idle":
            self.gif = self.raccoon_sad_idle
        elif state == "sad_pomodoro":
            self.gif = self.raccoon_sad_knitting

    def _setup_timer_ui(self):
        if hasattr(self, 'hour_entry'):  # ← Already built? Do nothing!
            return

        if self.timer_window is None:
            self.timer_window = tk.Toplevel(self.window)

        win = self.timer_window
        win.geometry("360x200")
        win.title("Pomodoro Timer")
        win.configure(bg="#2c3e50")
        win.resizable(False, False)

        # Create and SAVE the widgets so we don't make duplicates
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

        # Buttons
        tk.Button(win, text="Pause", width=8, command=self.__pause_timer).place(x=50, y=120)
        tk.Button(win, text="Resume", width=8,
                  command=lambda: self.__start_timer("pomodoro", fresh=False)).place(x=130, y=120)
        tk.Button(win, text="End", width=8, command=lambda: self.__end_timer("idle")).place(x=210, y=120)


    # use on user selection
    def __start_timer(self, state, fresh=True):
        self.__set_state(state)
        # TODO set starting time based on time attribute (whether from resuming or from starting)
        # lazy-init UI the first time
        if not hasattr(self, 'hour_entry'):
            self._setup_timer_ui()

        self.timer_window.deiconify()
        self.timer_window.lift()

        # ---- set initial time ----
        if fresh and state in ("pomodoro", "sad_pomodoro"):
            self.remaining_seconds = 25 * 60
        self.__update_display()
        self.timer_running = True
        self.__countdown()

    ##
    def __update_display(self):
        # Convert seconds to HH:MM:SS (GFG logic with divmod)
        mins, secs = divmod(self.remaining_seconds, 60)
        hours, mins = divmod(mins, 60)
        self.hour.set(f"{hours:02d}")
        self.minute.set(f"{mins:02d}")
        self.second.set(f"{secs:02d}")

    ##
    def __countdown(self):
        if self.timer_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.__update_display()
            self._after_id = self.timer_window.after(1000, self.__countdown) #changed

        else:
            self.timer_running = False
            messagebox.showinfo("Done!", "Time's up!")
            self.__end_timer("sad_idle")

    # use on user selection
    def __pause_timer(self):
        self.__set_state("paused")
        self.timer_running = False
        if self._after_id is not None:
            self.timer_window.after_cancel(self._after_id)
            self._after_id = None
        self.__set_state("sad_idle")

    # used on user selection and for natural timer ending
    def __end_timer(self, state):
        self.__set_state(state)
        self.remaining_seconds = 0
        self.timer_running = False  # Hide window
        self.__update_display()
        self.timer_window.withdraw()


    def on_right_click(self, event):
        # Create popup menu
        menu = tk.Menu(self.window, tearoff=0)
        if self.state == "pomodoro" or self.state == "sad_pomodoro":
            menu.add_command(label="Pause Pomodoro", command=self.__pause_timer)
            menu.add_command(label="End Pomodoro", command=lambda: self.__end_timer("idle"))
        elif self.state == "sad_idle":  # sad idle
            menu.add_command(label="Start Pomodoro", command=lambda: self.__set_state("sad_pomodoro"))
        else: # idle
            menu.add_command(label="Start Pomodoro", command=self.start_pomodoro)

        menu.add_separator()
        menu.add_command(label="Close", command=self.window.quit)
        menu.post(event.x_root, event.y_root)


    # NEW: Public method for menu (starts timer + setup)
    def start_pomodoro(self):
        if not hasattr(self, 'hour_entry'):  # Lazy init UI
            self._setup_timer_ui()
        self.__start_timer("pomodoro")
