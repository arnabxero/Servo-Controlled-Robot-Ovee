import g
import tkinter as tk
import time
import datetime
from calculations import calcDeltaPressure, calcDiameterFromSteps, calcDeformationMM


def calculate_pressure_slope():
    """Calculate slope between pressure and sqrt(deformation) using linear regression"""
    import math

    current_pressure = g.delta_pressure
    current_deformation_sqrt = math.sqrt(
        max(g.deformation_in_mm, 0.001))  # Avoid division by zero

    # Initialize data arrays if they don't exist
    if not hasattr(g, 'pressure_history'):
        g.pressure_history = []
        g.deformation_sqrt_history = []

    # Only collect data when we're in deformation phase
    if g.sensor_touch_flag and g.deformation_in_mm > 0:
        g.pressure_history.append(current_pressure)
        g.deformation_sqrt_history.append(current_deformation_sqrt)

        # Keep only recent data points (last 20 points for better performance)
        max_points = 20
        if len(g.pressure_history) > max_points:
            g.pressure_history = g.pressure_history[-max_points:]
            g.deformation_sqrt_history = g.deformation_sqrt_history[-max_points:]

        # Calculate linear regression slope (y = mx, where y is pressure, x is sqrt(deformation))
        if len(g.pressure_history) >= 2:
            n = len(g.pressure_history)

            # Calculate means
            x_mean = sum(g.deformation_sqrt_history) / n
            y_mean = sum(g.pressure_history) / n

            # Calculate slope using least squares method: m = Σ(xi*yi) / Σ(xi²)
            # For y = mx (no intercept), slope = Σ(xi*yi) / Σ(xi²)
            numerator = sum(
                x * y for x, y in zip(g.deformation_sqrt_history, g.pressure_history))
            denominator = sum(x * x for x in g.deformation_sqrt_history)

            if denominator != 0:
                g.pressure_slope = numerator / denominator
            else:
                g.pressure_slope = 0.0
        else:
            g.pressure_slope = 0.0
    else:
        # Reset data arrays when not in deformation phase
        if not g.sensor_touch_flag:
            g.pressure_history = []
            g.deformation_sqrt_history = []
            g.pressure_slope = 0.0

    # Update previous values for reference
    g.previous_pressure = current_pressure
    g.previous_deformation_sqrt = current_deformation_sqrt


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

        # Calculate pressure slope for graphing
        calculate_pressure_slope()

        # Update the final value entry with live slope value
        g.final_value_entry.delete(0, tk.END)
        g.final_value_entry.insert(0, str("{:.4f}".format(g.pressure_slope)))

        # Add slope to export data
        if not hasattr(g, 'export_slope'):
            g.export_slope = []
        g.export_slope.append(g.pressure_slope)

        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S.%f")
        g.export_timestamp.append(formatted_time)

        time.sleep(1/float(g.sample_rate or 1))
