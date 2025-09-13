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
        # Command Log Widget (Last Command Log panel)
        self.command_widget = scrolledtext.ScrolledText(
            parent_canvas.master,
            height=12,
            width=28,
            bg="#FFFAD0",
            fg="#333333",
            font=("Consolas", 8),
            wrap=tk.WORD
        )
        self.command_widget.place(x=716, y=80, width=227, height=225)

        # Console Widget (Console panel)
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

        # Start the update thread
        self.start_update_thread()

    def log_command(self, command):
        """Add a command to the command log"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_command = f"[{timestamp}] {command}"
        self.command_queue.put(formatted_command)

    def log_console(self, message):
        """Add a message to the console"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        formatted_message = f"[{timestamp}] {message}"
        self.console_queue.put(formatted_message)

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

                            # Keep only last 50 commands
                            lines = self.command_widget.get(
                                "1.0", tk.END).split('\n')
                            if len(lines) > 51:  # 50 + 1 for the extra newline
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
    """Convenience function to log commands"""
    logger.log_command(command)


def log_console(message):
    """Convenience function to log console messages"""
    logger.log_console(message)
