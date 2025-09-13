import g
import time
from console_logger import log_console


def moveServo(servo_index):
    """Move a specific servo based on its direction and speed"""
    try:
        cur_loc = g.board.digital[g.servo_pins[servo_index]].read()

        if cur_loc is not None:
            cur_loc = int(cur_loc)
        else:
            cur_loc = 90  # Default to middle position if read fails
            print(
                f"Warning: Could not read servo {servo_index} position, using default")
            log_console(
                f"Warning: Could not read servo {servo_index + 1} position, using default")

        if g.servo_direction[servo_index] == 1:
            cur_loc += g.servo_speed[servo_index]
            print(f"Servo {servo_index} moving to {cur_loc} degrees clockwise")
            log_console(
                f"Servo {servo_index + 1} moving to {cur_loc}° clockwise")

        elif g.servo_direction[servo_index] == 2:
            cur_loc -= g.servo_speed[servo_index]
            print(
                f"Servo {servo_index} moving to {cur_loc} degrees counterclockwise")
            log_console(
                f"Servo {servo_index + 1} moving to {cur_loc}° counterclockwise")

        # Constrain servo position to 0-180 degrees
        cur_loc = max(0, min(cur_loc, 240))
        g.board.digital[g.servo_pins[servo_index]].write(cur_loc)

    except Exception as e:
        print(f"Unable to write to servo {servo_index}: {e}")
        log_console(f"Error: Unable to write to servo {servo_index + 1}: {e}")


def runServoLoop():
    """Main servo control loop"""
    while True:
        if g.exit_flag:
            print("Servo thread stopped")
            break

        for i in range(len(g.servo_pins)):
            if g.servo_direction[i] != 0:  # Only move if direction is set
                moveServo(i)

        time.sleep(0.01)  # Small delay to prevent overwhelming the Arduino


def moveToPositionSmooth(servo_index, target_pos, delay=0.1):
    """Move servo smoothly to a specific position"""
    try:
        cur_pos = g.board.digital[g.servo_pins[servo_index]].read()
        if cur_pos is None:
            cur_pos = 90  # Default position
        else:
            cur_pos = int(cur_pos)

        if cur_pos > target_pos:
            for pos in range(cur_pos, target_pos, -1):
                g.board.digital[g.servo_pins[servo_index]].write(pos)
                print(f"Moving servo {servo_index} to position {pos}")
                time.sleep(delay)
        elif cur_pos < target_pos:
            for pos in range(cur_pos, target_pos, 1):
                g.board.digital[g.servo_pins[servo_index]].write(pos)
                print(f"Moving servo {servo_index} to position {pos}")
                time.sleep(delay)

        print(f"Servo {servo_index} reached target position {target_pos}")

    except Exception as e:
        print(
            f"Error moving servo {servo_index} to position {target_pos}: {e}")


def initializeServos():
    """Initialize all servo positions to default values"""
    try:
        for i, pin in enumerate(g.servo_pins):
            g.board.digital[pin].mode = g.board.SERVO
            g.board.digital[pin].write(
                g.servo_default_positions[i])

            print(
                f"Servo {i} (pin {pin}) initialized to {g.servo_default_positions[i]} degrees")

        print("All servo pins initialized successfully!")
        return True
    except Exception as e:
        print(f"Error initializing servos: {e}")
        return False


def setServoToHome():
    """Move all servos to home position"""
    print("Moving all servos to home position...")
    for i, home_pos in enumerate(g.servo_default_positions):
        moveToPositionSmooth(i, home_pos)
    print("All servos at home position")
