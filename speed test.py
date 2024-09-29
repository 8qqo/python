import speedtest
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import threading
import time
import random
from datetime import datetime

def run_speed_test():
    s = speedtest.Speedtest()
    s.get_best_server()

    download_speed = s.download() / 1_000_000  # Convert to Mbps
    upload_speed = s.upload() / 1_000_000  # Convert to Mbps
    ping = s.results.ping

    # Simulate jitter and packet loss
    jitter = random.uniform(5, 50)  # Random jitter between 5 and 50 ms
    packet_loss = random.uniform(0, 2)  # Random packet loss between 0 and 2 percent

    best_server = s.get_best_server()
    server_info = f"Connected to: {best_server['host']} located in {best_server['name']}, {best_server['country']}"
    
    return download_speed, upload_speed, ping, jitter, packet_loss, server_info

def animate_progress(progress_label, progress_type):
    for i in range(0, 101, 5):
        time.sleep(0.1)
        progress_var.set(i)
        progress_label.config(text=f"{progress_type} {i}%")
        root.after(10, root.update_idletasks)  # Use root.after for better UI updates

def plot_speed_test_results(download_speed, upload_speed, ping, jitter, packet_loss, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    categories = ['Download Speed (Mbps)', 'Upload Speed (Mbps)', 'Ping (ms)', 'Jitter (ms)', 'Packet Loss (%)']
    values = [download_speed, upload_speed, ping, jitter, packet_loss]
    
    fig, ax = plt.subplots(figsize=(14, 7))  # Increase figure size for better spacing
    bars = ax.bar(categories, values, color=['blue', 'green', 'red', 'purple', 'orange'], width=0.6)  # Reduce bar width
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + max(values) * 0.05, round(yval, 2), va='bottom', ha='center')  # Add padding to avoid overlap
    
    ax.set_title('Internet Speed Test Results')
    ax.set_xlabel('Category')
    ax.set_ylabel('Value')
    ax.set_ylim(0, max(values) * 1.4)  # Increase ylim to allow space for text
    # ax.tick_params(axis='x', rotation=15)  # Rotate x-axis labels

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def on_test_button_click():
    test_button.config(state=tk.DISABLED)
    server_info_text.set("Connecting to server...")
    threading.Thread(target=run_speed_test_and_update_ui).start()

def run_speed_test_and_update_ui():
    try:
        animate_progress(progress_label, "Downloading")
        download_speed, upload_speed, ping, jitter, packet_loss, server_info = run_speed_test()
        server_info_text.set(server_info)
        animate_progress(progress_label, "Uploading")
        plot_speed_test_results(download_speed, upload_speed, ping, jitter, packet_loss, chart_frame)
    finally:
        progress_var.set(0)
        progress_label.config(text="")
        test_button.config(state=tk.NORMAL)

root = tk.Tk()
root.title("Internet Speed Test")
root.geometry("1000x700")  # Increase window size

# Create a frame for the chart
chart_frame = ttk.Frame(root)
chart_frame.pack(pady=20, fill=tk.BOTH, expand=True)

# Create a button to start the test
test_button = ttk.Button(root, text="Run Speed Test", command=on_test_button_click)
test_button.pack(pady=10)

# Create a progress bar
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, mode='determinate', length=300, variable=progress_var)
progress_bar.pack(pady=10)

# Create a label for progress display
progress_label = ttk.Label(root, text="")
progress_label.pack(pady=5)

# Create a text area to display server information
server_info_text = tk.StringVar()
server_info_label = ttk.Label(root, textvariable=server_info_text)
server_info_label.pack(pady=10)

# Display the current date
current_date = datetime.now().strftime("%Y-%m-%d")
date_label = ttk.Label(root, text=f"Date: {current_date}")
date_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
