import os
import tkinter as tk
from tkinter import Entry, StringVar, messagebox
from PIL import Image, ImageTk

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
        self._after_id = None  # track scheduled countdown job
        self.manual_end = False # if timer ends prematurely
        self.completed_poms = 0
        self.successful_pom = 4 # 4
        self.pom_length = 1 # 25
        self.rest_timer = 0
        self.rest_length = 0 # 5
        self.long_rest_length = 30 # 30
        self.rest_length_penalty = 1 # 5
        self.penalty_timer = 0
        self.is_rest = False
        self.time_til_happy = 0


        # window setup
        self.window.geometry(f"{dimension}x{dimension}+{x}+{y}")
        self.window.overrideredirect(True)
        self.window.wm_attributes('-transparentcolor', 'red')
        self.window.wm_attributes('-topmost', True)  # Make it top of everything

        # Pet label
        self.pet_label = tk.Label(self.window, bd=0, bg='red')
        self.pet_label.pack()
        self.pet_label.bind('<Button-3>', self.on_right_click)  # Right click
        self.pet_label.bind('<Button-1>', self.start_drag)
        self.pet_label.bind('<B1-Motion>', self.on_drag)

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

    # ---------------------- TIMER UI ----------------------
    def _setup_timer_ui(self):
        if hasattr(self, 'hour_entry'):  # ← Already built? Do nothing!
            return

        if self.timer_window is None:
            self.timer_window = tk.Toplevel(self.window)

        win = self.timer_window
        win.geometry("360x200")
        win.title("Pomodoro Timer")
        win.resizable(False, False)

        # --- Background image ---
        raw_bg = Image.open(os.path.join(self.impath, 'background.png'))
        #raw_bg.show()
        resized_bg = raw_bg.resize((360, 200), Image.Resampling.LANCZOS)
        self.timer_bg = ImageTk.PhotoImage(resized_bg)

        # --- Cartoon timer image ---
        pil_timer = Image.open(os.path.join(self.impath, "cartoonTimerEditpng.png"))
        orig_w, orig_h = pil_timer.size
        scale_factor = min(200 / orig_h, 360 / orig_w)
        new_w, new_h = int(orig_w * scale_factor), int(orig_h * scale_factor)
        pil_timer = pil_timer.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self.timer_image = ImageTk.PhotoImage(pil_timer)

        # --- Canvas ---
        self.canvas = tk.Canvas(win, width=360, height=200, highlightthickness=0)
        self.canvas.pack()

        # Draw background first
        self.canvas.create_image(0, 0, anchor="nw", image=self.timer_bg)

        # Draw cartoon timer centered
        self.timer_x, self.timer_y = 180, 100
        self.canvas.create_image(self.timer_x, self.timer_y, image=self.timer_image)

        # Overlay countdown text (slightly above center of timer image)
        self.timer_text_item = self.canvas.create_text(
            self.timer_x, self.timer_y - 30,
            text="25:00",
            font=("DS-Digital", 20),
            fill="white",
            anchor="center"
        )


    # use on user selection
    def __start_timer(self, state, fresh=True):
        print("Start timer")
        self.__set_state(state)

        # lazy-init UI the first time
        if not hasattr(self, 'hour_entry'):
            self._setup_timer_ui()

        self.timer_window.deiconify()
        self.timer_window.lift()

        # ---- set initial time ----
        if fresh and state in ("pomodoro", "sad_pomodoro"):
            self.remaining_seconds = self.pom_length * 60
        self.is_rest = False
        self.__update_display(self.remaining_seconds)
        self.timer_running = True
        self.__countdown(self.remaining_seconds)

    def __rest_countdown(self, state, length):
        print("Start rest " + str(length))
        self.remaining_seconds = 0
        self.is_rest = True
        self.rest_timer = length * 60
        self.__set_state(state)
        self.__update_display(self.rest_timer)
        self.timer_running = True
        self.__countdown(self.rest_timer)

    ##
    def __update_display(self, timer_length):
        # Convert seconds to HH:MM:SS (GFG logic with divmod)
        mins, secs = divmod(timer_length, 60)
        hours, mins = divmod(mins, 60)
        time_str = f"{hours:02d}:{mins:02d}:{secs:02d}"
        if hasattr(self, 'canvas'):
            self.canvas.itemconfig(self.timer_text_item, text=time_str)

    ##
    def __countdown(self, timer_length):
        if self.timer_running and timer_length > 0:
            if self.time_til_happy > 0 and not self.is_rest:
                self.time_til_happy -= 1
            if not self.is_rest:
                self.remaining_seconds -= 1
            timer_length -= 1
            self.__update_display(timer_length)
            self._after_id = self.timer_window.after(1000, self.__countdown, timer_length) #changed

        else:
            self.timer_running = False
            if not self.manual_end and not self.is_rest: #if pom timer ended naturally

                if self.time_til_happy <= 0:
                    self.completed_poms += 1
                    print(str(self.completed_poms))

                if self.completed_poms == self.successful_pom:
                    self.__rest_countdown("idle", self.long_rest_length)
                    # TODO add sweater thing here
                elif self.state != "sad_pomodoro" or self.time_til_happy <= 0:
                    self.__rest_countdown("idle", self.rest_length)
                else:
                    self.__rest_countdown("sad_idle", self.rest_length)
            elif self.is_rest: # if the resting timer ended
                print("rest over")
                self.is_rest = False
                self.penalty_timer = self.rest_length_penalty * 60
                if self.completed_poms == self.successful_pom:
                    self.completed_poms = 0
                self.__check_rest_length()
            elif self.manual_end:
                self.__set_state("sad_idle")
                self.manual_end = False

            #messagebox.showinfo("Done!", "Time's up!")
            #self.__end_timer("sad_idle")

    def __check_rest_length(self):
        if self.penalty_timer > 0 and self.timer_running == False:
            self.penalty_timer -= 1
            self._after_id = self.timer_window.after(1000, self.__check_rest_length)
        elif self.penalty_timer == 0 and self.timer_running == False:
            self.__set_state("sad_idle")
            self.completed_poms = 0
            self.time_til_happy = self.pom_length * 60
            self.remaining_seconds = 0
            print("You Took Too Long To Start The Next Pomodoro. Pomo lost motivation on his project.")

    # use on user selection
    def __pause_timer(self):
        print("Pause")
        self.__set_state("paused")
        self.timer_running = False
        self.time_til_happy = self.pom_length * 60
        if self._after_id is not None:
            self.timer_window.after_cancel(self._after_id)
            self._after_id = None
        self.__set_state("sad_idle")

    # used on user selection and for natural timer ending
    def __end_timer(self, state):
        print("End timer")
        self.time_til_happy = self.pom_length * 60
        self.__set_state(state)
        self.remaining_seconds = 0
        self.timer_running = False  # Hide window
        self.__update_display(self.remaining_seconds)
        self.timer_window.withdraw()
        self.manual_end = True

    # ---------------------- MENU ----------------------
    def on_right_click(self, event):
        # Create popup menu
        menu = tk.Menu(self.window, tearoff=0)
        if self.state == "pomodoro" or self.state == "sad_pomodoro":
            menu.add_command(label="Pause Pomodoro", command=self.__pause_timer)
            menu.add_command(label="End Pomodoro", command=lambda: self.__end_timer("sad_idle"))
        elif self.state == "sad_idle":
            if self.remaining_seconds == 0:
                menu.add_command(label="Start Pomodoro", command=lambda: self.__start_timer("sad_pomodoro"))
            elif self.remaining_seconds > 0:
                menu.add_command(label="Resume Pomodoro", command=lambda: self.__start_timer("sad_pomodoro", fresh=False))
                menu.add_command(label="End Pomodoro", command=lambda: self.__end_timer("sad_idle"))
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
