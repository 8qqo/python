import urllib.request as req
import bs4

def getData(url):
    # Create a Request object and attach Request Headers information
    request = req.Request(url, headers={
        "cookie": "over18=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    
    # Parse the source code (HTML) and obtain the title
    root = bs4.BeautifulSoup(data, "html.parser")
    titles = root.find_all("div", class_="title")  # Find all div tags with class="title"
    
    title_list = []
    for title in titles:
        if title.a is not None:  # If the title contains a tag (not removed), print it
            print(title.a.string)
            title_list.append(title.a.string)
    
    nextLink = root.find("a", string="‹ 上頁")
    return (nextLink["href"] if nextLink else None, title_list)

pageurl = "https://www.ptt.cc/bbs/Gossiping/index.html"
count = 0
all_titles = []
while count < 5:
    next_page, titles = getData(pageurl)
    if next_page is not None:
        pageurl = "https://www.ptt.cc" + next_page
        all_titles.extend(titles)
        print(pageurl)
        count += 1
    else:
        break

#Save the captured titles to a file
with open("webcrawler-titles.txt", "w", encoding="utf-8") as file:
    for title in all_titles:
        file.write(title + "\n")

