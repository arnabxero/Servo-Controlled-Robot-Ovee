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
        output = os.popen('ls /dev/tty.*').read()
    elif system == "Windows":
        print("Windows Detected, finding ports")
        output = os.popen('wmic path Win32_SerialPort').read()
    else:
        print("Unknown operating system")

    output = os.popen('ls /dev/tty.*').read()

    for substr in output.split('\n'):
        substr2 = re.sub('\x1b\[[0-9;]*m', '', substr)
        lines.append(substr2)
        print(substr2)
    lines.pop()

    def_index = 0
    for i, line in enumerate(lines):
        if "usb" in line:
            def_index = i
            break

    default_port_name = lines[def_index]
    print("Default Port: " + default_port_name)

    try:
        g.board = pyfirmata.Arduino(default_port_name)
        it = pyfirmata.util.Iterator(g.board)
        it.start()
        # Analog 2 pin is sensor pin
        g.sensor = g.board.get_pin('a:2:i')
        g.stop_switch_pin = g.board.get_pin('d:5:i')

    except:
        # tk.messagebox.showerror('Arduino Selection error', 'Arduino not found')
        print("Arduino Not Found")

    try:
        g.board.digital[g.gripper_pin].mode = pyfirmata.SERVO
        g.board.digital[g.gripper_pin].write(20)
    except:
        print("Unable to set digital pins for output")

    ######################## Arduino Setup ########################
