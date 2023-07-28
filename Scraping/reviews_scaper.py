"""
Scraping script for reviews
"""

# Import of necessary libraries

from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import csv
import re
import time
import random
from spacy_langdetect import LanguageDetector
import spacy
from spacy.language import Language

# Custom factory for spacy language detector
@Language.factory('language_detector')
def language_detector(nlp, name):
    return LanguageDetector()

# Load language models for English and Italian
eng = spacy.load('en_core_web_sm')
ita = spacy.load('it_core_news_sm')

# Add language detector pipe to the models
eng.add_pipe('language_detector', last=True)
ita.add_pipe('language_detector', last=True)

# Selenium Chrome options
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument('--window-size=1920,1080')

# Read the list of pages to scrape
pages_doc = open('red_wines_urls_clean.txt', 'r')
page_list = [page for page in pages_doc]
pages_doc.close()

# Open CSV file to write reviews
rev_csv = open('red_reviews.csv', 'a', encoding='ascii', errors='ignore')
csvwriter = csv.writer(rev_csv, delimiter=';', lineterminator="\n", quoting=csv.QUOTE_ALL)

# Get starting point from user
start_from = input('Start from: ')
vine_counter = int(start_from)

# Loop through each page
for target_url in page_list[int(start_from) - 1:]:
    t1 = time.time()
    driver = webdriver.Chrome(options=options)
    driver.get(target_url)  # Open the page

    time.sleep(1 + random.random())  # Wait for a random time between 1 and 2 seconds

    SCROLL_PAUSE_TIME = 2 + (random.random() - 0.5)  # Random time between 1.5 and 2.5 seconds
    last_height = driver.execute_script("return document.body.scrollHeight")  # Get page height

    # Scroll down the page until its height doesn't change anymore (i.e., it's fully loaded)
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(document.body.scrollHeight/3, document.body.scrollHeight*2/3);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(document.body.scrollHeight*2/3, document.body.scrollHeight);")
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height
    
    # Click the button to show reviews
    driver.find_element(By.CSS_SELECTOR,
                        "#all_reviews button[class='MuiButtonBase-root MuiButton-root jss1 MuiButton-outlined jss3 MuiButton-disableElevation']").click()

    time.sleep(3)

    # Scroll down the reviews
    for i in range(30):
        driver.find_element(By.CSS_SELECTOR,
                            'a._3qc2M.reviewAnchor__anchor--2NKFw.communityReview__reviewContent--3xA5s').send_keys(
            Keys.PAGE_DOWN)

    time.sleep(3)

    # Find all reviews
    reviews = driver.find_elements(By.CSS_SELECTOR, "div.communityReviewItem__reviewCard--1RupJ")
    for element in reviews[:-1]:
        text = element.find_element(By.XPATH, '// *[ @ id = "baseModal"] / div / div[2] / div[3] / div / div / div[1] / div[1] / a / span').text

        if not text:
            continue

        rate = element.find_element(By.CSS_SELECTOR, 'span.userRating__ratingNumber--1SGVL').text
        
        info = element.find_element(By.CSS_SELECTOR, 'div.communityReview__textInfo--7SzS6').text
        
        likes_comms = element.find_element(By.CSS_SELECTOR, 'div.communityReview__userActions--2RDK9').text.split()

        if not likes_comms:
            continue

        try:
            year = element.find_element(By.CSS_SELECTOR,
                                        'span.reviewedVintageYear__vintageText--3TZOW.communityReview__vintageText--vW6OI').text
        except:
            year = 0

        # Write review data to CSV
        csvwriter.writerow(
            [target_url, info, rate, likes_comms[0], likes_comms[1], year, eng(text)._.language['language'], text])
    t2 = time.time()
    print(vine_counter, ' done: ', round(t2 - t1), 's')
    vine_counter += 1

    driver.quit()

rev_csv.close()