import g
import os
import re
import pyfirmata
import platform

system = platform.system()


def boardSetup():
    ######################## Arduino Setup ########################
    lines = []

    if system == "Darwin":
        print("Mac OS Detected, finding ports")
        try:
            output = os.popen('ls /dev/tty.*').read()
            for substr in output.split('\n'):
                substr2 = re.sub('\x1b\[[0-9;]*m', '', substr)
                if substr2.strip():  # Only add non-empty lines
                    lines.append(substr2.strip())
                    print(substr2)
        except Exception as e:
            print(f"Error finding ports on macOS: {e}")

    elif system == "Windows":
        print("Windows Detected, finding ports")
        try:
            # Method 1: Try PowerShell command
            output = os.popen(
                'powershell "Get-WmiObject -Class Win32_SerialPort | Select-Object DeviceID"').read()

            if not output.strip() or "Get-WmiObject" in output:
                # Method 2: Fallback to mode command
                print("Trying alternative port detection method...")
                output = os.popen('mode').read()
                import re
                com_ports = re.findall(r'(COM\d+)', output)
                for port in com_ports:
                    lines.append(port)
                    print(port)
            else:
                # Parse PowerShell output
                for line in output.split('\n'):
                    if 'COM' in line and line.strip():
                        # Extract just the COM port part
                        com_match = re.search(r'COM\d+', line)
                        if com_match:
                            port = com_match.group()
                            lines.append(port)
                            print(port)

        except Exception as e:
            print(f"Error finding ports on Windows: {e}")

        # Method 3: If no ports found, try common COM ports manually
        if not lines:
            print("No ports detected, testing common COM ports...")
            common_ports = ['COM1', 'COM2', 'COM3', 'COM4',
                            'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10']
            for port in common_ports:
                try:
                    # Quick test if port is available
                    test_board = pyfirmata.Arduino(port)
                    test_board.exit()
                    lines.append(port)
                    print(f"Found working port: {port}")
                    break
                except:
                    continue

    else:
        print("Unknown operating system, trying Unix-style detection")
        try:
            output = os.popen('ls /dev/tty.*').read()
            for substr in output.split('\n'):
                substr2 = re.sub('\x1b\[[0-9;]*m', '', substr)
                if substr2.strip():
                    lines.append(substr2.strip())
                    print(substr2)
        except Exception as e:
            print(f"Error finding ports: {e}")

    # Check if we found any ports
    if not lines:
        print("ERROR: No Arduino ports found!")
        print("Please check your Arduino connection and try again.")
        print("Make sure Arduino IDE can detect your device.")
        return False  # Return False to indicate failure

    # Find default port (prefer USB ports on Mac/Linux, first COM port on Windows)
    def_index = 0
    for i, line in enumerate(lines):
        if system == "Windows":
            # On Windows, just use the first COM port found
            def_index = i
            break
        elif "usb" in line.lower():
            # On Mac/Linux, prefer USB ports
            def_index = i
            break

    default_port_name = lines[def_index]
    print(f"Selected Port: {default_port_name}")

    try:
        print(f"Attempting to connect to Arduino on {default_port_name}...")
        g.board = pyfirmata.Arduino(default_port_name)
        it = pyfirmata.util.Iterator(g.board)
        it.start()

        # Give it a moment to initialize
        import time
        time.sleep(1)

        # Setup sensor and switch pins
        g.sensor = g.board.get_pin('a:2:i')  # Analog pin 2 for sensor
        g.stop_switch_pin = g.board.get_pin(
            'd:4:i')  # Digital pin 4 for stop switch

        # Setup servo pins
        setupServos()

        print("Arduino connected successfully!")
        print("Sensor pin: A2")
        print("Stop switch pin: D4")
        print(f"Servo pins: {g.servo_pins}")
        return True  # Return True to indicate success

    except Exception as e:
        print(f"Arduino connection failed: {e}")
        print("Please check:")
        print("- Arduino is properly connected")
        print("- Correct drivers are installed")
        print("- Port is not being used by another application")
        print("- Arduino IDE can connect to the device")
        return False

    ######################## Arduino Setup ########################


def setupServos():
    """Initialize servo pins and set them to default positions"""
    try:
        for i, pin in enumerate(g.servo_pins):
            g.board.digital[pin].mode = pyfirmata.SERVO
            g.board.digital[pin].write(
                g.servo_default_positions[i])
            print(
                f"Servo {i} (pin {pin}) initialized to {g.servo_default_positions[i]} degrees")
        print("All servo pins initialized successfully!")
        return True
    except Exception as e:
        print(f"Error setting up servo pins: {e}")
        return False


def test_connection():
    """Test function to verify Arduino connection and sensor readings"""
    if not boardSetup():
        return

    print("\nTesting sensor readings and servo positions...")
    print("Press Ctrl+C to stop")

    try:
        import time
        for i in range(50):  # Test for 5 seconds
            sensor_value = g.sensor.read() if g.sensor else None
            switch_value = g.stop_switch_pin.read() if g.stop_switch_pin else None

            print(f"Sensor (A2): {sensor_value:.4f if sensor_value else 'None'} | "
                  f"Switch (D4): {switch_value}")

            # Test servo positions
            servo_positions = []
            for j, pin in enumerate(g.servo_pins):
                try:
                    pos = g.board.digital[pin].read()
                    servo_positions.append(f"S{j}: {pos if pos else 'None'}")
                except:
                    servo_positions.append(f"S{j}: Error")

            print(f"Servos: {' | '.join(servo_positions)}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        try:
            if hasattr(g, 'board') and g.board:
                g.board.exit()
                print("Arduino connection closed")
        except:
            pass


if __name__ == "__main__":
    # Run test when script is executed directly
    test_connection()
