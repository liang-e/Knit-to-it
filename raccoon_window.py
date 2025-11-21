# pet.py
import tkinter as tk
import os



def launch_pet(state="sad_pomodoro", x=1400, y=700, master=None):
    impath = os.path.join(os.path.dirname(__file__), 'image', '')
    gif_dimension = 128
    pet_window = tk.Toplevel(master) if master else tk.Tk()

    gif = None

    raccoon_knitting = [tk.PhotoImage(file=impath + 'raccoon_knitting.gif', format='gif -index %i' % i) for i in range(2)]
    raccoon_idle = [tk.PhotoImage(file=impath + 'raccoon_idle.gif', format='gif -index %i' % i) for i in range(2)]
    raccoon_sad_idle = [tk.PhotoImage(file=impath + 'raccoon_sad.gif', format='gif -index %i' % i) for i in range(3)]
    raccoon_sad_knitting = [tk.PhotoImage(file=impath + 'raccoon_sad_knitting.gif', format='gif -index %i' % i) for i in range(2)]

    if state == "pomodoro":
        gif = raccoon_knitting
    elif state == "idle":
        gif = raccoon_idle
    elif state == "sad_idle":
        gif = raccoon_sad_idle
    elif state == "sad_pomodoro":
        gif = raccoon_sad_knitting

    frame = 0
    def play_gif(frames):
        nonlocal frame
        pet_label.configure(image=frames[frame])
        frame = (frame + 1) % len(frames)
        delay = 1800 if state == "sad_pomodoro" else 500 if state == "sad_idle" else 1000
        pet_window.after(delay, play_gif, frames)

    def on_right_click(event):
        menu = tk.Menu(pet_window, tearoff=0)
        if state in ["pomodoro", "sad_pomodoro"]:
            menu.add_command(label="Pause Pomodoro", command=pet_window.quit)
            menu.add_command(label="End Pomodoro", command=pet_window.quit)
        else:
            menu.add_command(label="Start Pomodoro", command=pet_window.quit)
        menu.add_separator()
        menu.add_command(label="Close", command=pet_window.quit)
        menu.post(event.x_root, event.y_root)

    pet_window.geometry(f"{gif_dimension}x{gif_dimension}+{x}+{y}")
    pet_window.overrideredirect(True)
    pet_window.wm_attributes('-transparentcolor', 'red')
    pet_window.wm_attributes('-topmost', True)

    pet_label = tk.Label(pet_window, bd=0, bg='black')
    pet_label.bind('<Button-3>', on_right_click)
    pet_label.pack()

    play_gif(gif)
    pet_window.mainloop()