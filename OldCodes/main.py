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

# Custom Functions Import
from exit import close_action
import g
from boardSetup import boardSetup
from updateConsole import updateConsole
from runSensor import runSensorLoop
from runGripper import runGripperLoop
from utils import updateSysFlag, export_data, handleGripperButton, pauseClaw, resetParams
from calculations import calcDeformationMM

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

window.title("Soft Robot Controller")

window.geometry("1200x641")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=641,
    width=1200,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    386.0,
    29.0,
    945.0,
    374.0,
    fill="#7D7D7D",
    outline="")

exit_btn_image = PhotoImage(
    file=relative_to_assets("button_1.png"))
exit_button = Button(
    image=exit_btn_image,
    borderwidth=0,
    highlightthickness=0,
    command=close_action,
    relief="flat"
)

exit_button.place(
    x=1151.0,
    y=577.0,
    width=40.0,
    height=35.0
)

g.consoleBox = Text(
    bd=0,
    bg="#ECFFEF",
    fg="#000716",
    highlightthickness=0
)
g.consoleBox.insert("end", "This is the main console"+"\n" +
                    "It will display all the actions performed by the robot" + "\n")

g.consoleBox.place(
    x=946.0,
    y=57.0,
    width=253.0,
    height=490.0
)

gripper_closing_entry_image = PhotoImage(
    file=relative_to_assets("entry_1.png"))
gripper_closing_time_entry_bg = canvas.create_image(
    661.0,
    428.0,
    image=gripper_closing_entry_image
)
g.gripper_closing_time_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0
)
g.gripper_closing_time_entry.insert(
    0, str("{:.4f}".format(g.gripper_closing_time)))
g.gripper_closing_time_entry.place(
    x=593.0,
    y=405.0,
    width=136.0,
    height=44.0
)

diameter_entry_image = PhotoImage(
    file=relative_to_assets("entry_2.png"))
diameter_entry_bg = canvas.create_image(
    496.0,
    428.0,
    image=diameter_entry_image
)
g.diameter_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0
)
g.diameter_entry.insert(0, str("{:.3f}".format(g.diameter)))
g.diameter_entry.place(
    x=428.0,
    y=405.0,
    width=136.0,
    height=44.0
)


delta_pressure_entry_image = PhotoImage(
    file=relative_to_assets("entry_3.png"))
delta_pressure_bg = canvas.create_image(
    833.0,
    427.0,
    image=delta_pressure_entry_image
)
g.delta_pressure_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0
)
g.delta_pressure_entry.insert(0, str("{:.3f}".format(g.delta_pressure)))
g.delta_pressure_entry.place(
    x=765.0,
    y=404.0,
    width=136.0,
    height=44.0
)

sensor_reading_entry_image = PhotoImage(
    file=relative_to_assets("entry_4.png"))
sensor_reading_bg = canvas.create_image(
    581.0,
    510.0,
    image=sensor_reading_entry_image
)
g.sensor_reading_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0
)
g.sensor_reading_entry.insert(0, str("{:.3f}".format(g.sensor_value)))
g.sensor_reading_entry.place(
    x=513.0,
    y=487.0,
    width=136.0,
    height=44.0
)

gripper_angle_image = PhotoImage(
    file=relative_to_assets("entry_5.png"))
gripper_angle_entry_bg = canvas.create_image(
    753.0,
    509.0,
    image=gripper_angle_image
)
g.gripper_angle_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0
)
g.gripper_angle_entry.insert(0, str("{:.3f}".format(g.gripper_degree)))
g.gripper_angle_entry.place(
    x=685.0,
    y=486.0,
    width=136.0,
    height=44.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
reset_button = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: resetParams(),
    relief="flat"
)
reset_button.place(
    x=435.0,
    y=572.0,
    width=96.12933349609375,
    height=46.0
)

start_button_img = PhotoImage(
    file=relative_to_assets("button_3.png"))
start_button = Button(
    image=start_button_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: updateSysFlag('1'),
    relief="flat"
)
start_button.place(
    x=560.62353515625,
    y=572.0,
    width=96.12933349609375,
    height=46.0
)

pause_button_img = PhotoImage(
    file=relative_to_assets("button_4.png"))
pause_button = Button(
    image=pause_button_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: updateSysFlag('0'),
    relief="flat"
)
pause_button.place(
    x=686.2470703125,
    y=572.0,
    width=96.12933349609375,
    height=46.0
)

export_button_img = PhotoImage(
    file=relative_to_assets("button_5.png"))
export_button = Button(
    image=export_button_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: export_data(g.export_timestamp, g.export_diameter, g.export_deformation, g.export_delta_pressure, g.export_sensor_value, g.export_closing_time, str(
        formatted_datetime)+'_data.csv'),
    relief="flat"
)
export_button.place(
    x=811.87060546875,
    y=572.0,
    width=96.12933349609375,
    height=46.0
)

gripper_close_btn_image = PhotoImage(
    file=relative_to_assets("button_6.png"))
gripper_close_btn = Button(
    image=gripper_close_btn_image,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
gripper_close_btn.bind(
    "<Button-1>", lambda event: handleGripperButton(1, True))
gripper_close_btn.place(
    x=89.0,
    y=446.0,
    width=136.0,
    height=46.0
)

gripper_open_btn_image = PhotoImage(
    file=relative_to_assets("button_7.png"))
gripper_open_btn = Button(
    image=gripper_open_btn_image,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)


def button_pressed():
    handleGripperButton(2, True)


def button_released():
    handleGripperButton(2, True)


gripper_open_btn.bind("<ButtonPress-1>", lambda event: button_pressed())
gripper_open_btn.bind("<ButtonRelease-1>", lambda event: button_released())

gripper_open_btn.place(
    x=239.0,
    y=446.0,
    width=136.0,
    height=46.0
)


###########################
gripper_pause_btn_image = PhotoImage(
    file=relative_to_assets("button_4.png"))
gripper_pause_btn = Button(
    image=gripper_pause_btn_image,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
gripper_pause_btn.bind("<Button-1>", lambda event: pauseClaw())
gripper_pause_btn.place(
    x=160.0,
    y=496.0,
    width=136.0,
    height=46.0
)
########################


def onChange_runtime(*args):
    try:
        g.run_time = float(runtime_entry.get() or 0.0)
        g.deformation_in_mm = calcDeformationMM()
        updateConsole("After Touch Run time Set to: " + str(g.run_time))
    except ValueError:
        updateConsole("Invalid input!")


runtime_text = StringVar()
runtime_text.trace_add('write', onChange_runtime)

precision_entry_image = PhotoImage(
    file=relative_to_assets("entry_6.png"))
precision_bg = canvas.create_image(
    130.50067138671875,
    78.5,
    image=precision_entry_image
)
runtime_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0,
    textvariable=runtime_text
)
runtime_entry.insert(0, g.run_time)
runtime_entry.place(
    x=89.00067138671875,
    y=61.0,
    width=83.0,
    height=33.0
)


def onChange_speed(*args):
    try:
        g.gripper_speed = float(speed_entry.get() or 0.0)
        updateConsole("Gripper Speed Set to: " + str(g.gripper_speed))
    except ValueError:
        updateConsole("Invalid input!")


speed_text = StringVar()
speed_text.trace_add('write', onChange_speed)

speed_entry_image = PhotoImage(
    file=relative_to_assets("entry_7.png"))
speed_bg = canvas.create_image(
    280.50067138671875,
    78.5,
    image=speed_entry_image
)
speed_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0,
    textvariable=speed_text
)
speed_entry.insert(0, g.gripper_speed)
speed_entry.place(
    x=239.00067138671875,
    y=61.0,
    width=83.0,
    height=33.0
)


def onChange_min_angle(*args):
    try:
        g.gripper_angle_min = float(min_angle_entry.get() or 0.0)
        updateConsole("Gripper Min Angle Set to: " + str(g.gripper_angle_min))
    except ValueError:
        updateConsole("Invalid input!")


min_angle_text = StringVar()
min_angle_text.trace_add('write', onChange_min_angle)

min_angle_image = PhotoImage(
    file=relative_to_assets("entry_8.png"))
min_angle_bg = canvas.create_image(
    129.50067138671875,
    143.5,
    image=min_angle_image
)
min_angle_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0,
    textvariable=min_angle_text
)
min_angle_entry.insert(0, g.gripper_angle_min)
min_angle_entry.place(
    x=88.00067138671875,
    y=126.0,
    width=83.0,
    height=33.0
)


def onChange_max_angle(*args):
    try:
        g.gripper_angle_max = float(max_angle_entry.get() or 0.0)
        updateConsole("Gripper Max Angle Set to: " + str(g.gripper_angle_max))
    except ValueError:
        updateConsole("Invalid input!")


max_angle_text = StringVar()
max_angle_text.trace_add('write', onChange_max_angle)

max_angle_image = PhotoImage(
    file=relative_to_assets("entry_9.png"))
max_angle_bg = canvas.create_image(
    279.50067138671875,
    143.5,
    image=max_angle_image
)
max_angle_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0,
    textvariable=max_angle_text
)
max_angle_entry.insert(0, g.gripper_angle_max)
max_angle_entry.place(
    x=238.00067138671875,
    y=126.0,
    width=83.0,
    height=33.0
)


def onChange_sensor_min(*args):
    try:
        g.sensor_min = float(sensor_min_entry.get() or 0.0)
        updateConsole("Sensor Resting Value Set to: " + str(g.sensor_min))
    except ValueError:
        updateConsole("Invalid input!")


sensor_min_text = StringVar()
sensor_min_text.trace_add('write', onChange_sensor_min)

sensor_min_image = PhotoImage(
    file=relative_to_assets("entry_10.png"))
sensor_min_bg = canvas.create_image(
    131.50067138671875,
    207.5,
    image=sensor_min_image
)
sensor_min_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0,
    textvariable=sensor_min_text
)
sensor_min_entry.insert(0, g.sensor_min)
sensor_min_entry.place(
    x=90.00067138671875,
    y=190.0,
    width=83.0,
    height=33.0
)


def onChange_sensor_max(*args):
    try:
        g.sensor_max = float(sensor_max_entry.get() or 0.0)
        updateConsole("Sensor Max Value Set to: " + str(g.sensor_max))
    except ValueError:
        updateConsole("Invalid input!")


sensor_max_text = StringVar()
sensor_max_text.trace_add('write', onChange_sensor_max)

entry_image_11 = PhotoImage(
    file=relative_to_assets("entry_11.png"))
entry_bg_11 = canvas.create_image(
    281.50067138671875,
    207.5,
    image=entry_image_11
)
sensor_max_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0,
    textvariable=sensor_max_text
)
sensor_max_entry.insert(0, g.sensor_max)
sensor_max_entry.place(
    x=240.00067138671875,
    y=190.0,
    width=83.0,
    height=33.0
)


def onChange_sensor_touch(*args):
    try:
        g.sensor_touch_value = float(sensor_touch_entry.get() or 0.0)
        updateConsole("Sensor Touch Value Set to: " +
                      str(g.sensor_touch_value))
    except ValueError:
        updateConsole("Invalid input!")


sensor_touch_text = StringVar()
sensor_touch_text.trace_add('write', onChange_sensor_touch)

sensor_touch_image = PhotoImage(
    file=relative_to_assets("entry_12.png"))
sensor_touch_bg = canvas.create_image(
    131.5,
    270.5,
    image=sensor_touch_image
)
sensor_touch_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0,
    textvariable=sensor_touch_text
)
sensor_touch_entry.insert(0, g.sensor_touch_value)
sensor_touch_entry.place(
    x=90.0,
    y=253.0,
    width=83.0,
    height=33.0
)


def onChange_sample_rate(*args):
    try:
        g.sample_rate = float(sample_rate_entry.get() or 0.0)
        updateConsole("Sampling Rate Set to: " +
                      str(g.sample_rate))
    except ValueError:
        updateConsole("Invalid input!")


sample_rate_text = StringVar()
sample_rate_text.trace_add('write', onChange_sample_rate)

sample_rate_image = PhotoImage(
    file=relative_to_assets("entry_13.png"))
sample_rate_bg = canvas.create_image(
    281.50067138671875,
    270.5,
    image=sample_rate_image
)
sample_rate_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0,
    textvariable=sample_rate_text
)
sample_rate_entry.insert(0, g.sample_rate)
sample_rate_entry.place(
    x=240.00067138671875,
    y=253.0,
    width=83.0,
    height=33.0
)


# def onChange_deformation_degree(*args):
#     try:
#         g.deformation_degree = float(deformation_degree_entry.get() or 0.0)
#         updateConsole("Deformation Factor Set to: " +
#                       str(g.deformation_degree))

#         g.deformation_in_mm = convertDeformationDegreeToMM(
#             g.deformation_degree)

#         g.deformation_mm_entry.delete(0, tk.END)

#         g.deformation_mm_entry.insert(
#             0, str("{:.3f}".format(g.deformation_in_mm)))

#     except ValueError:
#         updateConsole("Invalid input!")


# deformation_degree_text = StringVar()
# deformation_degree_text.trace_add('write', onChange_deformation_degree)

# deformation_degree_image = PhotoImage(
#     file=relative_to_assets("entry_14.png"))
# deformation_degree_bg = canvas.create_image(
#     280.50067138671875,
#     345.5,
#     image=deformation_degree_image
# )
# deformation_degree_entry = Entry(
#     bd=0,
#     bg="#DAE4FF",
#     fg="#000716",
#     highlightthickness=0,
#     textvariable=deformation_degree_text
# )
# deformation_degree_entry.insert(0, g.deformation_degree)
# deformation_degree_entry.place(
#     x=90.0,
#     y=328.0,
#     width=83.0,
#     height=33.0

# )


def onChange_sensorKpa_factor(*args):
    try:
        g.sensor_to_pressure_factor = float(sensorKpa_entry.get() or 0.0)
        updateConsole("Sensor to kPa Factor Set to: " +
                      str(g.sensor_to_pressure_factor))
    except ValueError:
        updateConsole("Invalid input!")


sensorKpa_text = StringVar()
sensorKpa_text.trace_add('write', onChange_sensorKpa_factor)

sensorKpa_image = PhotoImage(
    file=relative_to_assets("entry_15.png"))
sensorKpa_bg = canvas.create_image(
    131.5,
    345.5,
    image=sensorKpa_image
)
sensorKpa_entry = Entry(
    bd=0,
    bg="#DAE4FF",
    fg="#000716",
    highlightthickness=0,
    textvariable=sensorKpa_text
)
sensorKpa_entry.insert(0, g.sensor_to_pressure_factor)
sensorKpa_entry.place(
    x=239.00067138671875,
    y=328.0,
    width=83.0,
    height=33.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat"
)
button_8.place(
    x=184.00067138671875,
    y=61.0,
    width=41.0,
    height=35.0
)

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_9 clicked"),
    relief="flat"
)
button_9.place(
    x=334.00067138671875,
    y=61.0,
    width=41.0,
    height=35.0
)

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_10 clicked"),
    relief="flat"
)
button_10.place(
    x=183.00067138671875,
    y=126.0,
    width=41.0,
    height=35.0
)

button_image_11 = PhotoImage(
    file=relative_to_assets("button_11.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_11 clicked"),
    relief="flat"
)
button_11.place(
    x=333.00067138671875,
    y=126.0,
    width=41.0,
    height=35.0
)

button_image_12 = PhotoImage(
    file=relative_to_assets("button_12.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_12 clicked"),
    relief="flat"
)
button_12.place(
    x=185.00067138671875,
    y=190.0,
    width=41.0,
    height=35.0
)

button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_13 clicked"),
    relief="flat"
)
button_13.place(
    x=185.0,
    y=253.0,
    width=41.0,
    height=35.0
)

button_image_14 = PhotoImage(
    file=relative_to_assets("button_14.png"))
button_14 = Button(
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_14 clicked"),
    relief="flat"
)
button_14.place(
    x=185.0,
    y=328.0,
    width=41.0,
    height=35.0
)

button_image_15 = PhotoImage(
    file=relative_to_assets("button_15.png"))
button_15 = Button(
    image=button_image_15,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_15 clicked"),
    relief="flat"
)
button_15.place(
    x=335.00067138671875,
    y=190.0,
    width=41.0,
    height=35.0
)

button_image_16 = PhotoImage(
    file=relative_to_assets("button_16.png"))
button_16 = Button(
    image=button_image_16,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_16 clicked"),
    relief="flat"
)
button_16.place(
    x=335.00067138671875,
    y=253.0,
    width=41.0,
    height=35.0
)


button_image_17 = PhotoImage(
    file=relative_to_assets("button_17.png"))
button_17 = Button(
    image=button_image_17,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_17 clicked"),
    relief="flat"
)
button_17.place(
    x=334.00067138671875,
    y=328.0,
    width=41.0,
    height=35.0
)


def CreateAllCanvasComponents(canvas):

    canvas.create_text(
        238.0,
        306.0,
        anchor="nw",
        text="Sensor to kPa",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        511.0,
        462.0,
        anchor="nw",
        text="Live Sensor Reading",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        689.0,
        462.0,
        anchor="nw",
        text="Live Gripper Angle",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_rectangle(
        10.0,
        337.0,
        25.0,
        352.0,
        fill="#FD01D5",
        outline="")

    canvas.create_text(
        28.0,
        335.0,
        anchor="nw",
        text="Factors",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        94.0,
        306.0,
        anchor="nw",
        text="Deformation Degree",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_rectangle(
        9.0,
        460.0,
        24.0,
        475.0,
        fill="#00CECE",
        outline="")

    canvas.create_rectangle(
        946.0,
        57.0,
        1200.0,
        548.0,
        fill="#DCFFD0",
        outline="")

    canvas.create_text(
        428.0,
        1.0,
        anchor="nw",
        text="SOFT BOT CONTROL PANEL (JAW ONLY)",
        fill="#727272",
        font=("Inter SemiBold", 24 * -1)
    )

    canvas.create_text(
        31.0,
        458.0,
        anchor="nw",
        text="Control",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        580.0,
        380.0,
        anchor="nw",
        text="Gripper Closing Time(sec)",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        443.0,
        380.0,
        anchor="nw",
        text="Diameter (mm)",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        762.0,
        380.0,
        anchor="nw",
        text="Delta Pressure (kPa)",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        164.0,
        379.0,
        anchor="nw",
        text="GRASPER CONTROL",
        fill="#6F6F6F",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        137.0,
        419.0,
        anchor="nw",
        text="CLOSE",
        fill="#6F6F6F",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        292.0,
        419.0,
        anchor="nw",
        text="OPEN",
        fill="#6F6F6F",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        1043.0,
        38.0,
        anchor="nw",
        text="CONSOLE",
        fill="#6F6F6F",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        1.0,
        594.0,
        anchor="nw",
        text="NIFE LAB",
        fill="#4E4D4D",
        font=("Inter SemiBold", 20 * -1)
    )

    canvas.create_rectangle(
        -1.0,
        29.5,
        387.00128173828125,
        30.5,
        fill="#D6D6D6",
        outline="")

    canvas.create_rectangle(
        -1.0,
        29.0,
        1200.0003662109375,
        30.0,
        fill="#D6D6D6",
        outline="")

    canvas.create_rectangle(
        386.375,
        28.98992919921875,
        387.375,
        548.000244140625,
        fill="#D6D6D6",
        outline="")

    canvas.create_rectangle(
        944.9999999734582,
        27.99998241843423,
        947.0,
        548.0,
        fill="#D6D6D6",
        outline="")

    canvas.create_rectangle(
        -1.0,
        547.0,
        946.0,
        548.0000000059013,
        fill="#D6D6D6",
        outline="")

    canvas.create_rectangle(
        -1.0,
        373.0,
        946.0,
        374.00000000590126,
        fill="#D6D6D6",
        outline="")

    canvas.create_rectangle(
        944.99609375,
        56.0,
        1200.0039672851562,
        57.0,
        fill="#D6D6D6",
        outline="")

    canvas.create_rectangle(
        946.0,
        547.0,
        1201.0078735351562,
        548.0,
        fill="#D6D6D6",
        outline="")

    canvas.create_rectangle(
        0.0,
        30.0,
        388.0,
        306.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        9.00067138671875,
        70.0,
        24.00067138671875,
        85.0,
        fill="#0008CE",
        outline="")

    canvas.create_rectangle(
        9.00067138671875,
        135.0,
        24.00067138671875,
        150.0,
        fill="#8C00CE",
        outline="")

    canvas.create_rectangle(
        10.00067138671875,
        199.0,
        25.00067138671875,
        214.0,
        fill="#CE003D",
        outline="")

    canvas.create_rectangle(
        10.00067138671875,
        262.0,
        25.00067138671875,
        277.0,
        fill="#CE9400",
        outline="")

    canvas.create_text(
        34.00067138671875,
        68.0,
        anchor="nw",
        text="Move",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        97.0,
        38.0,
        anchor="nw",
        text="Aftertouch Runtime",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        255.0,
        38.0,
        anchor="nw",
        text="Speed",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        33.00067138671875,
        133.0,
        anchor="nw",
        text="Angle",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        113.0,
        103.0,
        anchor="nw",
        text="Min",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        266.0,
        103.0,
        anchor="nw",
        text="Max",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        32.00067138671875,
        197.0,
        anchor="nw",
        text="Sensor",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        30.0,
        252.0,
        anchor="nw",
        text="Sensor ",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        30.0,
        266.0,
        anchor="nw",
        text="Touch",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        104.0,
        167.0,
        anchor="nw",
        text="Resting",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        262.0,
        167.0,
        anchor="nw",
        text="Max",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        88.0,
        231.0,
        anchor="nw",
        text="Touch Value",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        240.0,
        231.0,
        anchor="nw",
        text="Sample Rates/s",
        fill="#3B3D70",
        font=("Inter SemiBold", 14 * -1)
    )


CreateAllCanvasComponents(canvas)

gripper_thread = threading.Thread(target=runGripperLoop)
gripper_thread.daemon = True
gripper_thread.start()


sensor_thread = threading.Thread(target=runSensorLoop)
sensor_thread.daemon = True
sensor_thread.start()

window.resizable(False, False)
window.mainloop()
