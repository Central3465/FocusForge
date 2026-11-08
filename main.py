import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
from datetime import date, timedelta

class focusforge:
    def __init__(a, b):
        a.b = b
        a.b.title("FocusForge")
        a.b.geometry("450x600")
        a.b.resizable(False, False)
        a.focustime = 25 * 60
        a.breaktime = 5 * 60
        a.remainingtime = a.focustime
        a.running = False
        a.isfocus = True
        a.timerid = None
        a.totalsecs = 0
        a.completedsessions = 0
        a.datafile = "data.json"
        a.dailyfocus = 0
        a.lastwatered = None # thanks hackclub terra for giving me inspiration
        a.today = date.today().isoformat()
        a.loaddata()
        a.create_widgets()
        a.update_display()

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

        a.progressbar = ttk.Progressbar(a.b, length=300, maximum=3600, mode="determinate")
        a.progressbar.pack(pady=10)

        a.farmlabel = tk.Label(a.b, text="your farm", font=("Arial", 20, "bold"))
        a.farmlabel.pack(pady=15)

        a.croplabel = tk.Label(a.b, text="your crop needs water!", font=("Arial", 14))
        a.croplabel.pack(pady=5)

        a.waterbtn = tk.Button(a.b, text="Water Farm", font=("Arial", 12), width=15, command=a.waterfarm)
        a.waterfarm.pack(pady=10)

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

        a.checkday()

        if a.remainingtime > 0:
            a.remainingtime -= 1

            if a.isfocus:
                a.totalsecs +=1
                a.dailyfocus += 1
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

        a.progressbar["value"] = a.totalsecs % 3600

    def loaddata(a):
        if os.path.exists(a.datafile):
            try:
                with open(a.datafile, "r") as file:
                    data = json.load(file)

                a.totalsecs = max(0, int(data.get("total_focus_seconds", 0)))
                a.completedsessions = max(0, int(data.get("completed_sessions", 0)))
            except (json.JSONDecodeError, ValueError, TypeError, OSError):
                print("error loading data")
        else:
            with open(a.datafile, "w") as file:
                test = { "total_focus_seconds": 0, "completed_sessions": 0}
                json.dump(test, file, indent=4)

    def savedata(a):
        data = { "total_focus_seconds": a.totalsecs, "completed_sessions": a.completedsessions}

        with open(a.datafile, "w") as f:
            json.dump(data, f, indent=4)

    def checkday(a):
        currentday = date.today().isoformat()

        if currentday != a.today:
            a.today = currentday
            a.dailyfocus = 0
            a.savedata()

    def waterfarm(a):
        if a.dailyfocus < 3600:
            messagebox.showinfo("not ready!", "you need 60 minutes of focus time to water your crops")
            return

        if a.lastwatered == a.today:
            messagebox.showinfo("already watered!", "you've already watered your crops today, take a break!")
            return

        a.lastwatered = a.today
        a.savedata()
        a.updatefarm()

        messagebox.showinfo("Farm watered!", "your crops are now watered, great work!")

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