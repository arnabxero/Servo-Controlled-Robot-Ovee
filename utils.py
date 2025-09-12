from tkinter import StringVar
import g
import time
import tkinter as tk
import csv
import os
from runServo import setServoToHome


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


def checkStopSwitchStatus():
    """Check if stop switch is already pressed at startup"""
    try:
        if g.stop_switch_pin and g.stop_switch_pin.read() == True:
            return True
        return False
    except Exception as e:
        print(f"Error reading stop switch: {e}")
        return False


def autoCalibrateDiameter():
    """Auto-calibrate the gripper by opening to full extent until stop switch is hit"""
    print("Starting auto-calibration...")

    # Give Arduino pins time to stabilize after connection
    print("Waiting for Arduino to stabilize...")
    time.sleep(2)  # Wait 2 seconds for pins to stabilize

    # Now check if stop switch is already pressed
    if checkStopSwitchStatus():
        print("Stop switch is already pressed!")
        print("Gripper appears to be already at fully open position.")
        print("Skipping auto-calibration and setting reference point.")

        # Set calibration as complete without moving
        g.auto_calibration_complete = True
        g.gripper_steps = 0  # Reset step counter at current position
        g.diameter_in_mm = g.max_diameter_mm
        g.gripper_direction = 0
        g.gripper_active = False

        print(
            f"Auto-calibration complete! Step counter set to 0. Max diameter set to {g.max_diameter_mm} mm")
        return

    print("Stop switch is not pressed. Opening gripper to full extent...")

    # Save current speed
    original_speed = g.gripper_speed

    # Set high speed for calibration (much faster)
    g.gripper_speed = 500  # 5x faster than normal

    # Reset step counter and set initial diameter
    g.gripper_steps = 0
    g.diameter_in_mm = g.max_diameter_mm

    # Start opening the gripper
    g.gripper_direction = 2  # Opening direction
    g.gripper_active = True
    g.sensor_touch_flag = False

    print(
        f"Gripper opening at high speed ({g.gripper_speed})... waiting for stop switch activation")

    # Wait for auto-calibration to complete with timeout
    start_time = time.time()
    timeout = 30  # 30 second timeout

    while not g.auto_calibration_complete:
        time.sleep(0.1)  # Check every 100ms

        # Safety timeout
        if time.time() - start_time > timeout:
            print("WARNING: Auto-calibration timeout! Stop switch may not be working.")
            print("Stopping gripper and setting calibration as complete.")
            g.gripper_active = False
            g.gripper_direction = 0
            g.auto_calibration_complete = True
            break

    # Restore original speed after calibration
    g.gripper_speed = original_speed
    print(f"Auto-calibration complete! Speed restored to {original_speed}")


def handleGripperButton(direction, motorActive):
    # Only allow manual control if auto-calibration is complete
    if not g.auto_calibration_complete and direction != 2:
        print("Auto-calibration in progress. Manual control disabled until calibration complete.")
        return

    g.gripper_direction = direction
    g.sensor_touch_flag = False
    g.gripper_active = motorActive
    print("Gripper Direction: " + str(g.gripper_direction))
    print("Gripper Active: " + str(g.gripper_active))
    # UpdateLogger


# New servo control functions
def handleServoButton(servo_num, direction):
    """Handle servo movement button press"""
    g.servo_direction[servo_num] = direction
    print(f"Servo {servo_num} is now moving direction {direction}")
    # UpdateConsole
    # UpdateLogger


def setServoSpeed(servo_num, speed):
    """Set speed for a specific servo or all servos"""
    try:
        speed = float(speed)

        if servo_num != 99:  # Specific servo
            g.servo_speed[servo_num] = speed
            print(f"Servo {servo_num} speed set to {speed} degrees per step")
        else:  # All servos (servo_num == 99)
            for i in range(len(g.servo_speed)):
                g.servo_speed[i] = speed
            print(f"All servos speed set to {speed} degrees per step")
            # Update entry fields if they exist
            refreshServoSpeedEntries()

        # UpdateConsole
        # UpdateLogger

    except ValueError:
        print(f"Invalid speed value: {speed}")
        # UpdateConsole
        # UpdateLogger


def refreshServoSpeedEntries():
    """Refresh all servo speed entry fields with current values"""
    try:
        for i, entry in enumerate(g.servo_speed_entries):
            if entry is not None:
                entry.delete(0, tk.END)
                entry.insert(0, str(g.servo_speed[i]))
    except:
        print("Minor Warning - Unable to refresh servo speed entries")


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
    if not g.auto_calibration_complete:
        print("Cannot reset gripper during auto-calibration")
        return

    g.gripper_speed = 100
    g.gripper_direction = 0
    g.gripper_active = False
    g.gripper_steps = 0
    g.sensor_touch_flag = False
    g.gripper_closing_time = 0
    g.time_of_touch = 0
    g.gripper_starting_time = 0.0
    g.gripper_start_time_flag = False

    # Reset diameter to max (fully open)
    g.diameter_in_mm = g.max_diameter_mm

    print("Resetting Gripper Parameters...")
    # UpdateConsole
    # UpdateLogger


def resetServos():
    """Reset all servo parameters to default values"""
    g.servo_direction = [0, 0, 0, 0, 0]
    g.servo_speed = [1, 1, 1, 1, 1]
    print("Resetting Servo Parameters...")
    refreshServoSpeedEntries()
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
    """Handle application closure without moving servos"""
    print("Exiting...")
    g.exit_flag = True

    # Move servos to home positions
    setServoToHome()

    # Don't move servos - leave them where they are
    print("Servos left in current positions")
    os._exit(0)
