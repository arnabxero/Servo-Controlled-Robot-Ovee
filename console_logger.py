import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
import datetime


class ConsoleLogger:
    def __init__(self):
        self.command_queue = queue.Queue()
        self.console_queue = queue.Queue()
        self.command_widget = None
        self.console_widget = None

    def setup_widgets(self, parent_canvas):
        """Setup the command log and console text widgets"""
        # Command Log Widget (Last Command Log panel) - Human readable actions
        self.command_widget = scrolledtext.ScrolledText(
            parent_canvas.master,
            height=12,
            width=28,
            bg="#FFFAD0",
            fg="#333333",
            font=("Arial", 9),  # Changed to more readable font
            wrap=tk.WORD
        )
        self.command_widget.place(x=716, y=80, width=227, height=225)

        # Console Widget (Console panel) - Technical messages
        self.console_widget = scrolledtext.ScrolledText(
            parent_canvas.master,
            height=25,
            width=32,
            bg="#DCFFD0",
            fg="#333333",
            font=("Consolas", 8),
            wrap=tk.WORD
        )
        self.console_widget.place(x=949, y=80, width=248, height=585)

        # Add initial welcome message
        self.log_command("System initialized successfully")

        # Start the update thread
        self.start_update_thread()

    def log_command(self, command):
        """Add a human-readable command to the command log"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_command = f"[{timestamp}] {command}"
        self.command_queue.put(formatted_command)

    def log_console(self, message):
        """Add a technical message to the console"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        formatted_message = f"[{timestamp}] {message}"
        self.console_queue.put(formatted_message)

    # Human-readable command logging methods
    def log_button_press(self, button_name):
        """Log when a button is pressed"""
        self.log_command(f"Button pressed: {button_name}")

    def log_servo_movement(self, servo_number, direction):
        """Log servo movement in human terms"""
        direction_map = {
            0: "stopped",
            1: "moving clockwise",
            2: "moving counterclockwise"
        }
        action = direction_map.get(direction, f"direction {direction}")
        self.log_command(f"Servo {servo_number} {action}")

    def log_gripper_action(self, action):
        """Log gripper actions"""
        self.log_command(f"Gripper {action}")

    def log_value_change(self, parameter_name, old_value, new_value):
        """Log when a parameter value changes"""
        self.log_command(
            f"Changed {parameter_name}: {old_value} → {new_value}")

    def log_setting_change(self, setting_name, new_value):
        """Log when a setting is changed"""
        self.log_command(f"Updated {setting_name} to {new_value}")

    def log_calibration_event(self, event):
        """Log calibration events"""
        self.log_command(f"Calibration: {event}")

    def log_data_action(self, action):
        """Log data-related actions"""
        self.log_command(f"Data: {action}")

    def log_system_event(self, event):
        """Log system events"""
        self.log_command(f"System: {event}")

    def start_update_thread(self):
        """Start the thread that updates the GUI widgets"""
        def update_widgets():
            while True:
                try:
                    # Update command log
                    while not self.command_queue.empty():
                        command = self.command_queue.get_nowait()
                        if self.command_widget:
                            self.command_widget.insert(tk.END, command + "\n")
                            self.command_widget.see(tk.END)

                            # Keep only last 30 commands for readability
                            lines = self.command_widget.get(
                                "1.0", tk.END).split('\n')
                            if len(lines) > 31:  # 30 + 1 for the extra newline
                                self.command_widget.delete("1.0", "2.0")

                    # Update console
                    while not self.console_queue.empty():
                        message = self.console_queue.get_nowait()
                        if self.console_widget:
                            self.console_widget.insert(tk.END, message + "\n")
                            self.console_widget.see(tk.END)

                            # Keep only last 100 console messages
                            lines = self.console_widget.get(
                                "1.0", tk.END).split('\n')
                            if len(lines) > 101:  # 100 + 1 for the extra newline
                                self.console_widget.delete("1.0", "2.0")

                except queue.Empty:
                    pass
                except:
                    pass

                # Small delay to prevent high CPU usage
                threading.Event().wait(0.1)

        update_thread = threading.Thread(target=update_widgets, daemon=True)
        update_thread.start()


# Global logger instance
logger = ConsoleLogger()


def log_command(command):
    """Convenience function to log human-readable commands"""
    logger.log_command(command)


def log_console(message):
    """Convenience function to log technical console messages"""
    logger.log_console(message)


# New convenience functions for specific types of logging
def log_button_press(button_name):
    """Log button press with human-readable name"""
    logger.log_button_press(button_name)


def log_servo_movement(servo_number, direction):
    """Log servo movement"""
    logger.log_servo_movement(servo_number, direction)


def log_gripper_action(action):
    """Log gripper action"""
    logger.log_gripper_action(action)


def log_value_change(parameter_name, old_value, new_value):
    """Log parameter value changes"""
    logger.log_value_change(parameter_name, old_value, new_value)


def log_setting_change(setting_name, new_value):
    """Log setting changes"""
    logger.log_setting_change(setting_name, new_value)


def log_calibration_event(event):
    """Log calibration events"""
    logger.log_calibration_event(event)


def log_data_action(action):
    """Log data actions"""
    logger.log_data_action(action)


def log_system_event(event):
    """Log system events"""
    logger.log_system_event(event)
