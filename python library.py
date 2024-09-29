import requests
from bs4 import BeautifulSoup

url = "https://docs.python.org/zh-tw/3/library/index.html"

# 發送HTTP請求並取得網頁內容
response = requests.get(url)

# 確認是否成功取得網頁內容
if response.status_code == 200:
    # 使用Beautiful Soup解析HTML內容
    soup = BeautifulSoup(response.content, "html.parser")
    
    # 找到標準函式庫的內容區域
    library_content = soup.find("div", {"class": "toctree-wrapper compound"})
    
    # 如果找到內容，則寫入到文件
    if library_content:
        with open("python_library_index.txt", "w", encoding="utf-8") as file:
            file.write(library_content.get_text())
        print("標準函式庫的內容已成功寫入到 python_library_index.txt 文件中。")
    else:
        print("未能找到標準函式庫的內容。")
else:
    print("無法取得網頁內容，錯誤碼：", response.status_code)
