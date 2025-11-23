
import tkinter as tk
import os

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

        # window and pet_label configuration and binding
        self.window.geometry(str(self.dimension) + 'x' + str(self.dimension) + '+' + str(self.x) + '+' + str(self.y))  # dimensions and positioning of pet
        self.window.overrideredirect(True)
        self.window.wm_attributes('-transparentcolor', 'red')
        self.window.wm_attributes('-topmost', True)  # Make it top of everything

        self.pet_label = tk.Label(self.window, bd=0, bg='black')
        self.pet_label.bind('<Button-3>', self.on_right_click)  # Right click
        self.pet_label.pack()

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

    # use on user selection
    def __start_timer(self, state):
        self.__set_state(state)
        # TODO set starting time based on time attribute (whether from resuming or from starting)
        # TODO call running timer

    # use on user selection
    def __pause_timer(self, state):
        self.__set_state(state)
        # TODO set time attribute to current time
        # TODO call display time

    # used on user selection and for natural timer ending
    def __end_timer(self, state):
        self.__set_state(state)
        # TODO reset time attribute to default time
        # TODO call display time

    # decrements the timer while it is running
    def __running_timer(self):
        # TODO decrements and displays timer separately from time attribute
        # TODO call display time after each decrement

    def __display_time(self, time):
        # TODO displays the time while running, before timer is starated, while timer is resumed

    # TODO replace set_state method calls with timer calls
    def on_right_click(self, event):
        # Create popup menu
        menu = tk.Menu(self.window, tearoff=0)
        if self.state == "pomodoro" or self.state == "sad_pomodoro":
            menu.add_command(label="Pause Pomodoro", command=lambda: self.__set_state("sad_idle"))
            menu.add_command(label="End Pomodoro", command=lambda: self.__set_state("sad_idle"))
        elif self.state == "sad_idle":  # sad idle
            menu.add_command(label="Start Pomodoro", command=lambda: self.__set_state("sad_pomodoro"))
        else: # idle
            menu.add_command(label="Start Pomodoro", command=lambda: self.__set_state("pomodoro"))
        menu.add_separator()
        menu.add_command(label="Close", command=self.window.quit)
        menu.post(event.x_root, event.y_root)



