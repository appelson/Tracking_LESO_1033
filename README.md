# Tracking Law Enforcement Support Office (LESO) 1033 Data

This repository automates the process of downloading public information related to military equipment owned by law enforcement agencies from the **Law Enforcement Support Office (LESO)** website. The scraper downloads all available Excel files from the [LESO Public Information page](https://www.dla.mil/Disposition-Services/Offers/Law-Enforcement/Public-Information/).

The scraper runs on the 10th day of every month and saves the downloaded files in directories named by the date they were retrieved. 

## Purpose

Although some of this data can be accessed through the Internet Archive, this is not a permanent solution. This tool was created to ensure continuous tracking of LESO data, as it is overwritten every quarter. 

## File Structure
- `.github/workflows/run_scripts.yaml`: GitHub Actions workflow file used for automating the execution of the scraper script.
- `scraper.py`: Python script responsible for scraping data from the DLA website and downloading Excel files using Selenium.
- `downloads/`: Directory where the Excel files are downloaded.
- `README.md`: This file.

## Source
The code written is directly influenced by “Jsoma/Selenium-Github-Actions.” GitHub, 2025, [github.com/jsoma/selenium-github-actions](github.com/jsoma/selenium-github-actions).
