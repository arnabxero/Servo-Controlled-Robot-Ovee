import tkinter as tk
from tkinter import StringVar, OptionMenu


def on_selection_change(*args):
    selected_value = variable.get()
    print(f"Selected value: {selected_value}")


# Create the main window
root = tk.Tk()
root.title("Dropdown Menu Example")

# Define the variable to hold the selected value
variable = StringVar(root)
variable.set("Option 1")  # Set default value

# Create a list of options
options = ["Option 1", "Option 2", "Option 3", "Option 4"]

# Create the dropdown menu
dropdown = OptionMenu(root, variable, *options)
dropdown.pack(pady=20)

# Trace the variable to detect changes using trace_add
variable.trace_add("write", on_selection_change)

# Run the application
root.mainloop()
