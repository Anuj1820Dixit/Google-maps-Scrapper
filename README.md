# 🗺️ Google Maps Business Scraper

A Python-based web scraping tool that extracts business contact information from **Google Maps** search results. This script uses **Selenium WebDriver**, supports **auto-restart after crashes**, and can **resume progress from the last scraped page**. Additionally, it attempts to fetch business emails by crawling their official websites.

---

## 📌 Features

- 🔍 Scrapes:
  - Business Name
  - Contact Number
  - Address
  - Website
  - Email (via website crawling)
- 🔁 Resumes from last saved page if interrupted
- 💾 Tracks completed queries and avoids repetition
- 🧠 Recovers from WebDriver crashes automatically
- 🗂️ Exports results as Excel files (one per keyword)
- 📜 Logs activity to `GMB_city_extraction.log`

---

## 🛠️ Technologies Used

- Python 3.x
- Selenium
- Pandas
- Requests
- WebDriver Manager
- OpenPyXL

---

## 📂 Folder Structure

📁 project_root/
│
├── Input.xlsx # Excel file containing the list of keywords in "Input" column
├── Output/ # Folder where results are saved as individual Excel files
├── progress.json # Tracks the last scraped page per query
├── completed_queries.txt # Tracks completed keywords
├── GMB_city_extraction.log # Log file for monitoring
└── scraper.py # Main script


---

## ✅ Requirements

Install dependencies via:

```bash
pip install -r requirements.txt
```
Example requirements.txt:
selenium
pandas
requests
webdriver-manager
openpyxl


🚀 How to Use
Prepare Input:
Create an Excel file named Input.xlsx with a sheet containing a column titled Input. Each row should contain a Google Maps search keyword (e.g., cafes in Mumbai, plumbers in Bangalore).

Run the Script:
```
python scraper.py
```
Output:
Results will be saved inside the Output/ directory as separate Excel files for each search keyword.

🔄 Auto-Resume & Crash Recovery
The script automatically saves your scraping progress and resumes from where it left off.

If the WebDriver crashes, it restarts and continues without data loss.

📧 Email Extraction Logic
If a business website is available, the script fetches the page and attempts to extract visible email addresses using regex patterns.

📓 Logging
All scraping activity is recorded in GMB_city_extraction.log.

📌 Example Output
Each output file includes:

ID	Company_Name	Contact_Number	Email	Ratings	Reviews	Address	Website
-------------------------------------------------------------------------------------
1	ABC Cafe	+91-9876543210	hello@abccafe.com			Bandra, Mumbai	www.abccafe.com

⚠️ Disclaimer
This tool is intended for educational and research purposes only. Web scraping Google Maps may violate their Terms of Service, and excessive automated access may result in temporary IP bans.

Use responsibly and ensure compliance with local data protection laws.

🙌 Acknowledgements
Selenium
WebDriver Manager
Google Maps
