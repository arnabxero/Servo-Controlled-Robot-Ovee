from tkinter import *
from pathlib import Path

# Custom imports
# from tkinter import *
# Explicit imports to satisfy Flake8
import matplotlib.pyplot as plt
from pathlib import Path
import random
from PIL import Image, ImageTk
import os
import pyfirmata
import re
import tkinter as tk
from tkinter import END, StringVar, ttk
import threading
import time
import csv
import datetime
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import matplotlib.animation as animation
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
# from utils import onChange
from tkinter import *
from pathlib import Path
from utils import create_entry_value, entry_callback

code_path = os.path.abspath(__file__)
assets_relative_path = os.path.join(
    os.path.dirname(code_path), "assets/frame0")
ASSETS_PATH = Path(assets_relative_path)
OUTPUT_PATH = Path(__file__).parent


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.geometry("400x400")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=400,
    width=400,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    307.5,
    578.5,
    image=entry_image_1
)

# Create and set up entries using utils functions
entry_value_1 = create_entry_value('entry_1', entry_callback)
entry_1 = Entry(
    bd=0,
    bg="#FEE0D3",
    fg="#000716",
    highlightthickness=0,
    textvariable=entry_value_1
)
entry_1.place(
    x=50,
    y=50,
    width=100,
    height=30
)

entry_value_2 = create_entry_value('entry_2', entry_callback)
entry_2 = Entry(
    bd=0,
    bg="#FEE0D3",
    fg="#000716",
    highlightthickness=0,
    textvariable=entry_value_2
)
entry_2.place(
    x=50,
    y=90,
    width=100,
    height=30
)

entry_value_3 = create_entry_value('entry_3', entry_callback)
entry_3 = Entry(
    bd=0,
    bg="#FEE0D3",
    fg="#000716",
    highlightthickness=0,
    textvariable=entry_value_3
)
entry_3.place(
    x=50,
    y=130,
    width=100,
    height=30
)

window.mainloop()
