
import tkinter as tk
from raccoon_window import RaccoonWindow

if __name__ == "__main__":
    # Raccoon window (main root)
    pet_window = tk.Tk()

    # Timer window (hidden at start, child of root)
    timer_window = tk.Toplevel(pet_window)
    timer_window.withdraw()  # Critical!

    # Create raccoon and link timer
    raccoon = RaccoonWindow(pet_window)
    raccoon.timer_window = timer_window  # ← Now it's a proper child window

    # Start
    pet_window.mainloop()
