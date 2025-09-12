import tkinter as tk
from tkinter import ttk


class NumberInput(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.var = tk.IntVar(value=0)  # Default value

        # Create spinbox
        self.spinbox = ttk.Spinbox(
            self, from_=-1000, to=1000, textvariable=self.var, wrap=True)
        self.spinbox.grid(row=0, column=1, padx=(0, 5), pady=5)

    def increment(self):
        self.var.set(self.var.get() + 1)

    def decrement(self):
        self.var.set(self.var.get() - 1)


# Create main window
root = tk.Tk()
root.title("Number Input Field with Arrows")

# Create NumberInput widget
number_input = NumberInput(root)
number_input.pack(pady=20)

# Run the application
root.mainloop()
