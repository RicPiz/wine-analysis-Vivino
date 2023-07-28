"""
Web scraping program for the project
"""

# Import necessary libraries
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
import random

# Set options for the Chrome webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Disable automation controls
options.add_experimental_option("useAutomationExtension", False)  # Disable use of automation extensions

# Read the list of URLs from a file
pages_doc = open('red_wines_urls_clean.txt', 'r')
page_list = [page for page in pages_doc]
pages_doc.close()

# Open the output CSV file and create a CSV writer
vini = open('red_wines.csv', 'a')
vinewriter = csv.writer(vini, delimiter=';', lineterminator="\n")

# Ask the user where to start scraping from
start_from = input('Start from: ') #30
vine_counter = int(start_from)

# Iterate over each URL in the list
for target_url in page_list[int(start_from)-1:]:
    t1 = time.time()

    time.sleep(4 + random.random()*3)

    # Start the Chrome webdriver and open the target URL
    driver = webdriver.Chrome(options=options)
    driver.get(target_url)

    time.sleep(1 + random.random())

    # Scroll through the page
    SCROLL_PAUSE_TIME = 2 + (random.random() - 0.5)
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Keep scrolling until no more content is loaded
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        driver.execute_script("window.scrollTo(document.body.scrollHeight/3, 2*document.body.scrollHeight/3);")
        driver.execute_script("window.scrollTo(2*document.body.scrollHeight/3, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Try to scrape the desired data from the page, providing default values in case of errors
    try:
        headline = driver.find_element(By.CSS_SELECTOR, 'span.headline').text
    except:
        headline = 'na'

    try:
        name = driver.find_element(By.CSS_SELECTOR, 'span.vintage').text
    except:
        name = 'na'

    avg_review_selector = '_19ZcA' 
    try:
        avg_review = driver.find_element(By.CSS_SELECTOR, 'div.' + avg_review_selector).text
    except:
        avg_review = 'na'

    num_review_selector = '_1_k5A'
    try:
        num_review = driver.find_element(By.CSS_SELECTOR, 'div.' + num_review_selector).text
        num_review = num_review.replace(',', '.') 
    except:
        num_review = 'na'

    breads_selector = '--2pkcX'
    try:
        breads = driver.find_element(By.CSS_SELECTOR, 'div.breadCrumbs__breadCrumbs' + breads_selector).text
    except:
        breads = 'na'

    price_selector = '--3mO4u'
    try:
        price = driver.find_element(By.CSS_SELECTOR, 'span.purchaseAvailability__currentPrice' + price_selector).text
    except:
        price = 'na'
    taste_selector = '--3aXLX'
    taste_structures = driver.find_elements(By.CSS_SELECTOR, 'span.indicatorBar__progress' + taste_selector)
    taste_names = driver.find_elements(By.CSS_SELECTOR, 'tr.tasteStructure__tasteCharacteristic--1rMFl')

    level_structure = []
    for element_name, element in zip(taste_names, taste_structures):
        en = element_name.text.replace('\n', '-')
        el = element.get_attribute('style').replace('width: 15%; left: ', '').strip(';')
        level_structure.append((en, el))

    try:
        c1 = driver.find_element(By.XPATH, '//*[@id="wine-page-lower-section"]/div[1]/div/div[3]/div/div[3]/div/a[1]/div[2]')
        c2 = driver.find_element(By.XPATH, '//*[@id="wine-page-lower-section"]/div[1]/div/div[3]/div/div[3]/div/a[2]/div[2]')
        c3 = driver.find_element(By.XPATH, '//*[@id="wine-page-lower-section"]/div[1]/div/div[3]/div/div[3]/div/a[3]/div[2]')
        food_advice = c1.text + ' / ' + c2.text + ' / ' + c3.text
    except:
        food_advice = 'na / na / na'

    note_selector = '--3J0at'
    try:
        nota = driver.find_elements(By.CSS_SELECTOR, 'span.tasteNote__flavorGroup' + note_selector)
    except:
        nota = 'na'

    mentions_selector = '--1Hjv0'
    mentions = driver.find_elements(By.CSS_SELECTOR, 'div.tasteNote__mentions' + mentions_selector)

    n_m = []
    counter = 0
    for n, m in zip(nota, mentions):
        if counter == 3:
            break
        m = [int(d) for d in m.text.split() if d.isdigit()]
        n_m.append((n.text, m[0]))
        counter += 1
    try:
        img = driver.find_element(By.CSS_SELECTOR, 'picture.bottleShot img')
        src = img.get_attribute('src')
        urlretrieve(src, "images/"+name+"'.png")
    except:
        print('no image found')

    # Write the scraped data to the CSV file
    try:
        vinewriter.writerow([headline, name, avg_review, num_review, breads, price, level_structure, food_advice, n_m])
        t2 = time.time()
        print(vine_counter, ' done: ', round(t2-t1), 's')
    except:
        print(vine_counter, 'cannot be done, skipping')

    vine_counter += 1
    driver.quit()

vini.close()
