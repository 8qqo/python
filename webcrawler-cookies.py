#抓取PTT原始碼(HTML)
import urllib.request as req
def getData(url):
#建立一個Request物件、附加Request Headers的資訊
    request=req.Request(url,headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
            data=response.read().decode("utf-8")
    #print(data)
    #解析原始碼(HTML)，取得標題
    import bs4
    root=bs4.BeautifulSoup(data,"html.parser")
    #print(root.title)
    titles=root.find_all("div",class_="title")#尋找所有class="title"的div標籤
    #print(titles)
    for title in titles:
        if title.a !=None:#如果標題包含a標籤(沒有被刪除).印出來
            print(title.a.string)
    nextLink= root.find("a", string="‹ 上頁")
    return (nextLink["href"])

pageurl="https://www.ptt.cc/bbs/Gossiping/index.html"
count=0
while count<5:
    pageurl="https://www.ptt.cc"+getData(pageurl)
    print(pageurl)
    count+=1

        