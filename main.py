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
    