import g
import time
from updateConsole import updateConsole
from calculations import calcEstar
from getTableParams import getTableParams


def calculate_custom_delay(speed):
    if speed < 1:
        custom_delay = 1.0
    else:
        custom_delay = 1.0 / speed
    return custom_delay


def moveMotor():
    try:
        if g.gripper_direction == 1:
            g.board.digital[g.pin_step_direction].write(0)
        else:
            g.board.digital[g.pin_step_direction].write(1)

        g.board.digital[g.pin_step_active].write(1)
        time.sleep(0.0001)
        g.board.digital[g.pin_step_active].write(0)

        print(f"Step Count: {g.step_count}")
        g.step_count += 1
    except Exception as e:
        print(f"Unable to write to Arduino board: {e}")


def runGripperLoop():
    while True:
        try:
            if g.runSystem_flag:
                custom_delay = calculate_custom_delay(g.gripper_speed)

                if g.motor_active:
                    if g.gripper_direction == 1:
                        updateConsole(
                            f"Gripper Closing for: {g.gripper_closing_time:.4f} seconds")
                        if not g.gripper_start_time_flag:
                            g.gripper_start_time_flag = True
                            g.gripper_starting_time = time.monotonic()

                        if not g.touched_flag and g.gripper_start_time_flag:
                            g.gripper_closing_time = time.monotonic() - g.gripper_starting_time

                    print("Stepper is active")
                    moveMotor()

                    if g.touched_flag:
                        if (g.active_run_time + (time.monotonic() - g.time_of_touch)) > g.run_time:
                            g.motor_active = False
                            g.active_run_time = 0
                            continue
                    else:
                        g.active_run_time = 0

                time.sleep(custom_delay)
        except Exception as e:
            print(f"Error in gripper loop: {e}")
