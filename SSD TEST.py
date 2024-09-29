import os
import time
import numpy as np

# 配置
FILE_SIZE_MB = 2000         # 測試文件大小 2 GB
FILE_NAME = 'test_file.tmp'  # 測試文件名稱
BLOCK_SIZE_KB = 16         # 隨機測試時的塊大小 (KB)
NUM_BLOCKS = 10000         # 隨機測試時的塊數量

def write_test_file(file_name, size_mb):
    """寫入測試文件"""
    with open(file_name, 'wb') as f:
        f.write(os.urandom(size_mb * 1024 * 1024))

def read_test_file(file_name):
    """讀取測試文件"""
    with open(file_name, 'rb') as f:
        f.read()

def sequential_read_write_test(file_name, size_mb):
    """順序讀寫性能測試"""
    start_time = time.perf_counter()
    
    # 寫入測試
    with open(file_name, 'wb') as f:
        f.write(os.urandom(size_mb * 1024 * 1024))
    write_time = time.perf_counter() - start_time
    write_speed = size_mb / write_time
    print(f'Sequential Write Speed: {write_speed:.2f} MB/s')
    
    start_time = time.perf_counter()
    
    # 讀取測試
    with open(file_name, 'rb') as f:
        f.read()
    read_time = time.perf_counter() - start_time
    read_speed = size_mb / read_time
    print(f'Sequential Read Speed: {read_speed:.2f} MB/s')

def random_read_write_test(file_name, block_size_kb, num_blocks):
    """隨機讀寫性能測試"""
    block_size = block_size_kb * 1024
    data = os.urandom(block_size)
    
    # 隨機寫入測試
    start_time = time.perf_counter()
    with open(file_name, 'r+b') as f:
        for _ in range(num_blocks):
            position = np.random.randint(0, FILE_SIZE_MB * 1024 * 1024 - block_size)
            f.seek(position)
            f.write(data)
    write_time = time.perf_counter() - start_time
    if write_time == 0:  # 防止除以零錯誤
        print('Error: Write time is zero.')
        return
    write_speed = (block_size_kb * num_blocks) / write_time / 1024
    print(f'Random Write Speed: {write_speed:.2f} MB/s')
    
    # 隨機讀取測試
    start_time = time.perf_counter()
    with open(file_name, 'rb') as f:
        for _ in range(num_blocks):
            position = np.random.randint(0, FILE_SIZE_MB * 1024 * 1024 - block_size)
            f.seek(position)
            f.read(block_size)
    read_time = time.perf_counter() - start_time
    if read_time == 0:  # 防止除以零錯誤
        print('Error: Read time is zero.')
        return
    read_speed = (block_size_kb * num_blocks) / read_time / 1024
    print(f'Random Read Speed: {read_speed:.2f} MB/s')

def verify_data(file_name, block_size_kb, num_blocks):
    """驗證數據"""
    block_size = block_size_kb * 1024
    data = os.urandom(block_size)
    
    with open(file_name, 'r+b') as f:
        for _ in range(num_blocks):
            position = np.random.randint(0, FILE_SIZE_MB * 1024 * 1024 - block_size)
            f.seek(position)
            f.write(data)
    
    with open(file_name, 'rb') as f:
        for _ in range(num_blocks):
            position = np.random.randint(0, FILE_SIZE_MB * 1024 * 1024 - block_size)
            f.seek(position)
            read_data = f.read(block_size)
            if read_data != data:
                print('Data verification failed.')
                return
    print('Data verification successful.')

def main():
    print('Starting SSD Performance Test...')
    
    # 確保開始時有乾淨的狀態
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)
    
    # 順序讀寫測試
    print('Sequential Read/Write Test:')
    sequential_read_write_test(FILE_NAME, FILE_SIZE_MB)
    
    # 在隨機讀寫測試之前驗證數據
    verify_data(FILE_NAME, BLOCK_SIZE_KB, NUM_BLOCKS)
    
    # 隨機讀寫測試
    print('\nRandom Read/Write Test:')
    random_read_write_test(FILE_NAME, BLOCK_SIZE_KB, NUM_BLOCKS)
    
    # 清理
    os.remove(FILE_NAME)

if __name__ == "__main__":
    main()
