import psutil
import datetime
from collections import defaultdict
import tkinter as tk
from tkinter import simpledialog, scrolledtext

def gather_system_info():
    # CPU 信息
    logical_cpu_count = psutil.cpu_count()
    physical_cpu_count = psutil.cpu_count(logical=False)
    cpu_percentages = psutil.cpu_percent(interval=0.5, percpu=True)
    cpu_freq = psutil.cpu_freq()
    
    # 記憶體信息
    virtual_memory = psutil.virtual_memory()
    
    # 硬碟信息
    disk_partitions = psutil.disk_partitions()
    
    # 網路信息
    net_io_counters = psutil.net_io_counters()
    net_if_addrs = psutil.net_if_addrs()
    
    # 將連線按類型分組
    net_connections = psutil.net_connections()
    connections_by_type = defaultdict(list)
    for conn in net_connections:
        connections_by_type[conn.type].append(conn)
    
    # 登錄用戶信息
    users = psutil.users()
    
    # 系統啟動時間
    boot_time = psutil.boot_time()
    boot_time_hr = datetime.datetime.fromtimestamp(boot_time)
    
    # 構建系統信息
    info = []
    info.append("CPU 信息")
    info.append(f"邏輯 CPU 數量: {logical_cpu_count}")
    info.append(f"實際物理 CPU 數量: {physical_cpu_count}")
    info.append(f"每個 CPU 的使用率: {cpu_percentages}")
    info.append(f"CPU 使用頻率: {cpu_freq}")
    info.append("\n記憶體信息")
    info.append(f"{virtual_memory}")
    info.append("\n硬碟信息")
    for partition in disk_partitions:
        info.append(f"{partition}")
    info.append("\n網路信息")
    info.append(f"網路 I/O 封包: {net_io_counters}")
    info.append("網路卡的組態資訊:")
    for interface, addrs in net_if_addrs.items():
        info.append(f"{interface}: {addrs}")
    info.append("\n目前機器的網路連線:")
    for conn_type, conns in connections_by_type.items():
        info.append(f"連線類型: {conn_type}")
        for conn in conns:
            info.append(f"本地地址: {conn.laddr}")
            info.append(f"遠端地址: {conn.raddr}")
            info.append(f"狀態: {conn.status}")
            info.append(f"PID: {conn.pid}")
            info.append("")
    info.append("\n登錄用戶信息:")
    for user in users:
        info.append(f"{user}")
    info.append("\n系統啟動時間")
    info.append(f"系統啟動時間 (timestamp): {boot_time}")
    info.append(f"系統啟動時間 (human-readable): {boot_time_hr}")

    return "\n".join(info)

def show_system_info():
    # 創建一個新的 Tkinter 視窗來顯示系統信息
    info_window = tk.Toplevel(root)
    info_window.title("System Information")
    
    # 設定視窗的大小
    info_window.geometry("600x400")
    
    # 創建一個滾動文本框顯示系統信息
    text_area = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, bg='#f0f0f0', fg='black')
    text_area.pack(expand=True, fill=tk.BOTH)
    
    # 獲取系統信息並顯示
    system_info = gather_system_info()
    text_area.insert(tk.INSERT, system_info)
    text_area.config(state=tk.DISABLED)  # 設為只讀模式

def login():
    # 獲取帳號和密碼
    accountnumber = account_entry.get()
    password = password_entry.get()

    # 驗證密碼
    if accountnumber != "s0119378":  # 替換成實際的預期帳號
        print("帳號錯誤，無法查看系統信息。")
    elif password != "s01193781106":  # 替換成實際的預期密碼
        print("密碼錯誤，無法查看系統信息。")
    else:
        # 如果帳號和密碼都正確，則在這裡繼續執行您的程式碼
        # 呼叫副程式
        show_system_info()
        root.destroy()  # 關閉主視窗

def clear_entries():
    # 清除帳號和密碼輸入框中的內容
    account_entry.delete(0, 'end')
    password_entry.delete(0, 'end')
    
# 創建一個新的 Tkinter 視窗
root = tk.Tk()

# 為視窗設定標題
root.title("System Hardware Information Gathering")

# 設定視窗的大小
root.geometry("400x240")

# 設定視窗的背景顏色
root.config(bg='#00fff0')  # 淺灰色背景

# 創建帳號和密碼的標籤和輸入框
account_label = tk.Label(root, text="帳號", bg='#00fff0')
account_label.grid(row=0, column=0)
account_entry = tk.Entry(root, show='*')
account_entry.grid(row=0, column=1)

password_label = tk.Label(root, text="密碼", bg='#00fff0')
password_label.grid(row=1, column=0)
password_entry = tk.Entry(root, show='*')
password_entry.grid(row=1, column=1)

# 創建一個登錄按鈕
login_button = tk.Button(root, text="登錄", command=login)
login_button.grid(row=2, column=0)

# 創建一個關閉按鈕
close_button = tk.Button(root, text="關閉", command=root.destroy)
close_button.grid(row=2, column=1)

# 創建一個清除按鈕
clear_button = tk.Button(root, text="清除", command=clear_entries)
clear_button.grid(row=2, column=2)

# 設定按鈕的大小
login_button.config(height=2, width=15)
close_button.config(height=2, width=15)
clear_button.config(height=2, width=15)

# 運行視窗
root.mainloop()
