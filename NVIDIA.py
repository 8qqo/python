import urllib.request as req
import bs4

# Wikipedia URL for NVIDIA GPU list
url = "https://en.wikipedia.org/wiki/List_of_Nvidia_graphics_processing_units"

# Create a Request object with headers
request = req.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
})

# Send the request and get the response
with req.urlopen(request) as response:
    data = response.read().decode("utf-8")

# Parse the HTML
root = bs4.BeautifulSoup(data, "html.parser")

# Find all tables with class 'wikitable'
tables = root.find_all("table", class_="wikitable")

# Extract GPU names
gpu_names = []
for table in tables:
    rows = table.find_all("tr")
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all("td")
        if len(cols) > 0:
            gpu_name = cols[0].text.strip()
            gpu_names.append(gpu_name)

# Print all extracted GPU names
for index, name in enumerate(gpu_names, start=1):
    print(f"{index}. {name}")

# Write GPU names to a text file
with open("nvidia_gpus.txt", "w", encoding="utf-8") as file:
    for index, name in enumerate(gpu_names, start=1):
        file.write(f"{index}. {name}\n")

print("GPU names have been written to nvidia_gpus.txt successfully.")
