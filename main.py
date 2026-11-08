import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
from datetime import date, timedelta
import webbrowser

class focusforge:
    def __init__(a, b):
        a.b = b
        a.b.title("FocusForge")
        a.b.geometry("700x700")
        a.b.minsize(500, 500)
        a.b.resizable(True, True)
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
        a.waterstreak = 0
        a.today = date.today().isoformat()
        a.loaddata()
        a.checkday()
        a.canvas = tk.Canvas(a.b, highlightthickness=0)
        a.scrollbar = ttk.Scrollbar(a.b, orient="vertical", command=a.canvas.yview)
        a.scrollframe = tk.Frame(a.canvas)
        a.window_id = a.canvas.create_window(0, 0, window=a.scrollframe, anchor="nw")
        a.scrollframe.bind("<Configure>", a.updatescroll)
        a.canvas.bind("<Configure>", a.updatescroll)
        a.canvas.configure(yscrollcommand=a.scrollbar.set)
        a.scrollbar.pack(side="right", fill="y")
        a.canvas.pack(side="left", fill="both", expand=True)
        a.b.bind_all("<MouseWheel>", a.onmousewheel)
        a.create_widgets()
        a.update_display()

    def updatescroll(a, event=None):
        # make the content fill the window: at least as wide and as tall as the canvas
        cw = a.canvas.winfo_width()
        ch = a.canvas.winfo_height()
        needed = a.scrollframe.winfo_reqheight()
        a.canvas.itemconfigure(a.window_id, width=cw, height=max(needed, ch))
        a.canvas.configure(scrollregion=(0, 0, cw, max(needed, ch)))

        # only show the scrollbar when content is taller than the window
        if needed > ch:
            if not a.scrollbar.winfo_ismapped():
                a.scrollbar.pack(side="right", fill="y", before=a.canvas)
        else:
            a.scrollbar.pack_forget()
            a.canvas.yview_moveto(0)

    def onmousewheel(a, event):
        if a.scrollframe.winfo_reqheight() > a.canvas.winfo_height():
            a.canvas.yview_scroll(int(-event.delta / 120), "units")

    def create_widgets(a):
        a.heading = tk.Label(a.scrollframe, text="FocusForge", font=("Helvetica", 24)) # remember b is window and a is app
        a.heading.pack(pady=20, fill="x", padx=40)

        a.sessionlabel = tk.Label(a.scrollframe, text="Focus Time", font=("Arial", 16))
        a.sessionlabel.pack(pady=5, fill="x", padx=40)

        a.timerlabel = tk.Label(a.scrollframe, text="25:00", font=("Arial", 64, "bold"))
        a.timerlabel.pack(pady=20, fill="x", padx=40)

        a.startbtn = tk.Button(a.scrollframe, text="Start", font=("Arial", 12), command=a.starttimer)
        a.startbtn.pack(pady=5, fill="x", padx=40)

        a.pausebtn = tk.Button(a.scrollframe, text="Pause", font=("Arial", 12), command=a.pausetimer)
        a.pausebtn.pack(pady=5, fill="x", padx=40)

        a.resetbtn = tk.Button(a.scrollframe, text="Reset", font=("Arial", 12), command=a.resettimer)
        a.resetbtn.pack(pady=5, fill="x", padx=40)

        a.sessioncountlabel = tk.Label(a.scrollframe, text="Completed session: 0", font=("Arial", 12))
        a.sessioncountlabel.pack(pady=(20, 5), fill="x", padx=40)

        a.croplabel = tk.Label(a.scrollframe, text="Seedling -- Your crops need water!", font=("Arial", 12))
        a.croplabel.pack(pady=5)

        a.waterlabel = tk.Label(a.scrollframe, text="Water: 0 / 1", font=("Arial", 14, "bold"))
        a.waterlabel.pack(pady=5, fill="x", padx=40)

        a.progresslabel = tk.Label(a.scrollframe, text="Focus time: 0 / 60 minutes", font=("Arial", 11))
        a.progresslabel.pack(pady=5, fill="x", padx=40)

        a.progressbar = ttk.Progressbar(a.scrollframe, maximum=3600, mode="determinate")
        a.progressbar.pack(pady=10, fill="x", padx=40)

        a.farmlabel = tk.Label(a.scrollframe, text="Your Farm", font=("Arial", 20, "bold"))
        a.farmlabel.pack(pady=15)

        a.farmframe = tk.Frame(a.scrollframe, padx=15, pady=15)
        a.farmframe.pack(pady=10)

        a.plots = []
        for i in range(4):
            plot = tk.Frame(a.farmframe, width=140, height=110, bg="brown", borderwidth=3)

            plot.grid(row=i//2, column=i%2, padx=10, pady=10)
            plot.pack_propagate(False)
            crop = tk.Label(plot, text="🌻", font=("Arial", 30))
            crop.bind("<Button-1>", lambda e, index=i: a.plotclick(index))
            crop.pack(expand=True)

            a.plots.append(crop)

        a.streaklabel = tk.Label(a.scrollframe, text="Watering streak: 0 days", font=("Arial", 12))
        a.streaklabel.pack(pady=5)

        a.waterbtn = tk.Button(a.scrollframe, text="Water your farm", font=("Arial", 12), command=a.waterfarm)
        a.waterbtn.pack(pady=10)

        a.musiclabel = tk.Label(a.scrollframe, text="Focus Music", font=("Arial", 20, "bold"))
        a.musiclabel.pack(pady=15, fill="x", padx=40)

        a.musicstatus = tk.Label(a.scrollframe, text="Ready to focus?", font=("Arial", 11))
        a.musicstatus.pack(pady=5, fill="x", padx=40)

        a.spotifybtn = tk.Button(a.scrollframe, text="Open Spotify", font=("Arial", 12), command=a.openspotify)
        a.spotifybtn.pack(pady=10, fill="x", padx=40)

    # make plots interactive
    def plotclick(a, index):
        messagebox.showinfo("Plot", f"You clicked on plot {index+1}!")

    def updateplots(a):
        if a.waterstreak >= 7:
            icon = "🌳"
        elif a.waterstreak >= 3:
            icon = "🌱"
        else:
            icon = "🌻"

        for plot in a.plots:
            plot.config(text=icon)

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
        a.updateplots()
        a.updatefarm()

    def update_progress(a):
        waters = a.totalsecs // 3600

        progress = a.totalsecs % 3600
        mins = progress // 60

        a.waterlabel.config(text=f"Water: {waters}")

        a.progresslabel.config(text=f"Focus time: {mins} / 60 minutes")

        a.progressbar["value"] = a.totalsecs % 3600

    def updatefarm(a):
        yesterday = (date.today() - timedelta(days=1)).isoformat()

        if a.lastwatered == a.today:
            status = "Your crops are already watered today!"
            a.waterbtn.config(state="disabled")
        elif a.lastwatered is not None and a.lastwatered < yesterday:
            status = "Oh no, your crops are withered! You missed a day of watering."
            a.waterbtn.config(state="normal")
        else:
            status = "Your crops need water!"
            a.waterbtn.config(state="normal")

        if a.waterstreak >= 7:
            crop = "Mature crop"
        elif a.waterstreak >= 3:
            crop = "Growing crop"
        else:
            crop = "Seedling"

        a.croplabel.config(text=f"{crop} -- {status}")
        a.streaklabel.config(text=f"Watering streak: {a.waterstreak} days")
        a.updateplots()

    def loaddata(a):
        if os.path.exists(a.datafile):
            try:
                with open(a.datafile, "r") as file:
                    data = json.load(file)

                a.totalsecs = max(0, int(data.get("total_focus_seconds", 0)))
                a.completedsessions = max(0, int(data.get("completed_sessions", 0)))
                a.dailyfocus = max(0, int(data.get("daily_focus_seconds", 0)))
                a.lastwatered = data.get("last_watered")
                a.today = data.get("today", date.today().isoformat())
                a.waterstreak = max(0, int(data.get("streak", 0)))
            except (json.JSONDecodeError, ValueError, TypeError, OSError):
                print("error loading data")
        else:
            with open(a.datafile, "w") as file:
                test = { "total_focus_seconds": 0, "completed_sessions": 0}
                json.dump(test, file, indent=4)

    def savedata(a):
        data = { 
            "total_focus_seconds": a.totalsecs, 
            "completed_sessions": a.completedsessions, 
            "daily_focus_seconds": a.dailyfocus, 
            "last_watered": a.lastwatered, 
            "today": a.today,
            "streak": a.waterstreak
        }

        with open(a.datafile, "w") as f:
            json.dump(data, f, indent=4)

    def checkday(a):
        currentday = date.today().isoformat()

        if currentday != a.today:
            yesterday = (date.today() - timedelta(days=1)).isoformat()

            if a.lastwatered != yesterday: # missing a day now resets streak
                a.waterstreak = 0

            a.today = currentday
            a.dailyfocus = 0
            a.savedata()

    def waterfarm(a):
        if a.dailyfocus < 3600:
            messagebox.showwarning("Not ready!", "You need 1 hour of focus time to water your crops!")
            return

        if a.lastwatered == a.today:
            messagebox.showwarning("Already watered!", "You've already watered your crops today, take a break!")
            return

        a.lastwatered = a.today
        a.waterstreak += 1
        a.savedata()
        a.updatefarm()
        crop = "Seedling"
        if a.waterstreak >= 7:
            crop = "Mature crop"
        elif a.waterstreak >= 3:
            crop = "Growing crop"
        else:
            crop = "Seedling"

        messagebox.showinfo("Farm watered!", "your crops are now watered, great work!")
        a.croplabel.config(text=f"{crop} -- watered!")

    def openspotify(a):
        url = "https://open.spotify.com/playlist/671ZWIQMPSY2IO6Ot7b57V"

        success = webbrowser.open(url)

        if success:
            a.musicstatus.config(text="Opening Spotify...")
        else:
            a.musicstatus.config(text="Failed to open spotify.")

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