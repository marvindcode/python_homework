# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import csv
import json

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    driver.get("https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart")

    title = driver.title
    print("Page Title:", title)

    body = driver.find_element(By.CSS_SELECTOR, "body")  
    if not body:
        print("No <body> found.")
        exit()

    book_lists = body.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")

    results = []

    for book in book_lists:
        try:
            title = book.find_element(By.CLASS_NAME, "title-content").text
        except:
            title = "N/A"
        
        try:
            authors = book.find_elements(By.CLASS_NAME, "author-link")
            author_names = "; ".join([a.text for a in authors])
        except:
            author_names = "N/A"

        try:
            format_div = book.find_element(By.CLASS_NAME, "cp-format-info")
            format_year = format_div.find_element(By.TAG_NAME, "span").text
        except:
            format_year = "N/A"

        results.append({
            "Title": title,
            "Author": author_names,
            "Format-Year": format_year
        })

    df = pd.DataFrame(results)
    print(df.head())

    df.to_csv("get_books.csv", index=False)

    with open('get_books.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)

except Exception as e:
        print("Can't get the web page")

finally:
    driver.quit()

# %%


# %%
