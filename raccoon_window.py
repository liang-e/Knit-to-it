
import tkinter as tk
import os

impath = os.path.join(os.path.dirname(__file__), 'image', '') #image directory
x = 1400
y = 700
gif_dimension = 128
pet_window = tk.Tk()
state = "sad_pomodoro"
gif = None

# call buddy's action gif
raccoon_knitting = [tk.PhotoImage(file=impath + 'raccoon_knitting.gif', format='gif -index %i' % (i)) for i in range(2)]
raccoon_idle = [tk.PhotoImage(file=impath + 'raccoon_idle.gif', format='gif -index %i' % (i)) for i in range(2)]
raccoon_sad_idle = [tk.PhotoImage(file=impath + 'raccoon_sad.gif', format='gif -index %i' % (i)) for i in range (3)]
raccoon_sad_knitting = [tk.PhotoImage(file=impath + 'raccoon_sad_knitting.gif', format='gif -index %i' % (i)) for i in range (2)]

# making gif loop through frames
frame = 0
def play_gif(frames):
    global frame
    pet_label.configure(image=frames[frame])
    frame = (frame + 1) % len(frames)
    delay = 1000
    if state == "sad_pomodoro":
        delay = 1800
    elif state == "sad_idle":
        delay = 500
    pet_window.after(delay, play_gif, frames)

def on_right_click(event):
    print("RIGHT CLICK detected")  # test line

    # Create popup menu
    menu = tk.Menu(pet_window, tearoff=0)
    # menu.add_command(label="Sleep", command=lambda: change_state(1, 5))
    if state == "pomodoro" or state == "sad_pomodoro":
        menu.add_command(label="Pause Pomodoro", command=pet_window.quit)
        menu.add_command(label="End Pomodoro", command=pet_window.quit)
    else: #for idle and sad idle
        menu.add_command(label="Start Pomodoro", command=pet_window.quit)
    menu.add_separator()
    menu.add_command(label="Close", command=pet_window.quit)
    menu.post(event.x_root, event.y_root)

#window and label configuration and binding
pet_window.geometry(str(gif_dimension)+ 'x' +str(gif_dimension) + '+' + str(x) + '+' + str(y))  # dimensions and positioning of pet
pet_window.overrideredirect(True)
pet_window.wm_attributes('-transparentcolor', 'red')
pet_window.wm_attributes('-topmost', True)  # Make it top of everything

pet_label = tk.Label(pet_window, bd=0, bg='black')
pet_label.bind('<Button-3>', on_right_click)  # Right click
pet_label.pack()

# play gifs
if state == "pomodoro":
    gif = raccoon_knitting
elif state == "idle":
    gif = raccoon_idle
elif state == "sad_idle":
    gif = raccoon_sad_idle
elif state == "sad_pomodoro":
    gif = raccoon_sad_knitting
play_gif(gif)
pet_window.mainloop()

