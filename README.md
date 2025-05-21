# Tracking Law Enforcement Support Office (LESO) Police Data

This repository automates the process of downloading public information related to law enforcement agencies from the **Law Enforcement Support Office (LESO)** website. The scraper  downloads all available Excel files from the [LESO Public Information page](https://www.dla.mil/Disposition-Services/Offers/Law-Enforcement/Public-Information/).

The scraper runs monthly and saves the downloaded files in directories named by the date they were retrieved. 

## Purpose

Although some of this data can be accessed through the Internet Archive, using it can be difficult and is not a permanent solution. This tool was created to ensure continuous tracking of this data, as it is overwritten every quarter. It is crucial to track the weapons that law enforcement agencies are receiving and holding through military surplus programs.


## File Structure

`.github/workflows/run_scripts.yaml`: GitHub Actions workflow file used for automating the execution of the scraper script.
`scraper.py`: Python script responsible for scraping data from the DLA website and downloading Excel files.
`downloads/`: Directory where the Excel files are downloaded, categorized by the date the files were retrieved.
`README.md`: This file.

## Source
