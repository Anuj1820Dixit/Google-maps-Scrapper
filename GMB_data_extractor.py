import json
import os
import time
import random
import logging
import pandas as pd
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

import warnings
warnings.filterwarnings('ignore')

### 📌 File Paths for Saving Progress
progress_file = "progress.json"
completed_queries_file = "completed_queries.txt"


### 📌 Function to Restart ChromeDriver with a Small Window
def restart_driver(first_run=False):
    """Restarts ChromeDriver with a small window, only showing messages when it crashes."""
    try:
        driver.quit()  # Close existing session
    except:
        pass  

    chrome_driver_path = ChromeDriverManager().install()
    service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(800, 600)  # Set a small window size

    if not first_run:
        print("\n⚠️ WebDriver crashed. Restarting and resuming from last page...")

    return driver  # Return new driver instance


### 📌 Function to Extract Emails From Websites
def email_extractor(url):
    try:
        req = requests.get(re.sub(r"\s+", "", url), headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"},
            timeout=20)
        page_source = req.text
        EMAIL_REGEX = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
        list_of_emails = set(re.findall(EMAIL_REGEX, page_source))
        return list_of_emails if list_of_emails else ""
    except:
        return ""


### 📌 Function to Load & Save Progress (Last Page)
def load_progress():
    """Loads progress from the last saved page for each query."""
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            return json.load(f)  
    return {}  

def save_progress(query, page_number):
    """Saves the last page number for a given query."""
    progress = load_progress()
    progress[query] = page_number
    with open(progress_file, "w") as f:
        json.dump(progress, f)  


### 📌 Function to Track Completed Queries
def load_completed_queries():
    """Reads previously completed queries from the file or creates it if missing."""
    if not os.path.exists(completed_queries_file):
        with open(completed_queries_file, "w") as f:  
            pass  
    with open(completed_queries_file, "r") as f:
        return set(f.read().splitlines())  

def save_completed_query(query):
    """Saves a completed query to the file."""
    with open(completed_queries_file, "a") as f:
        f.write(query + "\n")  


### 📌 Function to Extract Business Details From Google Maps
def extract_details_from_map(keywords):
    logging.basicConfig(filename="GMB_city_extraction.log", format='%(asctime)s %(message)s', filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(keywords)

    data = pd.DataFrame(columns=['ID', 'Company_Name', 'Contact_Number', 'Email', 'Ratings', 'Reviews', 'Address', 'Website'])
    
    driver = restart_driver(first_run=True)  # First run without unnecessary messages

    progress = load_progress()  
    last_page = progress.get(keywords, 1)  

    driver.get(f"https://www.google.com/search?&tbm=lcl&q={keywords}&start={(last_page - 1) * 10}")
    
    # Only show "Resuming from Page X" if it’s not the first page
    if last_page > 1:
        print(f"\n🔍 Resuming: {keywords} from Page {last_page}")
    else:
        print(f"\n🔍 Searching: {keywords}")

    page_number = last_page  

    while True:
        try:
            print(f"📄 Page {page_number}")  # Show only page number

            companies = driver.find_elements(By.XPATH, "//div[@class='cXedhc']/a")

            for company in companies:
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", company)
                    company.click()
                    time.sleep(random.randint(5, 8))

                    Name = driver.find_element(By.XPATH, "//div[@class='SPZz6b']/h2").text if driver.find_elements(By.XPATH, "//div[@class='SPZz6b']/h2") else ""
                    Address_text = driver.find_elements(By.XPATH, "//div[@class='Z1hOCe']/div/span[2]")[0].text if driver.find_elements(By.XPATH, "//div[@class='Z1hOCe']/div/span[2]") else ""
                    Contact_text = driver.find_element(By.XPATH, "//div[@class='Z1hOCe']/div/span/span/a/span").text if driver.find_elements(By.XPATH, "//div[@class='Z1hOCe']/div/span/span/a/span") else ""
                    Website_text = driver.find_element(By.XPATH, "//div/a[@class='n1obkb mI8Pwc']").get_attribute('href') if driver.find_elements(By.XPATH, "//div/a[@class='n1obkb mI8Pwc']") else ""

                    email_id = email_extractor(Website_text) if Website_text else ""

                    details_dict = {
                        'Company_Name': [Name],
                        'Contact_Number': [Contact_text],
                        'Email': [", ".join(email_id)] if email_id else [""],
                        'Ratings': [""],
                        'Reviews': [""],
                        'Address': [Address_text],
                        'Website': [Website_text]
                    }
                    data = pd.concat([data, pd.DataFrame(details_dict)]).reset_index(drop=True)

                except WebDriverException:
                    print("\n⚠️ WebDriver session lost. Restarting and retrying the same query...")
                    driver = restart_driver()
                    return extract_details_from_map(keywords)  

            save_progress(keywords, page_number + 1)  

            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@id='pnnext']"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                next_button.click()
                page_number += 1
                time.sleep(random.randint(5, 10))
            except:
                print(f"✅ All pages completed for: {keywords}\n{'-'*50}")
                break  

        except:
            break  

    driver.quit()
    return data


### 📌 Main Execution: Read Input File & Process Queries
input_excel = pd.read_excel("Input.xlsx", engine="openpyxl")
completed_queries = load_completed_queries()

for keywords in input_excel["Input"]:
    if keywords in completed_queries:
        continue  

    dummy_data = extract_details_from_map(keywords)

    output_file = f"Output/{keywords}.xlsx"
    if os.path.exists(output_file):
        existing_data = pd.read_excel(output_file, engine="openpyxl")
        dummy_data = pd.concat([existing_data, dummy_data], ignore_index=True)

    dummy_data.to_excel(output_file, index=False)
    save_completed_query(keywords)

print("✅ Script completed successfully!")
