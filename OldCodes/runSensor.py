import g
import tkinter as tk
import time
from updateConsole import updateConsole
from calculations import calcEstar, calcDeltaPressure, calcDiameter, calcDiameterFromRunTime
import datetime  # Import the datetime module


def runSensorLoop():

    while True:
        if (g.runSystem_flag == True):
            updateConsole("SYSTEM RUNNING")

            if ((g.gripper_direction == 2) and (g.stop_switch_pin.read() == True)):
                print("Stop Switch Activated")
                updateConsole("Stop Switch Activated")
                g.motor_active = False

            try:
                g.sensor_value = (g.sensor.read() * 5.0) or 0.0

            except:
                # give random values
                updateConsole("WARNING: SENSOR FUNCTION FAILED")
                g.sensor_value = 0

            if (g.sensor_value >= (g.sensor_min + g.sensor_touch_value) and g.touched_flag == False):
                # print("Current Sensor Value:" + str(g.sensor_value))
                # print("Min Sensor Value:" + str(g.sensor_min))
                # print("Touch Sensor Value:" + str(g.sensor_touch_value))
                # print("Flag Touched:" + str(g.touched_flag))

                g.time_of_touch = time.monotonic()
                g.touched_flag = True
                print("Touched")
                updateConsole("Touched")

            g.sensor_reading_entry.delete(0, tk.END)
            g.sensor_reading_entry.insert(
                0, str("{:.4f}".format(g.sensor_value)))
            g.export_sensor_value.append(g.sensor_value)

            g.delta_pressure = calcDeltaPressure(g.sensor_value)
            g.delta_pressure_entry.delete(0, tk.END)
            g.delta_pressure_entry.insert(
                0, str("{:.4f}".format(g.delta_pressure)))
            g.export_delta_pressure.append(g.delta_pressure)

            g.diameter = calcDiameterFromRunTime()
            g.diameter_entry.delete(0, tk.END)
            g.diameter_entry.insert(0, str("{:.4f}".format(g.diameter)))
            g.export_diameter.append(g.diameter)

            g.gripper_closing_time_entry.delete(0, tk.END)
            g.gripper_closing_time_entry.insert(
                0, str("{:.4f}".format(g.gripper_closing_time)))

            # Track the timestamp
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S.%f")
            g.export_timestamp.append(formatted_time)

            if (g.touched_flag == False):
                g.export_deformation.append(0)
            else:
                g.export_deformation.append(g.deformation_in_mm)

            if (g.gripper_direction == 1):
                g.export_closing_time.append(g.gripper_closing_time)
            else:
                g.export_closing_time.append(0)

            updateConsole("Sensor Value: " + str(g.sensor_value))

        else:
            print("System Paused")
            # updateConsole("System is paused")

        time.sleep(1/float(g.sample_rate or 1))
