# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_owasp_top_10(driver):
    driver.get("https://owasp.org/www-project-top-ten/")
    links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/Top10/A"]')
    return [
        {"name": link.text.strip(), "url": link.get_attribute("href")}
        for link in links
        if link.text.startswith("A0") and "Top10" in link.get_attribute("href")
    ]

def main():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        data = scrape_owasp_top_10(driver)
    except Exception as e:
        print(f"Error: {type(e).__name__} - {e}")
        data = []
    finally:
        driver.quit()

    df = pd.DataFrame(data).drop_duplicates().reset_index(drop=True)
    df.to_csv("owasp_top_10.csv", index=False)
    print(df.head(10))

if __name__ == "__main__":
    main()

# %%
