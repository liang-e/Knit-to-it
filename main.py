## import pyautogui ## not needed but it's library has useful function for future applications
import random
import tkinter as tk
import time
import raccoon_window

import tkinter as tk
from raccoon_window import launch_pet
from timer import PomodoroApp

def main():
    root = tk.Tk()
    #root.withdraw()  # Optional: hide root if you only want the pet and timer windows
    launch_pet(state="sad_pomodoro", x=1400, y=700, master=root)
    PomodoroApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()







