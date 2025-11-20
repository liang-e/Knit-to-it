
import tkinter as tk
import os

impath = os.path.join(os.path.dirname(__file__), 'image', '') #image directory
x = 1400

pet_window = tk.Tk()

# call buddy's action gif
walk_positive = [tk.PhotoImage(file=impath + 'walking_positive.gif', format='gif -index %i' % (i)) for i in
                 range(8)]  # walk to left gif
raccoon_knitting = [tk.PhotoImage(file=impath + 'raccoon_knitting.gif', format='gif -index %i' % (i)) for i in range(2)]
frame = 0
# making gif work
def play_gif(frames):
    global frame
    pet_label.configure(image=frames[frame])
    frame = (frame + 1) % len(frames)
    pet_window.after(1000, play_gif, frames)


def on_right_click(event):
    print("RIGHT CLICK detected")  # test line

    # Create popup menu
    menu = tk.Menu(pet_window, tearoff=0)
    #menu.add_command(label="Sleep", command=lambda: change_state(1, 5))
    menu.add_separator()
    menu.add_command(label="Close", command=pet_window.quit)
    menu.post(event.x_root, event.y_root)


# Bind click event to the label

pet_window.geometry('128x128+' + str(x) + '+7 00')  # imagine border
# window configuration
#pet_window.config(highlightbackground='black')
pet_window.overrideredirect(True)
pet_window.wm_attributes('-transparentcolor', 'red')
pet_window.wm_attributes('-topmost', True)  # Make it top of everything

pet_label = tk.Label(pet_window, bd=0, bg='black')
pet_label.bind('<Button-3>', on_right_click)  # Right click
pet_label.pack()
play_gif(raccoon_knitting)
pet_window.mainloop()

