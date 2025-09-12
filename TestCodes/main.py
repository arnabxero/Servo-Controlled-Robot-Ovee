import tkinter as tk
from tkinter import StringVar, OptionMenu
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / \
    Path(r"/Users/arnabxero/Downloads/untitled folder 15/build/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# Create the main window
window = tk.Tk()
window.title("Dropdown Menu Example")
window.geometry("200x200")
window.configure(bg="#FFFFFF")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=1005.0,
    y=691.0,
    width=136.0,
    height=46.0
)

# Run the application
window.mainloop()
