## import pyautogui ## not needed but it's library has useful function for future applications
import random
import tkinter as tk

x = 1400
cycle = 0
check = 1
idle_num = [1, 2, 3, 4]
sleep_num = [10, 11, 12, 13, 15]
walk_left = [6, 7]
walk_right = [8, 9]
event_number = random.randrange(1, 3, 1)
import os
impath = os.path.join(os.path.dirname(__file__), 'image', '') #home directory
def event(cycle, x):
    global check, event_number

    if event_number in idle_num:
        check = 0
        print('idle')
        window.after(400, update, cycle, x)

    elif event_number == 5:
        check = 1
        print('from idle to sleep')
        window.after(100, update, cycle, x)

    elif event_number in walk_left:
        check = 4
        print('walking towards left')
        window.after(100, update, cycle, x)

    elif event_number in walk_right:
        check = 5
        print('walking towards right')
        window.after(100, update, cycle, x)

    elif event_number in sleep_num:
        check = 2
        print('sleep')
        window.after(1000, update, cycle, x)

    elif event_number == 14:
        check = 3
        print('from sleep to idle')
        window.after(100, update, cycle, x)

# Click handler functions
def on_left_click(event):
    global check, event_number, cycle
    print("LEFT CLICK detected")  # test line

    # Toggle between idle and sleep
    if check in [0, 4, 5]:  # If idle or walking
        print("Switching from idle/walking to idle->sleep state")  # test line
        check = 1
        event_number = 5
        cycle = 0
    elif check == 2:  # If sleeping
        print("Switching from sleep to sleep->idle state")  # test line
        check = 3
        event_number = 14
        cycle = 0

def on_right_click(event):
    print("RIGHT CLICK detected")  # test line

    # Create popup menu
    menu = tk.Menu(window, tearoff=0)
    menu.add_command(label="Sleep", command=lambda: change_state(1, 5))
    menu.add_command(label="Wake Up", command=lambda: change_state(0, 1))
    menu.add_command(label="Walk Left", command=lambda: change_state(4, 6))
    menu.add_command(label="Walk Right", command=lambda: change_state(5, 8))
    menu.add_separator()
    menu.add_command(label="Close", command=window.quit)
    menu.post(event.x_root, event.y_root)

def change_state(new_check, new_event):
    global check, event_number, cycle
    check = new_check
    event_number = new_event
    cycle = 0

# making gif work
def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle += 1
    else:
        cycle = 0
        event_number = random.randrange(first_num, last_num + 1, 1)
    return cycle, event_number


def update(cycle, x):
    global check, event_number

    if check == 0:
        frame = idle[cycle]
        cycle, event_number = gif_work(cycle, idle, event_number, 1, 9)

    elif check == 1:
        frame = idle_to_sleep[cycle]
        cycle, event_number = gif_work(cycle, idle_to_sleep, event_number, 10, 10)
    # sleep
    elif check == 2:
        frame = sleep[cycle]
        cycle, event_number = gif_work(cycle, sleep, event_number, 10, 15)
    # sleep to idle
    elif check == 3:
        frame = sleep_to_idle[cycle]
        cycle, event_number = gif_work(cycle, sleep_to_idle, event_number, 1, 1)
    # walk toward left
    elif check == 4:
        frame = walk_positive[cycle]
        cycle, event_number = gif_work(cycle, walk_positive, event_number, 1, 9)
        x -= 3
    # walk towards right
    elif check == 5:
        frame = walk_negative[cycle]
        cycle, event_number = gif_work(cycle, walk_negative, event_number, 1, 9)
        x -= -3
    window.geometry('100x100+' + str(x) + '+500') #imagine border
    label.configure(image=frame)
    window.after(1, event, cycle, x)


window = tk.Tk()
# call buddy's action gif
idle = [tk.PhotoImage(file=impath + 'raccoon_idle.gif', format='gif -index %i' % (i)) for i in range(5)]  # idle gif
idle_to_sleep = [tk.PhotoImage(file=impath + 'idle_to_sleep.gif', format='gif -index %i' % (i)) for i in
                 range(8)]  # idle to sleep gif
sleep = [tk.PhotoImage(file=impath + 'sleep.gif', format='gif -index %i' % (i)) for i in range(3)]  # sleep gif
sleep_to_idle = [tk.PhotoImage(file=impath + 'sleep_to_idle.gif', format='gif -index %i' % (i)) for i in
                 range(8)]  # sleep to idle gif
walk_positive = [tk.PhotoImage(file=impath + 'walking_positive.gif', format='gif -index %i' % (i)) for i in
                 range(8)]  # walk to left gif
walk_negative = [tk.PhotoImage(file=impath + 'walking_negative.gif', format='gif -index %i' % (i)) for i in
                 range(8)]  # walk to right gif
# window configuration
window.config(highlightbackground='black')
label = tk.Label(window, bd=0, bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor', 'black')
window.wm_attributes('-topmost', True) #Make it top of everything

# Bind click event to the label
label.bind('<Button-1>', on_left_click)  # Left click
label.bind('<Button-3>', on_right_click)  # Right click
label.pack()
window.after(1, update, cycle, x)
window.mainloop()