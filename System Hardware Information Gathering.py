import psutil
import datetime
from collections import defaultdict
import getpass  # 新增的模組

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
    
    # 將結果寫入到 txt 檔案
    with open('system_info.txt', 'w', encoding='utf-8') as f:
        f.write("CPU 信息\n")
        f.write(f"邏輯 CPU 數量: {logical_cpu_count}\n")
        f.write(f"實際物理 CPU 數量: {physical_cpu_count}\n")
        f.write(f"每個 CPU 的使用率: {cpu_percentages}\n")
        f.write(f"CPU 使用頻率: {cpu_freq}\n")
        f.write("\n記憶體信息\n")
        f.write(f"{virtual_memory}\n")
        f.write("\n硬碟信息\n")
        for partition in disk_partitions:
            f.write(f"{partition}\n")
        f.write("\n網路信息\n")
        f.write(f"網路 I/O 封包: {net_io_counters}\n")
        f.write("網路卡的組態資訊:\n")
        for interface, addrs in net_if_addrs.items():
            f.write(f"{interface}: {addrs}\n")
        f.write("\n目前機器的網路連線:\n")
        for conn_type, conns in connections_by_type.items():
            f.write(f"連線類型: {conn_type}\n")
            for conn in conns:
                f.write(f"本地地址: {conn.laddr}\n")
                f.write(f"遠端地址: {conn.raddr}\n")
                f.write(f"狀態: {conn.status}\n")
                f.write(f"PID: {conn.pid}\n")
                f.write("\n")
        f.write("\n登錄用戶信息:\n")
        for user in users:
            f.write(f"{user}\n")
        f.write("\n系統啟動時間\n")
        f.write(f"系統啟動時間 (timestamp): {boot_time}\n")
        f.write(f"系統啟動時間 (human-readable): {boot_time_hr}\n")
    
    print("系統信息已寫入到 system_info.txt 檔案中")


# 獲取用戶密碼
accountnumber = getpass.getpass("請輸入帳號以查看系統信息: ")
password = getpass.getpass("請輸入密碼以查看系統信息: ")

# 驗證密碼（這裡可以根據實際情況加入更複雜的驗證邏輯）
if accountnumber != "s0119378":  # 替換成實際的預期帳號
    print("帳號錯誤，無法查看系統信息。")
    exit()
elif password != "s01193781106":  # 替換成實際的預期密碼
    print("密碼錯誤，無法查看系統信息。")
    exit()
else:
    # 如果帳號和密碼都正確，則在這裡繼續執行您的程式碼
    # 呼叫副程式
    gather_system_info()
    pass

