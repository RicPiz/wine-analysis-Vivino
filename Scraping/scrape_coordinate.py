# Import necessary libraries
import csv
import urllib.request
from bs4 import BeautifulSoup
import re

# Read the list of URLs from a file
pages_doc = open('red_wines_urls_clean.txt', 'r')
page_list = [page for page in pages_doc]
pages_doc.close()

# Open the output CSV file and create a CSV writer
wines = open('coordinate_red_wines.csv', 'a')
winewriter = csv.writer(wines, delimiter=';', lineterminator="\n")
winewriter.writerow(['winemaker', 'latitude', 'longitude'])

# Ask the user where to start scraping from
start_from = input('Start from: ')
wine_counter = int(start_from)

# Iterate over each URL in the list
for target_url in page_list[int(start_from) - 1:]:
    # Open the target URL and read its content
    fp = urllib.request.urlopen(target_url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()

    try:
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(mystr, features="lxml")
        s = soup.find_all('script')

        # Find the script containing the coordinates
        pattern = re.compile('window.__PRELOADED_STATE__.vintagePageInformation = (.*);')
        coordinates = []
        for i in s:
            strObj = i.text
            match = pattern.search(strObj)
            if match:
                jsonString = strObj.split("window.__PRELOADED_STATE__.vintagePageInformation")[1].encode('utf8').decode('unicode_escape')
                location = re.search('"location":{"latitude":(.+?)}', jsonString).group()
                location = re.sub("[^\\d\\.]", ';', location)
                coordinates.append(location.split(';'))

        # Extract the latitude and longitude from the coordinates
        coordinates = [x for x in coordinates[0] if x]
        latitude = coordinates[0]
        longitude = coordinates[1]

        # Extract the winemaker name from the page
        winemaker = soup.find(attrs={'class': 'winery'}).text.strip()

        print(wine_counter)
        wine_counter += 1

        # Write the winemaker name and coordinates to the CSV file
        winewriter.writerow([winemaker, latitude, longitude])
    except:
        continue

wines.close()