# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

# Set options for the Chrome webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Disable automation controls
options.add_experimental_option("useAutomationExtension", False)  # Disable use of automation extensions
driver = webdriver.Chrome(options=options)  # Initialize the Chrome webdriver with the set options

# Target URL for web scraping (this is for red wines, for the whites just change the target url)
target_url = 'https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1VctNrLA1NTBQS6609QxRS7Z1DQ1SKwDKpqfZliUWZaaWJOao5Rel2KrlJ1XaqpWXRMcCJZMri4F0ZgkANXkXVQ%3D%3D'
driver.maximize_window()  # Maximize the browser window
driver.get(target_url)  # Open the target URL

time.sleep(1 + random.random())  # Pause the execution for a random time

# Scroll pause time with a random element
SCROLL_PAUSE_TIME = 2 + (random.random() - 0.5)

# Get the current height of the page
last_height = driver.execute_script("return document.body.scrollHeight")

pages = []  # Initialize an empty list to store URLs

# Scroll through the page and collect URLs until no new URLs are found
while True:
    # Scroll halfway down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    time.sleep(5)  # Pause the execution for 5 seconds
    
    # Get the new height of the page after scrolling
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    # If the new height equals the last height, break the loop
    if new_height == last_height:
        break
    last_height = new_height

    # CSS selector for the URLs
    urls_selector = '--3F_uB'
    # Find all elements matching the CSS selector
    urls = driver.find_elements(By.CSS_SELECTOR, 'a.wineCard__cardLink' + urls_selector)

    # For each URL, if it's not already in the list, add it
    for url in urls:
        if len(pages) == 10000:  # If we have collected 10,000 URLs, break the loop
            break
        if url.get_attribute('href') not in pages:
            pages.append(url.get_attribute('href'))

    if len(pages) == 10000:  # If we have collected 10,000 URLs, break the loop
        break

    print(len(pages))  # Print the current number of collected URLs

# Close the browser
driver.quit()

# Open a file to store the URLs
fin = open('red_wines_urls.txt', 'w') # for the whites, white_wines_urls.txt

# Write each URL to the file
for page in pages:
    fin.write(page)
    fin.write('\n')

# Close the file
fin.close()