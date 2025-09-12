import g
import tkinter as tk
import time
import datetime
from calculations import calcDeltaPressure, calcDiameterFromRunTime, calcDeformationMM


def runSensorLoop():
    while True:

        # Check if stop switch is triggered
        if ((g.gripper_direction == 2) and (g.stop_switch_pin.read() == True) and (g.gripper_active == True)):
            g.gripper_direction = 0
            g.gripper_active = False
            print("Stop Switch Activated")
            # UpdateConsole
            # UpdateLogger

        try:
            g.sensor_value = (g.sensor.read() * 5.0) or 0.0
        except:
            print("Warning: Sensor Read Error")
            None

            # UpdateConsole

        if ((g.sensor_value >= (g.sensor_idle_value + g.sensor_touch_value)) and (g.sensor_touch_flag == False) and (g.gripper_direction == 1)):
            g.time_of_touch = time.monotonic()
            g.sensor_touch_flag = True
            print("Sensor Touched")
            # UpdateConsole
            # UpdateLogger

        # Updating all display entries and export variables
        g.live_sensor_value_entry.delete(0, tk.END)
        g.live_sensor_value_entry.insert(
            0, str("{:.4f}".format(g.sensor_value)))
        g.export_sensor_value.append(g.sensor_value)

        g.delta_pressure = calcDeltaPressure(g.sensor_value)
        g.delta_pressure_entry.delete(0, tk.END)
        g.delta_pressure_entry.insert(
            0, str("{:.4f}".format(g.delta_pressure)))
        g.export_delta_pressure.append(g.delta_pressure)

        g.diameter_in_mm = calcDiameterFromRunTime()
        g.diameter_mm_entry.delete(0, tk.END)
        g.diameter_mm_entry.insert(0, str("{:.4f}".format(g.diameter_in_mm)))
        g.export_diameter.append(g.diameter_in_mm)

        g.gripper_closing_time_entry.delete(0, tk.END)
        g.gripper_closing_time_entry.insert(
            0, str("{:.4f}".format(g.gripper_closing_time)))
        if (g.gripper_direction == 1):
            g.export_closing_time.append(g.gripper_closing_time)
        else:
            g.export_closing_time.append(0)

        if (g.sensor_touch_flag == False):
            g.deformation_in_mm = 0
            g.deformation_mm_entry.delete(0, tk.END)
            g.deformation_mm_entry.insert(0, 0)
            g.export_deformation.append(0)
        else:
            g.deformation_in_mm = calcDeformationMM()
            g.deformation_mm_entry.delete(0, tk.END)
            g.deformation_mm_entry.insert(
                0, str("{:.4f}".format(g.deformation_in_mm)))
            g.export_deformation.append(g.deformation_in_mm)

        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S.%f")
        g.export_timestamp.append(formatted_time)

        time.sleep(1/float(g.sample_rate or 1))
