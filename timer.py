# timer.py - Knit-to-it Pomodoro Timer 🍅🧶

import tkinter as tk
from tkinter import Frame, Button, Label, messagebox


class PomodoroApp(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master or tk.Tk()
        self.pack(fill="both", expand=True)

        self.timer_label = None

        self.focus_time = 25 * 60
        self.break_time = 5 * 60
        self.time_left = self.focus_time
        self.running = False
        self.is_break = False
        self.completed_pomodoros = 0   # ← Changed as requested

        self.show_menu()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def add_label(self, text, font, pady=10, fg="#2d3436", bg=None):
        Label(self.master, text=text, font=font, bg=bg or self.master["bg"], fg=fg).pack(pady=pady)

    def add_button(self, parent, text, command, bg, fg="white", padx=15):
        Button(parent, text=text, bg=bg, fg=fg, font=("Arial", 14), command=command).pack(side="left", padx=padx)

    def show_menu(self):
        self.clear_window() # Changed this to reduce repeated screens lines 35-40 changed -a
        self.master.configure(bg="#f8f9fa")
        self.add_label("🧶 Knit-to-it Pomodoro Buddy 🧶", ("Helvetica", 26, "bold"), pady=60)
        self.add_label("25 minutes focus • 5 minutes break", ("Arial", 16), fg="#636e72")
        self.add_label("Your desktop buddy is walking while you work!", ("Arial", 14))

        Button(self.master, text="Start Pomodoro Session", font=("Arial", 20, "bold"),
               bg="#00b894", fg="white", width=25, height=3, command=self.start_session).pack(pady=40)

        self.add_label(f"Completed: {self.completed_pomodoros} 🍅", ("Arial", 18, "bold"), fg="#e17055", pady=20)

        Label(self.master, text="25 minutes focus • 5 minutes break",
              font=("Arial", 16), bg="#f8f9fa", fg="#636e72").pack(pady=10)

        Label(self.master, text="Your desktop buddy is walking while you work!",
              font=("Arial", 14), bg="#f8f9fa").pack(pady=20)

        Button(self.master, text="Start Pomodoro Session",
               font=("Arial", 20, "bold"), bg="#00b894", fg="white",
               width=25, height=3, command=self.start_session).pack(pady=40)

        Label(self.master, text=f"Completed: {self.completed_pomodoros} 🍅",
              font=("Arial", 18, "bold"), bg="#f8f9fa", fg="#e17055").pack(pady=20)

    def start_session(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        bg_color = "#d5f5e3" if not self.is_break else "#a29bfe"
        self.master.configure(bg=bg_color)

        mode_text = "FOCUS TIME! 📚🧶" if not self.is_break else "BREAK TIME ☕"
        Label(self.master, text=mode_text,
              font=("Helvetica", 32, "bold"), bg=bg_color, fg="#2d3436").pack(pady=50)

        self.timer_label = Label(self.master, text="25:00",
                                 font=("Helvetica", 80, "bold"), bg=bg_color, fg="#2d3436")
        self.timer_label.pack(expand=True, pady=40)

        msg = "Keep knitting and studying!" if not self.is_break else "Stretch & relax!"
        Label(self.master, text=msg,
              font=("Arial", 16), bg=bg_color, fg="#636e72").pack(pady=20)

        #Refactoring the buttons -a
        btn_frame = Frame(self.master, bg=bg_color)
        btn_frame.pack(pady=30)
        self.add_button(btn_frame, "Pause", self.pause, "#fdcb6e", fg="black")
        self.add_button(btn_frame, "Skip →", self.skip, "#ff7675")
        self.add_button(btn_frame, "Menu", self.show_menu, "#b2bec3")

        self.time_left = self.break_time if self.is_break else self.focus_time
        self.running = True
        self.countdown()

    def countdown(self):
        if self.running and self.time_left > 0:
            mins = self.time_left // 60
            secs = self.time_left % 60
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            self.time_left -= 1
            self.master.after(1000, self.countdown)  # type: ignore[arg-type]
        else:
            self.finish_phase()

    def finish_phase(self):
        self.running = False
        if not self.is_break:
            self.completed_pomodoros += 1   # ← Updated
            messagebox.showinfo("Pomodoro Complete! 🎉",
                                f"You finished Pomodoro #{self.completed_pomodoros}!\nTime for a break 🧶")
        else:
            messagebox.showinfo("Break Over!", "Back to work! Your buddy is ready 💪")

        self.is_break = not self.is_break
        self.start_session()

    def pause(self):
        self.running = False
        messagebox.showinfo("Paused", "Timer paused. Click 'Start Pomodoro Session' to resume.")

    def skip(self):
        self.time_left = 0
        self.finish_phase()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Knit-to-it Pomodoro")
    root.geometry("700x800")
    root.resizable(False, False)
    app = PomodoroApp(root)
    root.mainloop()

# Added a launch_timer function to launch the timer -a
def launch_timer():
    root = tk.Tk()
    root.title("Knit-to-it Pomodoro")
    root.geometry("700x800")
    root.resizable(False, False)
    PomodoroApp(root)
    root.mainloop()