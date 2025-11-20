## import pyautogui ## not needed but, it's library has useful function for future applications
# main.py - Launches the Desktop Pet + Pomodoro Timer


import tkinter as tk
from tkinter import messagebox
import random
import os
import threading
import sys

from timer import PomodoroApp

# ================================
# 1. DESKTOP PET - Clean, no shadows, no nonlocal errors
# ================================

impath = os.path.join(os.path.dirname(__file__), 'image')

# Global state
window = label = None
idle = idle_to_sleep = sleep = sleep_to_idle = walk_positive = walk_negative = []

x_pos = 1400          # renamed from x
anim_cycle = 0        # renamed from cycle
check = 1
idle_num = [1, 2, 3, 4]
sleep_num = [10, 11, 12, 13, 15]
walk_left = [6, 7]
walk_right = [8, 9]
event_number = random.randrange(1, 3, 1)

def run_desktop_pet():
    global window, label, idle, idle_to_sleep, sleep, sleep_to_idle, walk_positive, walk_negative
    global x_pos, anim_cycle, check, event_number

    window = tk.Tk()
    window.config(highlightbackground='black')
    label = tk.Label(window, bd=0, bg='black')
    window.overrideredirect(True)
    window.wm_attributes('-transparentcolor', 'black')  # fixed typo
    window.wm_attributes('-topmost', True)

    try:
        idle            = [tk.PhotoImage(file=os.path.join(impath, 'idle.gif'),            format=f'gif -index {i}') for i in range(5)]
        idle_to_sleep   = [tk.PhotoImage(file=os.path.join(impath, 'idle_to_sleep.gif'),   format=f'gif -index {i}') for i in range(8)]
        sleep           = [tk.PhotoImage(file=os.path.join(impath, 'sleep.gif'),           format=f'gif -index {i}') for i in range(3)]
        sleep_to_idle   = [tk.PhotoImage(file=os.path.join(impath, 'sleep_to_idle.gif'),   format=f'gif -index {i}') for i in range(8)]
        walk_positive   = [tk.PhotoImage(file=os.path.join(impath, 'walking_positive.gif'),format=f'gif -index {i}') for i in range(8)]
        walk_negative   = [tk.PhotoImage(file=os.path.join(impath, 'walking_negative.gif'),format=f'gif -index {i}') for i in range(8)]
    except Exception as exc:
        messagebox.showerror("Missing GIFs", f"Put your GIFs in:\n{impath}\n\nError: {exc}")
        sys.exit()

    def schedule_next(frame_cycle: int, pos_x: int):
        window.after(400, update_frame, frame_cycle, pos_x)

    def update_frame(frame_cycle: int, pos_x: int):
        global check, event_number, anim_cycle, x_pos

        # Choose animation and advance frame
        if check == 0:   # idle
            frame = idle[frame_cycle]
            next_cycle = (frame_cycle + 1) % len(idle)
            if next_cycle == 0:
                event_number = random.randrange(1, 10)
        elif check == 1:  # idle → sleep
            frame = idle_to_sleep[frame_cycle]
            next_cycle = (frame_cycle + 1) % len(idle_to_sleep)
            if next_cycle == 0:
                event_number = 10
        elif check == 2:  # sleeping
            frame = sleep[frame_cycle]
            next_cycle = (frame_cycle + 1) % len(sleep)
            if next_cycle == 0:
                event_number = random.randrange(10, 16)
        elif check == 3:  # sleep → idle
            frame = sleep_to_idle[frame_cycle]
            next_cycle = (frame_cycle + 1) % len(sleep_to_idle)
            if next_cycle == 0:
                event_number = 1
        elif check == 4:  # walk left
            frame = walk_positive[frame_cycle]
            next_cycle = (frame_cycle + 1) % len(walk_positive)
            if next_cycle == 0:
                event_number = random.randrange(1, 10)
            pos_x -= 6
        elif check == 5:  # walk right
            frame = walk_negative[frame_cycle]
            next_cycle = (frame_cycle + 1) % len(walk_negative)
            if next_cycle == 0:
                event_number = random.randrange(1, 10)
            pos_x += 6
        else:
            frame = idle[0]
            next_cycle = 0

        # Update global state
        anim_cycle = next_cycle
        x_pos = pos_x

        window.geometry(f'100x100+{pos_x}+900')
        label.configure(image=frame)

        # Schedule next update
        window.after(120, schedule_next, next_cycle, pos_x)

    def on_left_click(_event):  # renamed parameter to avoid shadow
        global check, event_number, anim_cycle
        if check in [0, 4, 5]:
            check, event_number, anim_cycle = 1, 5, 0
        elif check == 2:
            check, event_number, anim_cycle = 3, 14, 0

    def on_right_click(event):  # parameter name is fine here
        menu = tk.Menu(window, tearoff=0)
        menu.add_command(label="Sleep",      command=lambda: set_state(1, 5))
        menu.add_command(label="Wake Up",    command=lambda: set_state(3, 14))
        menu.add_command(label="Walk Left",  command=lambda: set_state(4, 6))
        menu.add_command(label="Walk Right", command=lambda: set_state(5, 8))
        menu.add_separator()
        menu.add_command(label="Close Buddy", command=window.destroy)
        menu.post(event.x_root, event.y_root)

    def set_state(new_check: int, new_event: int):
        global check, event_number, anim_cycle
        check, event_number, anim_cycle = new_check, new_event, 0

    label.bind('<Button-1>', on_left_click)
    label.bind('<Button-3>', on_right_click)
    label.pack()

    # Start animation loop
    window.after(120, update_frame, anim_cycle, x_pos)
    window.mainloop()


# ================================
# 3. LAUNCH THE FULL APP
# ================================

if __name__ == "__main__":
    pet_thread = threading.Thread(target=run_desktop_pet, daemon=True)
    pet_thread.start()

    root = tk.Tk()
    root.title("Knit-to-it Study Buddy 🧶")
    root.geometry("700x800")
    root.configure(bg="#f8f9fa")
    root.resizable(False, False)

    app = PomodoroApp(root)
    root.mainloop()