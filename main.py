# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import ttk
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

# Custom Imports
import g
from boardSetup import boardSetup
from utils import create_entry_value, entry_callback, handleGripperButton, resetGripper, autoSetSensorIdle, clearExportVariables, exportData, close_action, handleServoButton, setServoSpeed, resetServos
from runSensor import runSensorLoop
from runGripper import runGripperLoop
from runServo import runServoLoop
from graphs import create_graphs


current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%d-%m-%Y | %I_%M_%S %p")
code_path = os.path.abspath(__file__)
assets_relative_path = os.path.join(
    os.path.dirname(code_path), "assets/frame0")
ASSETS_PATH = Path(assets_relative_path)
OUTPUT_PATH = Path(__file__).parent


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


boardSetup()

window = Tk()

# window.geometry("1200x750")
window.geometry("200x200")
# time.sleep(7)
# window.geometry("1200x750")

window.configure(bg="#FFFFFF")


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=750,
    width=1200,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
button_image_exit = PhotoImage(
    file=relative_to_assets("button_exit.png"))
button_exit = Button(
    image=button_image_exit,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: close_action(),
    relief="flat"
)
button_exit.place(
    x=982.0,
    y=690.0,
    width=71.0,
    height=46.0
)

button_image_reset = PhotoImage(
    file=relative_to_assets("button_reset.png"))
button_reset = Button(
    image=button_image_reset,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: resetServos(),  # Reset servos instead of just printing
    relief="flat"
)
button_reset.place(
    x=1093.0,
    y=690.0,
    width=71.0,
    height=46.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
gripper_pause_button = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)

gripper_pause_button.bind(
    "<Button-1>", lambda event: handleGripperButton(g.gripper_direction, False))

gripper_pause_button.place(
    x=469.0,
    y=535.0,
    width=136.0,
    height=46.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
sensor_idle_autoset_button = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)

sensor_idle_autoset_button.bind(
    "<Button-1>", lambda event: autoSetSensorIdle(sensor_idle_value_entry))

sensor_idle_autoset_button.place(
    x=762.0,
    y=422.0,
    width=136.0,
    height=30.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
gripper_reset_button = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)

gripper_reset_button.bind(
    "<Button-1>", lambda event: resetGripper())

gripper_reset_button.place(
    x=394.0,
    y=611.0,
    width=98.0,
    height=46.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=92.0,
    y=692.0,
    width=142.0,
    height=46.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
clear_export_button = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)

# clear_export_button.bind(
#     "<Button-1>", lambda event: clearExportVariables())

clear_export_button.bind(
    "<Button-1>", lambda event: [clearExportVariables(), graphs.clear_data()])

clear_export_button.place(
    x=385.0,
    y=692.0,
    width=142.0,
    height=46.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: exportData(g.export_timestamp, g.export_diameter, g.export_deformation,
                               g.export_delta_pressure, g.export_sensor_value, g.export_closing_time),
    relief="flat"
)
button_7.place(
    x=546.0,
    y=692.0,
    width=142.0,
    height=46.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
export_data_button = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat"
)

export_data_button.place(
    x=582.0,
    y=611.0,
    width=98.0,
    height=46.0
)

canvas.create_rectangle(
    13.0,
    371.0,
    28.0,
    386.0,
    fill="#4B5DFF",
    outline="")

canvas.create_rectangle(
    13.0,
    421.0,
    28.0,
    436.0,
    fill="#38BC6D",
    outline="")

canvas.create_rectangle(
    13.0,
    471.0,
    28.0,
    486.0,
    fill="#FAB603",
    outline="")

canvas.create_rectangle(
    13.0,
    521.0,
    28.0,
    536.0,
    fill="#FF5656",
    outline="")

canvas.create_rectangle(
    13.0,
    571.0,
    28.0,
    586.0,
    fill="#E57FFF",
    outline="")

canvas.create_rectangle(
    13.0,
    627.0,
    28.0,
    642.0,
    fill="#73CE00",
    outline="")

canvas.create_rectangle(
    432.0,
    499.0,
    447.0,
    514.0,
    fill="#CE003D",
    outline="")

canvas.create_rectangle(
    92.0,
    611.0,
    345.0,
    657.0,
    fill="#FFE3B9",
    outline="")

canvas.create_rectangle(
    92.0,
    611.0,
    345.0,
    657.0,
    fill="#FEE0D3",
    outline="")

canvas.create_rectangle(
    741.0,
    700.0,
    909.0,
    731.0,
    fill="#FEE0D3",
    outline="")

canvas.create_rectangle(
    946.0,
    57.0,
    1200.0,
    677.0,
    fill="#DCFFD0",
    outline="")

canvas.create_rectangle(
    713.0,
    57.0,
    946.0,
    316.0,
    fill="#FFFAD0",
    outline="")

canvas.create_text(
    485.0,
    1.0,
    anchor="nw",
    text="ROBOT CONTROL PANEL",
    fill="#727272",
    font=("Inter SemiBold", 24 * -1)
)

canvas.create_text(
    32.0,
    369.0,
    anchor="nw",
    text="Servo 1",
    fill="#3B3D6F",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    32.0,
    519.0,
    anchor="nw",
    text="Servo 4",
    fill="#3B3D70",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    32.0,
    469.0,
    anchor="nw",
    text="Servo 3",
    fill="#3B3D70",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    32.0,
    419.0,
    anchor="nw",
    text="Servo 2",
    fill="#3B3D70",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    32.0,
    569.0,
    anchor="nw",
    text="Servo 5",
    fill="#3B3D70",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    35.0,
    617.0,
    anchor="nw",
    text="Overall\nSpeed",
    fill="#3B3D70",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    453.0,
    498.0,
    anchor="nw",
    text="Close",
    fill="#3B3D70",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_rectangle(
    582.0,
    499.0,
    597.0,
    514.0,
    fill="#03ADAD",
    outline="")

canvas.create_text(
    603.0,
    498.0,
    anchor="nw",
    text="Open",
    fill="#3B3D70",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    114.0,
    322.0,
    anchor="nw",
    text="ROBOT CONTROL",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    11.0,
    696.0,
    anchor="nw",
    text="DATA\nEXPORT",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    762.0,
    588.0,
    anchor="nw",
    text="NIFELAB",
    fill="#6F6F6F",
    font=("Inter SemiBold", 30 * -1)
)

canvas.create_text(
    249.0,
    689.0,
    anchor="nw",
    text="Recording Status",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    782.0,
    678.0,
    anchor="nw",
    text="PORT SELECT",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    453.0,
    322.0,
    anchor="nw",
    text="GRASPER CONTROL",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    752.0,
    322.0,
    anchor="nw",
    text="SENSOR PARAMETERS",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    752.0,
    35.0,
    anchor="nw",
    text="LAST COMMAND LOG",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    453.0,
    35.0,
    anchor="nw",
    text="LIVE VALUES MONITOR",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    149.0,
    35.0,
    anchor="nw",
    text="GRAPH",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    1039.0,
    35.0,
    anchor="nw",
    text="CONSOLE",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    284.0,
    322.0,
    anchor="nw",
    text="SPEED",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_text(
    395.0,
    361.0,
    anchor="nw",
    text="Aftertouch Runtime",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    307.5,
    578.5,
    image=entry_image_1
)
servo_speed_5_entry = Entry(
    bd=0,
    bg="#FEE0D3",
    fg="#000716",
    highlightthickness=0
)
servo_speed_5_entry.place(
    x=270.0,
    y=561.0,
    width=75.0,
    height=33.0
)


g.servo_speed_entries[4] = servo_speed_5_entry

servo_speed_5_entry.insert(0, g.servo_speed[4])

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    307.5,
    528.5,
    image=entry_image_2
)
servo_speed_4_entry = Entry(
    bd=0,
    bg="#FEE0D3",
    fg="#000716",
    highlightthickness=0
)
servo_speed_4_entry.place(
    x=270.0,
    y=511.0,
    width=75.0,
    height=33.0
)


entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    307.5,
    478.5,
    image=entry_image_3
)
servo_speed_3_entry = Entry(
    bd=0,
    bg="#FEE0D3",
    fg="#000716",
    highlightthickness=0
)
servo_speed_3_entry.place(
    x=270.0,
    y=461.0,
    width=75.0,
    height=33.0
)


entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    307.5,
    428.5,
    image=entry_image_4
)
servo_speed_2_entry = Entry(
    bd=0,
    bg="#FEE0D3",
    fg="#000716",
    highlightthickness=0
)
servo_speed_2_entry.place(
    x=270.0,
    y=411.0,
    width=75.0,
    height=33.0
)


entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    307.5,
    378.5,
    image=entry_image_5
)
servo_speed_1_entry = Entry(
    bd=0,
    bg="#FEDFD2",
    fg="#000716",
    highlightthickness=0
)
servo_speed_1_entry.place(
    x=270.0,
    y=361.0,
    width=75.0,
    height=33.0
)


entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    462.0,
    397.5,
    image=entry_image_6
)

aftertouch_runtime_value = create_entry_value(
    'aftertouch_runtime', entry_callback)

aftertouch_runtime_entry = Entry(
    bd=0,
    bg="#FEDFD2",
    fg="#000716",
    highlightthickness=0,
    textvariable=aftertouch_runtime_value
)
aftertouch_runtime_entry.place(
    x=394.0,
    y=380.0,
    width=136.0,
    height=33.0
)
aftertouch_runtime_entry.insert(0, g.aftertouch_runtime)


canvas.create_text(
    395.0,
    80.0,
    anchor="nw",
    text="Diameter (mm)",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

entry_image_7 = PhotoImage(
    file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(
    446.0,
    116.5,
    image=entry_image_7
)
g.diameter_mm_entry = Entry(
    bd=0,
    bg="#D2FBFE",
    fg="#000716",
    highlightthickness=0
)
g.diameter_mm_entry.place(
    x=378.0,
    y=99.0,
    width=136.0,
    height=33.0
)


canvas.create_text(
    384.0,
    156.0,
    anchor="nw",
    text="Deformation (mm)",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

entry_image_8 = PhotoImage(
    file=relative_to_assets("entry_8.png"))
entry_bg_8 = canvas.create_image(
    446.0,
    192.5,
    image=entry_image_8
)
g.deformation_mm_entry = Entry(
    bd=0,
    bg="#D2FBFE",
    fg="#000716",
    highlightthickness=0
)
g.deformation_mm_entry.place(
    x=378.0,
    y=175.0,
    width=136.0,
    height=33.0
)

canvas.create_text(
    474.0,
    234.0,
    anchor="nw",
    text="Live Sensor Value",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

entry_image_9 = PhotoImage(
    file=relative_to_assets("entry_9.png"))
entry_bg_9 = canvas.create_image(
    534.0,
    270.5,
    image=entry_image_9
)
g.live_sensor_value_entry = Entry(
    bd=0,
    bg="#D3FCFE",
    fg="#000716",
    highlightthickness=0
)
g.live_sensor_value_entry.place(
    x=466.0,
    y=253.0,
    width=136.0,
    height=33.0
)

canvas.create_text(
    549.0,
    156.0,
    anchor="nw",
    text="Delta Pressure (kPa)",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

entry_image_10 = PhotoImage(
    file=relative_to_assets("entry_10.png"))
entry_bg_10 = canvas.create_image(
    618.0,
    192.5,
    image=entry_image_10
)
g.delta_pressure_entry = Entry(
    bd=0,
    bg="#D3FCFE",
    fg="#000716",
    highlightthickness=0
)
g.delta_pressure_entry.place(
    x=550.0,
    y=175.0,
    width=136.0,
    height=33.0
)

canvas.create_text(
    534.0,
    80.0,
    anchor="nw",
    text="Grasper Closing Time (s)",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

entry_image_11 = PhotoImage(
    file=relative_to_assets("entry_11.png"))
entry_bg_11 = canvas.create_image(
    618.0,
    116.5,
    image=entry_image_11
)
g.gripper_closing_time_entry = Entry(
    bd=0,
    bg="#D3FCFE",
    fg="#000716",
    highlightthickness=0
)
g.gripper_closing_time_entry.place(
    x=550.0,
    y=99.0,
    width=136.0,
    height=33.0
)

canvas.create_text(
    561.0,
    361.0,
    anchor="nw",
    text="Grasper Speed",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

entry_image_12 = PhotoImage(
    file=relative_to_assets("entry_12.png"))
entry_bg_12 = canvas.create_image(
    612.0,
    397.5,
    image=entry_image_12
)

gripper_speed_value = create_entry_value(
    'gripper_speed', entry_callback)

gripper_speed_entry = Entry(
    bd=0,
    bg="#FEDFD2",
    fg="#000716",
    highlightthickness=0,
    textvariable=gripper_speed_value
)
gripper_speed_entry.place(
    x=544.0,
    y=380.0,
    width=136.0,
    height=33.0
)
gripper_speed_entry.insert(0, g.gripper_speed)

canvas.create_text(
    797.0,
    361.0,
    anchor="nw",
    text="Idle Value",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

entry_image_13 = PhotoImage(
    file=relative_to_assets("entry_13.png"))
entry_bg_13 = canvas.create_image(
    830.0,
    397.5,
    image=entry_image_13
)

sensor_idle_entry_value = create_entry_value(
    'sensor_idle_value', entry_callback)

sensor_idle_value_entry = Entry(
    bd=0,
    bg="#FEDFD2",
    fg="#000716",
    highlightthickness=0,
    textvariable=sensor_idle_entry_value
)
sensor_idle_value_entry.place(
    x=762.0,
    y=380.0,
    width=136.0,
    height=33.0
)
sensor_idle_value_entry.insert(0, g.sensor_idle_value)

canvas.create_text(
    788.0,
    481.0,
    anchor="nw",
    text="Touch Value",
    fill="#6F6F6F",
    font=("Inter SemiBold", 14 * -1)
)

entry_image_14 = PhotoImage(
    file=relative_to_assets("entry_14.png"))
entry_bg_14 = canvas.create_image(
    830.0,
    517.5,
    image=entry_image_14
)

sensor_touch_entry_value = create_entry_value(
    'sensor_touch_value', entry_callback)

sensor_touch_value_entry = Entry(
    bd=0,
    bg="#FEDFD2",
    fg="#000716",
    highlightthickness=0,
    textvariable=sensor_touch_entry_value
)
sensor_touch_value_entry.place(
    x=762.0,
    y=500.0,
    width=136.0,
    height=33.0
)
sensor_touch_value_entry.insert(0, g.sensor_touch_value)

canvas.create_rectangle(
    -1.0,
    29.0,
    1200.0003662109375,
    30.0,
    fill="#D6D6D6",
    outline="")

canvas.create_rectangle(
    -1.0,
    56.0,
    1200.0003662109375,
    57.0,
    fill="#D6D6D6",
    outline="")

canvas.create_rectangle(
    -1.0,
    315.0,
    946.0,
    316.0,
    fill="#D6D6D6",
    outline="")

canvas.create_rectangle(
    -1.0,
    676.0,
    1200.0,
    677.0,
    fill="#D6D6D6",
    outline="")

canvas.create_rectangle(
    -1.0,
    344.0,
    946.0,
    345.0,
    fill="#D6D6D6",
    outline="")

canvas.create_rectangle(
    945.0,
    28.0,
    946.0,
    750.017333984375,
    fill="#D6D6D6",
    outline="")

canvas.create_rectangle(
    360.9999999999999,
    28.99920654296875,
    362.0,
    677.0,
    fill="#D6D6D6",
    outline="")

canvas.create_rectangle(
    712.0,
    28.99920654296875,
    713.0,
    677.0,
    fill="#D6D6D6",
    outline="")

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_9.bind("<Button-1>", lambda event: handleServoButton(4, 1))
button_9.bind("<ButtonRelease-1>", lambda event: handleServoButton(4, 0))
button_9.place(
    x=92.0,
    y=561.0,
    width=75.0,
    height=35.0
)

button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))

button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_10.bind("<Button-1>", lambda event: handleServoButton(1, 1))
button_10.bind("<ButtonRelease-1>", lambda event: handleServoButton(1, 0))


button_10.place(
    x=92.0,
    y=411.0,
    width=75.0,
    height=35.0
)

# Speed slider for overall control (from legacy code)


def slider_changed(event):
    speed = slider.get()
    setServoSpeed(99, speed)  # 99 means all servos


style = ttk.Style()
style.configure("Custom.Horizontal.TScale", troughcolor="white")

slider = ttk.Scale(window, from_=0, to=50, orient=tk.HORIZONTAL,
                   length=253, command=slider_changed, style="Custom.Horizontal.TScale")
slider.set(1)
slider.place(x=92, y=625)


button_image_11 = PhotoImage(
    file=relative_to_assets("button_11.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_11.bind("<Button-1>", lambda event: handleServoButton(1, 2))
button_11.bind("<ButtonRelease-1>", lambda event: handleServoButton(1, 0))
button_11.place(
    x=182.0,
    y=411.0,
    width=75.0,
    height=35.0
)

button_image_12 = PhotoImage(
    file=relative_to_assets("button_12.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_12.bind("<Button-1>", lambda event: handleServoButton(4, 2))
button_12.bind("<ButtonRelease-1>", lambda event: handleServoButton(4, 0))
button_12.place(
    x=182.0,
    y=561.0,
    width=75.0,
    height=35.0
)

button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_13.bind("<Button-1>", lambda event: handleServoButton(3, 2))
button_13.bind("<ButtonRelease-1>", lambda event: handleServoButton(3, 0))
button_13.place(
    x=182.0,
    y=511.0,
    width=75.0,
    height=35.0
)

button_image_14 = PhotoImage(
    file=relative_to_assets("button_14.png"))
button_14 = Button(
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_14.bind("<Button-1>", lambda event: handleServoButton(3, 1))
button_14.bind("<ButtonRelease-1>", lambda event: handleServoButton(3, 0))
button_14.place(
    x=92.0,
    y=511.0,
    width=75.0,
    height=35.0
)

button_image_15 = PhotoImage(
    file=relative_to_assets("button_15.png"))
button_15 = Button(
    image=button_image_15,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_15.bind("<Button-1>", lambda event: handleServoButton(2, 1))
button_15.bind("<ButtonRelease-1>", lambda event: handleServoButton(2, 0))
button_15.place(
    x=92.0,
    y=461.0,
    width=75.0,
    height=35.0
)

button_image_16 = PhotoImage(
    file=relative_to_assets("button_16.png"))
button_16 = Button(
    image=button_image_16,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_16.bind("<Button-1>", lambda event: handleServoButton(0, 1))
button_16.bind("<ButtonRelease-1>", lambda event: handleServoButton(0, 0))

button_16.place(
    x=92.0,
    y=361.0,
    width=75.0,
    height=35.0
)

button_image_17 = PhotoImage(
    file=relative_to_assets("button_17.png"))
button_17 = Button(
    image=button_image_17,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_17.bind("<Button-1>", lambda event: handleServoButton(0, 2))
button_17.bind("<ButtonRelease-1>", lambda event: handleServoButton(0, 0))
button_17.place(
    x=182.0,
    y=361.0,
    width=75.0,
    height=35.0
)

button_image_18 = PhotoImage(
    file=relative_to_assets("button_18.png"))
button_18 = Button(
    image=button_image_18,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_18.bind("<Button-1>", lambda event: handleServoButton(2, 2))
button_18.bind("<ButtonRelease-1>", lambda event: handleServoButton(2, 0))
button_18.place(
    x=182.0,
    y=461.0,
    width=75.0,
    height=35.0
)

button_image_19 = PhotoImage(
    file=relative_to_assets("button_19.png"))
gripper_close_button = Button(
    image=button_image_19,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)

gripper_close_button.bind(
    "<Button-1>", lambda event: handleGripperButton(1, True))

gripper_close_button.place(
    x=394.0,
    y=444.0,
    width=136.0,
    height=46.0
)

button_image_20 = PhotoImage(
    file=relative_to_assets("button_20.png"))
gripper_open_button = Button(
    image=button_image_20,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)

gripper_open_button.bind(
    "<Button-1>", lambda event: handleGripperButton(2, True))

gripper_open_button.place(
    x=544.0,
    y=444.0,
    width=136.0,
    height=46.0
)

canvas.create_rectangle(
    270.0,
    710.0,
    295.0,
    735.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    317.0,
    710.0,
    342.0,
    735.0,
    fill="#000000",
    outline="")

# Create the real-time graphs
graphs = create_graphs(window)

sensor_thread = threading.Thread(target=runSensorLoop)
sensor_thread.daemon = True
sensor_thread.start()

gripper_thread = threading.Thread(target=runGripperLoop)
gripper_thread.daemon = True
gripper_thread.start()

# Start the servo control thread
servo_thread = threading.Thread(target=runServoLoop)
servo_thread.daemon = True
servo_thread.start()

# window.resizable(False, False)
window.mainloop()
