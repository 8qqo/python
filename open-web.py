import urllib.request as request
import json

src="https://data.taipei/api/v1/dataset/296acfa2-5d93-4706-ad58-e83cc951863c?scope=resourceAquire"

with request.urlopen(src) as response:
    data=json.load(response)
    clist=data["result"]["results"]

with open("data.txt","w",encoding="utf-8") as file:
    for company in clist:
        #print(company["公司名稱"]+"\n"+company["公司地址"])
        file.write(company["公司名稱"]+"\n")
        file.write(company["公司地址"]+"\n")
