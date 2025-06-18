# Importing Packages
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pandas as pd
import requests
import time
import os

# Loading CSV of links
df = pd.read_csv("links.csv")

# Getting links and jails
links = df["roster_url"].tolist()
jails = df["parish_jails"].tolist()

# Getting list of working links
valid_links = []

for link in links:
    try:
        response = requests.head(link, timeout=20)
        if response.status_code == 200:
            valid_links.append(link)
    except Exception as e:
        print("Error")

# Defining the `scrape_parish` function
def scrape_parish(url):
  
    # Setting the options for the scraper
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-gpu')
    
    # Defining the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Waiting 10 seconds 
    wait = WebDriverWait(driver, 10)

    # Getting the URL
    try:
        driver.get(url)

        # Clicking `lbShowAll`
        try:
            show_all_link = wait.until(EC.element_to_be_clickable((By.ID, "lbShowAll")))
            show_all_link.click()
            time.sleep(10)

        except Exception:
            pass

        # Parsing content
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", id="gvRoster")

        if table:
            df = pd.read_html(str(table))[0]
            df["Source URL"] = url
            df["Scraped At"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return df
        else:
            return None

    except Exception as e:
        return None
    finally:
        driver.quit()

# Defining results
results = []
max_workers = 5

# Scraping using a `ThreadPoolExecutor` with 5 workers
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(scrape_parish, url) for url in valid_links]

    for future in as_completed(futures):
        result_df = future.result()
        if result_df is not None:
            results.append(result_df)

# Combining results into a single dataframe
if results:
    combined_df = pd.concat(results, ignore_index=True)
else:
    print("None")

# Cleaning data
combined_df['roster_url'] = combined_df['Source URL']
data = pd.merge(combined_df, df, on='roster_url', how='left')
data_subset = data[['parish_jails', 'Name', 'DOB', 'Race', 'Gender', 'Arrest Date', 'Source URL', 'Scraped At']].copy()
data_subset.rename(columns=lambda x: x.strip().lower().replace(' ', '_'), inplace=True)

# Creating a folder
try:
  os.mkdir("raw")
except OSError as e:
  print("already exists")

# Saving results
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"raw/jailed_pop_{timestamp}.csv"
data_subset.to_csv(filename, index=False)
