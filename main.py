import tkinter as tk
from tkinter import messagebox

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

    def create_widgets(a):
        a.heading = tk.Label(a.b, text="FocusForge", font=("Helvetica", 24)) # remember b is window and a is app
        a.heading.pack(pady=20)

        a.sessionlabel = tk.Label(a.b, text="Focus Time", font=("Arial", 16))
        a.sessionlabel.pack(pady=5)

        a.timerlabel = tk.Label(a.b, text="25:00", font=("Arial", 64, "bold"))
        a.timerlabel.pack(pady=20)

        a.startbtn = tk.Button(a.b, text="Start", font=("Arial", 12), width=12, command=a.start)
        a.startbtn.pack(pady=5)

        a.pausebtn = tk.Button(a.b, text="Pause", font=("Arial", 12), width=12, command=a.pause)
        a.pausebtn.pack(pady=5)

        a.resetbtn = tk.Button(a.b, text="REset", font=("Arial", 12), width=12, command=a.reset)
        a.resetbtn.pack(pady=5)

        a.sessioncountlabel = tk.Label(a.b, text="Completed session: 0", font=("Arial", 12))
        a.sessioncountlabel.pack(pady=(20, 5))

        a.waterlabel = tk.Label(a.b, text="Water: 0 / 1", font=("Arial", 14, "bold"))
        a.waterlabel.pack(pady=5)

        a.progresslabel = tk.Label(a.b, text="Focus time: 0 / 60 minutes", font=("Arial", 11))
        a.progresslabel.pack(pady=5)