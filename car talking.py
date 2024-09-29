from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 設定 Chrome 選項
chrome_options = Options()
chrome_options.add_extension('path/to/adblock_plus.crx')  # 替換為 Adblock Plus 擴充功能的路徑

# 初始化 WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 打開 Speedtest 網頁
driver.get('https://www.speedtest.net/zh-Hant')

# 你的其他操作...

