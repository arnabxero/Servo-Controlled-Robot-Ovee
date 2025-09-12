import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
from collections import deque
import g


class RealtimeGraphs:
    def __init__(self, parent_widget):
        self.parent = parent_widget

        # Data storage (keep last 50 points for better performance)
        self.max_points = 50
        self.time_data = deque(maxlen=self.max_points)
        self.sensor_data = deque(maxlen=self.max_points)
        self.diameter_data = deque(maxlen=self.max_points)

        # Create the figure with subplots - smaller and simpler
        self.fig = Figure(figsize=(4.2, 7.5), dpi=70, facecolor='white')
        self.fig.subplots_adjust(hspace=0.5, left=0.2,
                                 right=0.9, top=0.9, bottom=0.15)

        # Create subplots
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)

        # Setup axes
        self.setup_axes()

        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.canvas.get_tk_widget().place(x=13, y=57, width=335, height=258)

        # Start time reference
        self.start_time = time.time()

        # Control flags
        self.running = True
        self.update_counter = 0

        # Start update thread (much slower updates)
        self.update_thread = threading.Thread(
            target=self.update_loop, daemon=True)
        self.update_thread.start()

    def setup_axes(self):
        # Sensor subplot
        self.ax1.set_title('Sensor Value', fontsize=9)
        self.ax1.set_ylabel('V', fontsize=8)
        self.ax1.tick_params(labelsize=7)
        self.ax1.grid(True, alpha=0.3, linewidth=0.5)

        # Grasper gap subplot
        self.ax2.set_title('Grasper Gap', fontsize=9)
        self.ax2.set_xlabel('Time (s)', fontsize=8)
        self.ax2.set_ylabel('mm', fontsize=8)
        self.ax2.tick_params(labelsize=7)
        self.ax2.grid(True, alpha=0.3, linewidth=0.5)

    def update_loop(self):
        """Separate thread for updating graphs - much slower than GUI"""
        while self.running:
            try:
                # Only update every 2 seconds to reduce lag
                time.sleep(2.0)

                # Get current data
                current_time = time.time() - self.start_time
                sensor_value = getattr(g, 'sensor_value', 0.0)
                diameter_mm = getattr(g, 'diameter_in_mm', 0.0)

                # Add data points
                self.time_data.append(current_time)
                self.sensor_data.append(sensor_value)
                self.diameter_data.append(diameter_mm)

                # Update plots (only if we have data)
                if len(self.time_data) > 1:
                    # Clear and replot (simple but effective)
                    self.ax1.clear()
                    self.ax2.clear()

                    # Replot data
                    self.ax1.plot(list(self.time_data), list(
                        self.sensor_data), 'b-', linewidth=1.5)
                    self.ax2.plot(list(self.time_data), list(
                        self.diameter_data), 'g-', linewidth=1.5)

                    # Reset titles and labels after clear
                    self.ax1.set_title('Sensor Value', fontsize=9)
                    self.ax1.set_ylabel('V', fontsize=8)
                    self.ax1.grid(True, alpha=0.3, linewidth=0.5)
                    self.ax1.tick_params(labelsize=7)

                    self.ax2.set_title('Grasper Gap', fontsize=9)
                    self.ax2.set_xlabel('Time (s)', fontsize=8)
                    self.ax2.set_ylabel('mm', fontsize=8)
                    self.ax2.grid(True, alpha=0.3, linewidth=0.5)
                    self.ax2.tick_params(labelsize=7)

                    # Simple auto-scaling
                    if len(self.time_data) > 0:
                        time_min, time_max = min(
                            self.time_data), max(self.time_data)
                        time_range = time_max - time_min
                        if time_range > 30:  # Show last 30 seconds
                            self.ax1.set_xlim(time_max - 30, time_max + 1)
                            self.ax2.set_xlim(time_max - 30, time_max + 1)
                        else:
                            self.ax1.set_xlim(time_min - 1, time_max + 1)
                            self.ax2.set_xlim(time_min - 1, time_max + 1)

                    # Redraw canvas (less frequently)
                    try:
                        self.canvas.draw_idle()  # Use draw_idle instead of draw
                    except:
                        pass  # Ignore drawing errors

            except Exception as e:
                print(f"Graph update error: {e}")
                continue

    def clear_data(self):
        """Clear all graph data"""
        self.time_data.clear()
        self.sensor_data.clear()
        self.diameter_data.clear()
        self.start_time = time.time()

        # Clear the plots
        try:
            self.ax1.clear()
            self.ax2.clear()
            self.setup_axes()
            self.canvas.draw_idle()
        except:
            pass

        print("Graph data cleared")

    def stop(self):
        """Stop the update thread"""
        self.running = False


def create_graphs(parent_widget):
    """Factory function to create and return graphs instance"""
    return RealtimeGraphs(parent_widget)
