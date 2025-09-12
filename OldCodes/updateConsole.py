import tkinter as tk
import g


def updateConsole(value):
    try:
        g.consoleBox.insert(tk.END, value + "\n")
        g.consoleBox.see(tk.END)
    except Exception as e:
        print(f"Minor Warning-Unable to update console: {str(e)}")
