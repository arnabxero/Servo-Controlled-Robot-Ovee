import pyfirmata
import time

# Define the board and the pin
# Change this to your board's port
board = pyfirmata.Arduino('COM7')
pin = 8

# Attach the servo to pin 8. The 'i' stands for 'input'.
# PyFirmata needs to know the pin is for servo control
board.digital[pin].mode = pyfirmata.SERVO

# Main loop to sweep the servo
while True:
    # Sweep from 0 to 180 degrees
    for angle in range(0, 181):
        board.digital[pin].write(angle)
        time.sleep(0.015)  # Pause for 15 milliseconds

    # Sweep from 180 to 0 degrees
    for angle in range(180, -1, -1):
        board.digital[pin].write(angle)
        time.sleep(0.015)  # Pause for 15 milliseconds
