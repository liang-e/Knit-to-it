import tkinter as tk
import os

impath = os.path.join(os.path.dirname(__file__), 'image', '')  # image directory
x = 1400
y = 700
gif_dimension = 128
pet_window = tk.Tk()

door_closed_path = impath + 'door_closed.png'
door_open_path = impath + 'door_open.png'

door_images = {}
door_label = None



class InventoryWindow:
    # window to display the raccoon's knitted stuff
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("knitted item inventory")
        self.top.resizable(False, False)
        self.top.grab_set()  # makes the window modal

        # placeholder
        tk.Label(self.top, text="[this window will show the raccoon's knitted rewards.]",
                 font=("arial", 12)).pack(padx=30, pady=30)

        tk.Button(self.top, text="close", command=self.close).pack(pady=10)

        # center the window
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x_pos = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y_pos = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'+{x_pos}+{y_pos}')

    def close(self):
        self.top.grab_release()
        self.top.destroy()


# --- image loading ---

def load_door_images():
    # loads door icons
    try:
        closed_img = tk.PhotoImage(file=door_closed_path)
        open_img = tk.PhotoImage(file=door_open_path)

        # door icon is appropriately small next to the pet
        door_images['CLOSED'] = closed_img.subsample(4, 4)
        door_images['OPEN'] = open_img.subsample(4, 4)

    except tk.TclError:
        print("warning: door icon images not found. using simple placeholder images.")
        door_images['CLOSED'] = tk.PhotoImage(width=40, height=40)
        door_images['OPEN'] = tk.PhotoImage(width=40, height=40)


load_door_images()


def on_door_enter(event):
    # changes the door icon to open on mouse hover and sets cursor
    if 'OPEN' in door_images:
        door_label.config(image=door_images['OPEN'])
        door_label.config(cursor="hand2")  # set cursor to show it's clickable


def on_door_leave(event):
    # changes the door icon to closed when mouse leaves and resets cursor
    if 'CLOSED' in door_images:
        door_label.config(image=door_images['CLOSED'])
        door_label.config(cursor="")  # reset cursor


def on_door_click(event):
    # opens the inventory window
    InventoryWindow(pet_window)


# setup window properties
door_width = door_images['CLOSED'].width() if 'CLOSED' in door_images else 40

window_width = door_width + 100
window_height = door_width + 50
pet_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

pet_window.overrideredirect(True)
pet_window.wm_attributes('-transparentcolor', 'white')
pet_window.wm_attributes('-topmost', True)
pet_window.config(bg='white')

# main interaction frame (holds the door)
interaction_frame = tk.Frame(pet_window, bg='white')
interaction_frame.pack(side="top", padx=10, pady=10)

# door icon label
door_label = tk.Label(interaction_frame, bd=0, bg='white', image=door_images.get('CLOSED'))
door_label.pack(side="left")  # placed in the frame

# bind door events
door_label.bind('<enter>', on_door_enter)
door_label.bind('<leave>', on_door_leave)
door_label.bind('<button1>', on_door_click)  # bind click to open inventorywindow


pet_window.mainloop()