# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://owasp.org/www-project-top-ten/")

vulnerabilities_10 = driver.find_elements(By.XPATH, '//a[starts-with(@href, "/Top10/A0")]')

results = []
for vuln in vulnerabilities_10:
    title = vuln.text.strip()
    href = vuln.get_attribute('href')
    if title and href:
        results.append({"Title": title, "Link": href})

driver.quit()

df = pd.DataFrame(results)
df.to_csv("owasp_top_10.csv", index=False)

print(df.head(10))



# %%
