# Importing packages
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Base URL
url = 'https://www.dla.mil/Disposition-Services/Offers/Law-Enforcement/Public-Information/'

# Creating a download directory
download_dir = os.path.join(os.getcwd(), 'downloads')
os.makedirs(download_dir, exist_ok=True)

# Setting up headless Chromium driver with necessary options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_dir,
    'download.prompt_for_download': False,
    'directory_upgrade': True
})

# Initializing the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Opening the page and parsing content
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Finding all Excel file links
xlsx_links = [link['href'] for link in soup.find_all('a', href=True) if '.xlsx' in link['href']]

# Downloading Excel files
for link in xlsx_links:
    driver.get("https://www.dla.mil" + link)
    while any(file.endswith('.crdownload') for file in os.listdir(download_dir)):
        time.sleep(3)
    print(f"Download completed: {'https://www.dla.mil'+link}")

# Closing the driver
driver.quit()
