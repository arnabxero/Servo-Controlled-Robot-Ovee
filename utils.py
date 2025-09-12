from tkinter import StringVar
import g
import time
import tkinter as tk
import csv
import os


def entry_callback(entry_name, var):
    try:
        value = float(var.get())
        setattr(g, entry_name, value)
        print(f'Updated {entry_name}: {getattr(g, entry_name)}')
        # UpdateConsole
        # UpdateLogger

    except ValueError:
        print(f'Invalid Value on {entry_name}')
        # UpdateConsole
        # UpdateLogger


def create_entry_value(entry_name, callback):
    var = StringVar()
    var.trace_add("write", lambda name, index, mode,
                  var=var: callback(entry_name, var))
    return var


def handleGripperButton(direction, motorActive):
    g.gripper_direction = direction
    # if (g.gripper_direction != 2):
    #     g.sensor_touch_flag = False
    g.sensor_touch_flag = False
    g.gripper_active = motorActive
    print("Gripper Direction: " + str(g.gripper_direction))
    print("Gripper Active: " + str(g.gripper_active))
    # UpdateLogger


def preciseSleep(duration):
    """Busy-wait sleep for more accurate timing."""
    end_time = time.monotonic() + duration
    while time.monotonic() < end_time:
        pass


def calculate_custom_delay(speed):
    if speed < 1:
        custom_delay = 1.0
    else:
        custom_delay = 1.0 / speed
    return custom_delay


def resetGripper():
    g.gripper_speed = 100
    g.gripper_direction = 0
    g.gripper_active = False
    g.gripper_steps = 0
    g.sensor_touch_flag = False
    g.gripper_closing_time = 0
    g.time_of_touch = 0
    g.gripper_starting_time = 0.0
    g.gripper_start_time_flag = False
    print("Resetting Gripper Parameters...")
    # UpdateConsole
    # UpdateLogger


def autoSetSensorIdle(sensor_idle_value_entry):
    g.sensor_idle_value = g.sensor_value + 0.01
    sensor_idle_value_entry.delete(0, tk.END)
    sensor_idle_value_entry.insert(
        0, str("{:.4f}".format(g.sensor_idle_value)))
    # Resolve: Invalid Value on sensor_idle_value error

    print("Sensor Idle Value Set to: "+str(g.sensor_idle_value))
    # UpdateConsole
    # UpdateLogger


def clearExportVariables():
    g.export_timestamp.clear()
    g.export_diameter.clear()
    g.export_delta_pressure.clear()
    g.export_deformation.clear()
    g.export_sensor_value.clear()
    g.export_closing_time.clear()
    print("Cleared Export Variables")


def append_to_csv(first_row, column1_data, column2_data, column3_data, column4_data, column5_data, column6_data):
    with open('Data_'+str(g.fileNumber)+'.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        if first_row:
            writer.writerow(
                ['Time', 'Dia (mm)', 'd (mm)', 'Delta P (KPa)', 'Sensor Voltage', 'Closing Time (Sec)'])

        writer.writerow([str(column1_data), str(column2_data), str(
            column3_data), str(column4_data), str(column5_data), str(column6_data)])


def exportData(array1, array2, array3, array4, array5, array6):
    for i in range(len(array1)):
        element1 = array1[i]
        element2 = array2[i]
        element3 = array3[i]
        element4 = array4[i]
        element5 = array5[i]
        element6 = array6[i]

        first_row = False

        if i == 0:
            first_row = True
        else:
            first_row = False

        print(element1, element2, element3, element4, element5, element6)

        append_to_csv(first_row, element1, element2,
                      element3, element4, element5, element6)

    g.fileNumber = g.fileNumber + 1


def close_action():
    print("Exiting...")
    os._exit(0)
