A powerful Python scraper that extracts detailed business information from Google Maps using a list of search queries like "general contractors in Kansas". For each keyword, it creates a separate CSV file and automatically skips already processed keywords by referring to a tracking file.

📌 Features
✅ Batch Processing of search queries

🔄 Automatic Tracking of completed searches using completed_queries.txt

📥 Extracts comprehensive business details:

Company_Name

Contact_Number

Email (if available)

Ratings

Reviews

Address

Website

📁 Saves data in separate CSV files for each keyword

🧠 Notes
The scraper uses Selenium to automate Google Maps navigation.

Make sure ChromeDriver is correctly installed and version-matched to your Chrome.

Large keyword lists are supported; processed entries are skipped in future runs.

Some fields like email or website may not be available for all businesses.

🛡️ Disclaimer
This tool is built for educational and research purposes only. Scraping Google Maps may violate their Terms of Service. Use at your own discretion.
