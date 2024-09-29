import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ping3 import ping
import statistics
import time
import numpy as np
from scipy.interpolate import make_interp_spline

class PingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Test Application")

        self.label = tk.Label(root, text="Enter host to ping:")
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=5)
        
        # Create a slider to select test duration
        self.slider_label = tk.Label(root, text="Select test duration (seconds):")
        self.slider_label.pack(pady=10)
        
        self.test_duration = tk.IntVar(value=30)
        self.slider = tk.Scale(root, from_=1, to=60, orient=tk.HORIZONTAL, variable=self.test_duration, label="Seconds")
        self.slider.pack(pady=10)

        self.button = tk.Button(root, text="Start Ping Test", command=self.perform_ping)
        self.button.pack(pady=20)
        
        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.pack(pady=10)
        self.result_text.config(state=tk.DISABLED)

        # Add countdown timer label
        self.timer_label = tk.Label(root, text="Time Remaining: 00:00")
        self.timer_label.pack(pady=10)
        
        # Create a larger Figure and Axes for plotting
        self.figure = Figure(figsize=(10, 6), dpi=100)  # Increased size
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(pady=20, fill=tk.BOTH, expand=True)

        # Connect the motion event and figure leave event to their respective functions
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('figure_leave_event', self.on_mouse_leave)

        # Initialize variables for countdown and data
        self.latencies = []
        self.scatter = None
        self.annotation = None
        self.timer_running = False
        self.remaining_time = 0

    def perform_ping(self):
        host = self.entry.get()
        if not host:
            messagebox.showerror("Input Error", "Please enter a host.")
            return

        duration = self.test_duration.get()  # Get duration in seconds
        self.remaining_time = duration
        self.timer_running = True
        self.update_timer()

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        start_time = time.time()
        self.latencies = []

        while time.time() - start_time < duration:
            latency = ping(host)
            if latency is None:
                self.result_text.insert(tk.END, f"Ping to {host} failed.\n")
                self.result_text.config(state=tk.DISABLED)
                return
            self.latencies.append(latency * 1000)  # Convert to milliseconds
            time.sleep(1)  # Wait for 1 second between pings

        self.timer_running = False
        self.result_text.config(state=tk.NORMAL)
        if self.latencies:
            min_ping = min(self.latencies)
            avg_ping = statistics.mean(self.latencies)
            max_ping = max(self.latencies)
            mdev_ping = statistics.stdev(self.latencies) if len(self.latencies) > 1 else 0
            
            result = (
                f"Minimum Ping: {min_ping:.2f} ms\n"
                f"Average Ping: {avg_ping:.2f} ms\n"
                f"Maximum Ping: {max_ping:.2f} ms\n"
                f"Mean Deviation: {mdev_ping:.2f} ms\n"
            )
            
            self.result_text.insert(tk.END, result)
        else:
            self.result_text.insert(tk.END, "No pings were recorded.\n")
        
        self.result_text.config(state=tk.DISABLED)
        
        # Update plot
        self.plot_data(self.latencies)

    def update_timer(self):
        try:
            if self.timer_running:
                minutes, seconds = divmod(self.remaining_time, 60)
                self.timer_label.config(text=f"Time Remaining: {minutes:02}:{seconds:02}")
                self.root.update_idletasks()
                self.remaining_time -= 1
                if self.remaining_time >= 0:
                    self.root.after(1000, self.update_timer)
                else:
                    self.timer_label.config(text="Time's Up!")
        except Exception as e:
            print(f"Error updating timer: {e}")

    
    def plot_data(self, latencies):
        self.ax.clear()
        
        # Create a smooth line plot with circular markers
        x = np.arange(len(latencies))
        y = np.array(latencies)
        
        # Interpolation for smooth curve
        x_new = np.linspace(x.min(), x.max(), 300)
        spline = make_interp_spline(x, y, k=3)  # Cubic spline
        y_smooth = spline(x_new)
        
        # Plot smooth line with circular markers
        self.ax.plot(x_new, y_smooth, linestyle='-', color='b', alpha=0.7)
        self.scatter = self.ax.scatter(x, y, color='b', s=100, edgecolor='black', zorder=5)  # Increased marker size
        
        # Set title and labels
        self.ax.set_title('Ping Latency Over Time')
        self.ax.set_xlabel('Ping Attempt')
        self.ax.set_ylabel('Latency (ms)')
        
        # Adjust x-ticks to avoid clutter
        if len(latencies) > 10:
            self.ax.set_xticks(range(0, len(latencies), max(1, len(latencies)//10)))
        else:
            self.ax.set_xticks(range(len(latencies)))
        
        self.ax.set_xticklabels([str(i+1) for i in self.ax.get_xticks()])
        
        # Redraw the canvas
        self.canvas.draw()

    def on_mouse_move(self, event):
        if event.inaxes == self.ax:
            # Remove previous annotation if exists
            if self.annotation:
                self.annotation.remove()
                self.annotation = None

            # Find the index of the nearest data point
            x_data = self.scatter.get_offsets()[:, 0]
            y_data = self.scatter.get_offsets()[:, 1]
            distances = np.sqrt((x_data - event.xdata) ** 2 + (y_data - event.ydata) ** 2)
            nearest_idx = np.argmin(distances)
            
            # Add annotation for the nearest data point
            self.annotation = self.ax.annotate(f'{y_data[nearest_idx]:.2f} ms',
                                               (x_data[nearest_idx], y_data[nearest_idx]),
                                               xytext=(10, 10),
                                               textcoords='offset points',
                                               arrowprops=dict(facecolor='black', shrink=0.05),
                                               fontsize=10, color='black')
            self.canvas.draw()

    def on_mouse_leave(self, event):
        # Remove annotation when mouse leaves the figure
        if self.annotation:
            self.annotation.remove()
            self.annotation = None
            self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PingApp(root)
    root.mainloop()
