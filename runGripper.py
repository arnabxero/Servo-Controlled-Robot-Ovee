import g
import time

# Custom Imports
from utils import preciseSleep, calculate_custom_delay


def moveMotor():
    try:
        if (g.gripper_direction == 1):  # Closing
            g.board.digital[g.pin_step_direction].write(0)
            g.gripper_steps += 1  # Increment when closing
        elif (g.gripper_direction == 2):  # Opening
            g.board.digital[g.pin_step_direction].write(1)
            g.gripper_steps -= 1  # Decrement when opening
            # Ensure steps don't go below 0 (can't open more than fully open)
            g.gripper_steps = max(0, g.gripper_steps)

        g.board.digital[g.pin_step_active].write(1)
        preciseSleep(0.0001)
        g.board.digital[g.pin_step_active].write(0)

        print(
            f"Step Count: {g.gripper_steps}, Direction: {g.gripper_direction}")
        # UpdateConsole

    except Exception as e:
        print(f"Unable to write to Arduino board: {e}")
        # UpdateConsole


def runGripperLoop():
    while True:
        custom_delay = calculate_custom_delay(g.gripper_speed)
        start_time = time.monotonic()

        if (g.gripper_active == True):

            if (g.gripper_direction == 1):  # Closing

                if (g.gripper_start_time_flag == False):
                    g.gripper_start_time_flag = True
                    g.gripper_starting_time = time.monotonic()

                if ((g.sensor_touch_flag == False) and (g.gripper_start_time_flag == True)):
                    g.gripper_closing_time = (
                        time.monotonic() - g.gripper_starting_time)
                    # print("Gripper Closing For: " + str(g.gripper_closing_time))
                    # UpdateConsole

            moveMotor()

            if (g.sensor_touch_flag == True):
                if ((time.monotonic() - g.time_of_touch) > g.aftertouch_runtime):
                    g.gripper_active = False
                    continue

        end_time = time.monotonic()
        elapsed_time = end_time - start_time
        remaining_time = custom_delay - elapsed_time

        if (remaining_time > 0):
            preciseSleep(remaining_time)
