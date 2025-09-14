import g
import tkinter as tk
import time
import datetime
from calculations import calcDeltaPressure, calcDiameterFromSteps, calcDeformationMM


def runSensorLoop():
    while True:

        # Check if stop switch is triggered - ONLY when opening (direction 2)
        if (g.stop_switch_pin and
            g.stop_switch_pin.read() == True and
            g.gripper_active == True and
                g.gripper_direction == 2):  # Only check when opening

            if not g.auto_calibration_complete:
                # Auto-calibration complete
                print(
                    "Auto-calibration complete! Gripper is now at fully open position.")
                print(
                    f"Step counter reset to 0. Max diameter set to {g.max_diameter_mm} mm")
                g.auto_calibration_complete = True
                g.gripper_steps = 0  # Reset step counter at fully open position
                g.diameter_in_mm = g.max_diameter_mm
            else:
                print("Stop Switch Activated - Gripper fully opened")

            g.gripper_direction = 0
            g.gripper_active = False
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

            # Record the diameter at touch point
            g.touch_point_diameter_mm = g.diameter_in_mm

            print("Sensor Touched")
            print(f"Touch point diameter: {g.touch_point_diameter_mm:.4f} mm")
            print(f"Target deformation: {g.target_deformation_in_mm:.4f} mm")
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

        # Use the new step-based calculation
        g.diameter_in_mm = calcDiameterFromSteps()
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

        # FIXED: Only update the display deformation, not the target deformation
        if (g.sensor_touch_flag == False):
            # Display 0 deformation when not touching
            g.deformation_mm_entry.delete(0, tk.END)
            g.deformation_mm_entry.insert(0, "0.0000")
            g.export_deformation.append(0)
        else:
            # Calculate and display actual deformation
            g.deformation_in_mm = calcDeformationMM()
            g.deformation_mm_entry.delete(0, tk.END)
            g.deformation_mm_entry.insert(
                0, str("{:.4f}".format(g.deformation_in_mm)))
            g.export_deformation.append(g.deformation_in_mm)

        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S.%f")
        g.export_timestamp.append(formatted_time)

        time.sleep(1/float(g.sample_rate or 1))
