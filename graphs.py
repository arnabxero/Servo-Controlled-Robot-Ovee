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
        self.pressure_data = deque(maxlen=self.max_points)
        self.deformation_data = deque(maxlen=self.max_points)
        self.slope_data = deque(maxlen=self.max_points)

        # Create the figure with subplots - using configurable DPI from g.py
        self.fig = Figure(figsize=(4.2, 7.5),
                          dpi=g.graph_dpi, facecolor='white')
        self.fig.subplots_adjust(hspace=0.5, left=0.2,
                                 right=0.8, top=0.9, bottom=0.15)

        # Create subplots
        self.ax1 = self.fig.add_subplot(211)
        self.ax1_secondary = self.ax1.twinx()  # Secondary y-axis for deformation
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

        # Print current DPI setting for user reference
        print(f"Graph initialized with DPI: {g.graph_dpi}")

    def setup_axes(self):
        # Pressure/Deformation subplot
        self.ax1.set_title('Pressure & Deformation', fontsize=9)
        self.ax1.set_ylabel('Pressure (kPa)', fontsize=8, color='blue')
        self.ax1.tick_params(axis='y', labelcolor='blue', labelsize=7)
        # Add this line for x-axis ticks
        self.ax1.tick_params(axis='x', labelsize=7)
        self.ax1.grid(True, alpha=0.3, linewidth=0.5)

        # Secondary y-axis for deformation (positioned on right side)
        self.ax1_secondary.set_ylabel(
            'Deformation (mm)', fontsize=8, color='red')
        self.ax1_secondary.tick_params(axis='y', labelcolor='red', labelsize=7)
        self.ax1_secondary.yaxis.set_label_position('right')
        self.ax1_secondary.yaxis.tick_right()

        # Slope subplot
        self.ax2.set_title('Pressure vs √Deformation Slope', fontsize=9)
        self.ax2.set_xlabel('Time (s)', fontsize=8)
        self.ax2.set_ylabel('Slope', fontsize=8)
        self.ax2.tick_params(labelsize=7)
        self.ax2.grid(True, alpha=0.3, linewidth=0.5)

    def update_graph_resolution(self, new_dpi):
        """Update the graph resolution dynamically"""
        try:
            # Update the global variable
            g.graph_dpi = new_dpi

            # Recreate the figure with new DPI
            old_fig = self.fig
            self.fig = Figure(figsize=(4.2, 7.5),
                              dpi=new_dpi, facecolor='white')
            self.fig.subplots_adjust(hspace=0.5, left=0.2,
                                     right=0.8, top=0.9, bottom=0.15)

            # Recreate subplots
            self.ax1 = self.fig.add_subplot(211)
            self.ax1_secondary = self.ax1.twinx()
            self.ax2 = self.fig.add_subplot(212)

            # Setup axes again
            self.setup_axes()

            # Update the canvas
            self.canvas.figure = self.fig
            self.canvas.draw()

            print(f"Graph resolution updated to DPI: {new_dpi}")

        except Exception as e:
            print(f"Error updating graph resolution: {e}")

    def update_loop(self):
        """Separate thread for updating graphs - much slower than GUI"""
        while self.running:
            try:
                # Only update every 2 seconds to reduce lag
                time.sleep(g.graph_update_delay)

                # Get current data
                current_time = time.time() - self.start_time
                pressure = getattr(g, 'delta_pressure', 0.0)

                # Get deformation from the entry widget (same as what's displayed)
                try:
                    deformation_text = g.deformation_mm_entry.get()
                    deformation = float(
                        deformation_text) if deformation_text else 0.0
                except:
                    deformation = 0.0

                slope = getattr(g, 'pressure_slope', 0.0)

                # Add data points
                self.time_data.append(current_time)
                self.pressure_data.append(pressure)
                self.deformation_data.append(deformation)
                self.slope_data.append(slope)

                # Update plots (only if we have data)
                if len(self.time_data) > 1:
                    # Clear and replot
                    self.ax1.clear()
                    self.ax1_secondary.clear()
                    self.ax2.clear()

                    # Plot pressure on primary y-axis
                    line1 = self.ax1.plot(list(self.time_data), list(
                        self.pressure_data), 'b-', linewidth=1.5, label='Pressure')

                    # Plot deformation on secondary y-axis
                    line2 = self.ax1_secondary.plot(list(self.time_data), list(
                        self.deformation_data), 'r-', linewidth=1.5, label='Deformation')

                    # Plot slope
                    self.ax2.plot(list(self.time_data), list(
                        self.slope_data), 'g-', linewidth=1.5)

                    # Reset titles and labels after clear
                    self.ax1.set_title('Pressure & Deformation', fontsize=9)
                    self.ax1.set_ylabel(
                        'Pressure (kPa)', fontsize=8, color='blue')
                    self.ax1.tick_params(
                        axis='y', labelcolor='blue', labelsize=7)
                    # Add this line for x-axis ticks
                    self.ax1.tick_params(axis='x', labelsize=7)
                    self.ax1.grid(True, alpha=0.3, linewidth=0.5)

                    # Secondary y-axis for deformation (positioned on right side)
                    self.ax1_secondary.set_ylabel(
                        'Deformation (mm)', fontsize=8, color='red')
                    self.ax1_secondary.tick_params(
                        axis='y', labelcolor='red', labelsize=7)
                    self.ax1_secondary.yaxis.set_label_position('right')
                    self.ax1_secondary.yaxis.tick_right()

                    self.ax2.set_title(
                        'Pressure vs √Deformation Slope', fontsize=9)
                    self.ax2.set_xlabel('Time (s)', fontsize=8)
                    self.ax2.set_ylabel('Slope', fontsize=8)
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

                    # Redraw canvas
                    try:
                        self.canvas.draw_idle()
                    except:
                        pass

            except Exception as e:
                print(f"Graph update error: {e}")
                continue

    def clear_data(self):
        """Clear all graph data"""
        self.time_data.clear()
        self.pressure_data.clear()
        self.deformation_data.clear()
        self.slope_data.clear()
        self.start_time = time.time()

        # Clear the plots
        try:
            self.ax1.clear()
            self.ax1_secondary.clear()
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


def set_graph_resolution(dpi_value):
    """Utility function to change graph resolution on the fly"""
    try:
        g.graph_dpi = int(dpi_value)
        print(f"Graph DPI setting changed to: {g.graph_dpi}")
        print("Note: Changes will take effect when graphs are recreated or application is restarted")
        return True
    except ValueError:
        print(
            f"Invalid DPI value: {dpi_value}. Please use a number (e.g., 70, 100, 150, 200)")
        return False
