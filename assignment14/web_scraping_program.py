from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#Setting Chrome setup
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

#Scrapping World Series History
driver.get("https://www.baseball-almanac.com/ws/wsmenu.shtml")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table.boxed"))
)

history_table = driver.find_element(By.CSS_SELECTOR, "table.boxed")
history_rows = history_table.find_elements(By.TAG_NAME, "tr")

history_data = []
for row in history_rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 5:
        year = cols[0].text.strip().split()[0]  
        history_data.append([
            year,
            cols[1].text.strip(),
            cols[2].text.strip(),
            cols[3].text.strip(),
            cols[4].text.strip()
        ])

history_df = pd.DataFrame(history_data, columns=[
    "Year", "National League", "NL Wins", "American League", "AL Wins"
])
history_df.to_csv("world_series_history.csv", index=False)


#Scrapping World Series Receipts
driver.get("https://www.baseball-almanac.com/ws/wsshares.shtml")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table.boxed"))
)

receipts_table = driver.find_element(By.CSS_SELECTOR, "table.boxed")
receipts_rows = receipts_table.find_elements(By.TAG_NAME, "tr")

receipts_data = []
for row in receipts_rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) == 7:  
        try:
            year = cols[0].find_element(By.TAG_NAME, "a").text.strip()
        except:
            year = cols[0].text.strip()

        receipts_data.append([
            year,
            cols[1].text.strip(),
            cols[2].text.strip(),
            cols[3].text.strip(),
            cols[4].text.strip(),
            cols[5].text.strip(),
            cols[6].text.strip()
        ])

receipts_df = pd.DataFrame(receipts_data, columns=[
    "Year", "Games", "Attendance", "Gate Receipts",
    "Players' Total", "Winners", "Losers"
])
receipts_df.to_csv("world_series_receipts.csv", index=False)

driver.quit()

#No pagination required, each dataset is in one page.

