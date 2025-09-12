import pyfirmata
import time
import platform
import os
import re


def find_arduino_port():
    """Find Arduino port automatically"""
    system = platform.system()
    lines = []

    if system == "Darwin":  # macOS
        print("Mac OS Detected, finding ports")
        try:
            output = os.popen('ls /dev/tty.*').read()
            for substr in output.split('\n'):
                substr2 = re.sub('\x1b\[[0-9;]*m', '', substr)
                if substr2.strip() and 'usb' in substr2.lower():
                    lines.append(substr2.strip())
        except Exception as e:
            print(f"Error finding ports on macOS: {e}")

    elif system == "Windows":  # Windows
        print("Windows Detected, finding ports")
        try:
            output = os.popen(
                'powershell "Get-WmiObject -Class Win32_SerialPort | Select-Object DeviceID"').read()
            for line in output.split('\n'):
                if 'COM' in line and line.strip():
                    com_match = re.search(r'COM\d+', line)
                    if com_match:
                        port = com_match.group()
                        lines.append(port)
        except Exception as e:
            print(f"Error finding ports on Windows: {e}")

    else:  # Linux/Unix
        print("Unix-style system detected, finding ports")
        try:
            output = os.popen('ls /dev/tty.*').read()
            for substr in output.split('\n'):
                substr2 = re.sub('\x1b\[[0-9;]*m', '', substr)
                if substr2.strip() and ('USB' in substr2 or 'ACM' in substr2):
                    lines.append(substr2.strip())
        except Exception as e:
            print(f"Error finding ports: {e}")

    return lines[0] if lines else None


def test_stop_switch():
    """Test stop switch reading"""

    # Find Arduino port
    port = find_arduino_port()
    if not port:
        print("ERROR: No Arduino port found!")
        print("Please check your Arduino connection.")
        return

    print(f"Attempting to connect to Arduino on {port}...")

    try:
        # Connect to Arduino
        board = pyfirmata.Arduino(port)
        it = pyfirmata.util.Iterator(board)
        it.start()

        # Give it a moment to initialize
        time.sleep(2)

        # Setup stop switch pin (Digital pin 4 as per your code)
        stop_switch_pin = board.get_pin('d:4:i')  # Digital pin 4 for input

        print("Arduino connected successfully!")
        print("Stop switch pin: D4")
        print("Reading stop switch status...")
        print("Press Ctrl+C to stop\n")

        # Continuous reading loop
        while True:
            try:
                # Read the stop switch
                switch_value = stop_switch_pin.read()

                # Print status with timestamp
                timestamp = time.strftime("%H:%M:%S")

                if switch_value is None:
                    print(f"[{timestamp}] Stop Switch: None (reading failed)")
                elif switch_value == True or switch_value == 1:
                    print(f"[{timestamp}] Stop Switch: PRESSED (True/1) ✓")
                elif switch_value == False or switch_value == 0:
                    print(f"[{timestamp}] Stop Switch: NOT PRESSED (False/0)")
                else:
                    print(
                        f"[{timestamp}] Stop Switch: {switch_value} (unexpected value)")

                time.sleep(0.5)  # Read every 500ms

            except KeyboardInterrupt:
                print("\nTest stopped by user")
                break

    except Exception as e:
        print(f"Error connecting to Arduino: {e}")
        print("Please check:")
        print("- Arduino is properly connected")
        print("- Correct drivers are installed")
        print("- Port is not being used by another application")
        print("- Arduino IDE can connect to the device")

    finally:
        try:
            if 'board' in locals():
                board.exit()
                print("Arduino connection closed")
        except:
            pass


if __name__ == "__main__":
    print("=== Stop Switch Test Script ===")
    print("This script will continuously read and display the stop switch status.")
    print("Make sure your Arduino is connected and no other programs are using it.\n")

    test_stop_switch()
