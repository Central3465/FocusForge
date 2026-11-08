import tkinter as tk
from tkinter import messagebox
import json
import os

class focusforge:
    def __init__(a, b):
        a.b = b
        a.b.title("FocusForge")
        a.b.geometry("450x500")
        a.b.resizable(False, False)
        a.focustime = 25 * 60
        a.breaktime = 5 * 60
        a.remainingtime = a.focustime
        a.running = False
        a.isfocus = True
        a.timerid = None
        a.totalsecs = 0
        a.completedsessions = 0
        a.create_widgets()
        a.update_display()
        a.datafile = "data.json"
        a.load_data()

    def create_widgets(a):
        a.heading = tk.Label(a.b, text="FocusForge", font=("Helvetica", 24)) # remember b is window and a is app
        a.heading.pack(pady=20)

        a.sessionlabel = tk.Label(a.b, text="Focus Time", font=("Arial", 16))
        a.sessionlabel.pack(pady=5)

        a.timerlabel = tk.Label(a.b, text="25:00", font=("Arial", 64, "bold"))
        a.timerlabel.pack(pady=20)

        a.startbtn = tk.Button(a.b, text="Start", font=("Arial", 12), width=12, command=a.starttimer)
        a.startbtn.pack(pady=5)

        a.pausebtn = tk.Button(a.b, text="Pause", font=("Arial", 12), width=12, command=a.pausetimer)
        a.pausebtn.pack(pady=5)

        a.resetbtn = tk.Button(a.b, text="Reset", font=("Arial", 12), width=12, command=a.resettimer)
        a.resetbtn.pack(pady=5)

        a.sessioncountlabel = tk.Label(a.b, text="Completed session: 0", font=("Arial", 12))
        a.sessioncountlabel.pack(pady=(20, 5))

        a.waterlabel = tk.Label(a.b, text="Water: 0 / 1", font=("Arial", 14, "bold"))
        a.waterlabel.pack(pady=5)

        a.progresslabel = tk.Label(a.b, text="Focus time: 0 / 60 minutes", font=("Arial", 11))
        a.progresslabel.pack(pady=5)

    def starttimer(a):
        if not a.running:
            a.running = True
            a.countdown()

    def pausetimer(a):
        a.running = False

        if a.timerid:
            a.b.after_cancel(a.timerid)
            a.timerid = None

    def resettimer(a):
        a.pausetimer()

        if a.isfocus:
            a.remainingtime = a.focustime
        else:
            a.remainingtime = a.breaktime

        a.update_display()

    def countdown(a):
        if not a.running:
            return

        if a.remainingtime > 0:
            a.remainingtime -= 1

            if a.isfocus:
                a.totalsecs +=1
                a.savedata()
                a.update_progress()

            a.update_display()

            a.timerid = a.b.after(1000, a.countdown)
        else:
            a.finish()

    def finish(a):
        a.running = False
        a.timerid = None

        if a.isfocus:
            a.completedsessions += 1
            a.savedata()

            messagebox.showinfo("Focus complete!", "Great work! Time for a break!")

            a.isfocus = False
            a.remainingtime = a.breaktime
        else:
            messagebox.showinfo("Break complete!", "Ready to focus again?")

            a.isfocus = True
            a.remainingtime = a.focustime

        a.update_display()

    def update_display(a):
        mins = a.remainingtime // 60
        secs = a.remainingtime % 60

        a.timerlabel.config(text=f"{mins:02d}:{secs:02d}")

        a.sessionlabel.config(text="Focus time" if a.isfocus else "short break")

        a.sessioncountlabel.config(text=f"Completed sessions: {a.completedsessions}")

        a.update_progress()

    def update_progress(a):
        waters = a.totalsecs // 3600

        progress = a.totalsecs % 3600
        mins = progress // 60

        a.waterlabel.config(text=f"Water: {waters}")

        a.progresslabel.config(text=f"Focus time: {mins} / 60 minutes")

    def loaddata(a):
        if os.path.exists(a.datafile):
            try:
                with open(a.datafile, "r") as file:
                    data = json.load(file)

                a.totalsecs = max(0, int(data.get("total_focus_secons", 0)))
                a.completedsessions = max(0, int(data.get("completed_sessions", 0)))
            except (json.JSONDecodeError, ValueError, TypeError, OSError):
                print("error loading data")
        else:
            with open(a.datafile, "w") as file:
                test = { "total_focus_seconds": 0, "completed_sessions": 0}
                json.dump(test)

    def savedata(a):
        data = { "total_focus_seconds": a.totalsecs, "completed_sessions": a.completedsessions}

        with open(a.progressfile, "w") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = focusforge(root)

    # make closing the window not destroy data
    root.protocol("WM_DELETE_WINDOW", lambda: (
        app.pausetimer(),
        app.savedata(), # forgot the commas, need them here
        root.destroy()
    ))

    root.mainloop()