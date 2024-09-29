import urllib.request as req
import bs4

# Wikipedia URL for Intel CPU list
url = "https://en.wikipedia.org/wiki/List_of_Intel_processors"

# Create a Request object with headers
request = req.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
})

# Send the request and get the response
with req.urlopen(request) as response:
    data = response.read().decode("utf-8")

# Parse the HTML
root = bs4.BeautifulSoup(data, "html.parser")

# Find the target table
table = root.find("table", class_="wikitable")

# Extract and save the data if the table is found
if table:
    rows = table.find_all("tr")
    
    # Extract headers
    headers = [header.get_text(strip=True) for header in rows[0].find_all("th")]

    # Open a file to write the data
    with open("intel_processors.txt", "w", encoding="utf-8") as file:
        # Write the headers to the file
        file.write("\t".join(headers) + "\n")
        
        # Extract and write the data rows
        for row in rows[1:]:  # Skip the header row
            cells = row.find_all("td")
            cell_texts = [cell.get_text(strip=True) for cell in cells]
            file.write("\t".join(cell_texts) + "\n")
    
    print("Data written to intel_processors.txt successfully.")
else:
    print("Target table not found")