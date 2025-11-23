
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

        # window and label configuration and binding
        self.window.geometry(str(self.dimension) + 'x' + str(self.dimension) + '+' + str(self.x) + '+' + str(self.y))  # dimensions and positioning of pet
        self.window.overrideredirect(True)
        self.window.wm_attributes('-transparentcolor', 'red')
        self.window.wm_attributes('-topmost', True)  # Make it top of everything

        self.label = tk.Label(pet_window, bd=0, bg='black')
        self.label.bind('<Button-3>', self.on_right_click)  # Right click
        self.label.pack()

        self.__play_gif(self.state)

    # making gif loop through frames
    def __play_gif(self, state):
        print(state)
        self.label.configure(image=self.gif[self.frame])
        self.frame = (self.frame + 1) % len(self.gif)
        delay = 1000
        if self.state == "sad_pomodoro":
            delay = 1800
        elif self.state == "sad_idle":
            delay = 500
        pet_window.after(delay, self.__play_gif, self.state)

    def __set_state(self, state):
        self.state = state
        if self.state == "pomodoro":
            self.gif = self.raccoon_knitting
        elif state == "idle":
            self.gif = self.raccoon_idle
        elif state == "sad_idle":
            self.gif = self.raccoon_sad_idle
        elif state == "sad_pomodoro":
            self.gif = self.raccoon_sad_knitting

    def on_right_click(self, event):
        # Create popup menu
        menu = tk.Menu(pet_window, tearoff=0)
        # menu.add_command(label="Sleep", command=lambda: change_state(1, 5))
        if self.state == "pomodoro" or self.state == "sad_pomodoro":
            menu.add_command(label="Pause Pomodoro", command=lambda: self.__set_state("sad_idle"))
            menu.add_command(label="End Pomodoro", command=lambda: self.__set_state("sad_idle"))
        elif self.state == "sad_idle":  # sad idle
            menu.add_command(label="Start Pomodoro", command=lambda: self.__set_state("sad_pomodoro"))
            print("sad_idle")
        else: # idle
            menu.add_command(label="Start Pomodoro", command=lambda: self.__set_state("pomodoro"))
            print("idle")
        menu.add_separator()
        menu.add_command(label="Close", command=pet_window.quit)
        menu.post(event.x_root, event.y_root)


pet_window = tk.Tk()
raccoon = RaccoonWindow(pet_window)
pet_window.mainloop()

